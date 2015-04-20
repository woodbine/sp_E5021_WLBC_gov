# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5021_WLBC_gov"
url = "http://www.wandsworth.gov.uk/downloads/200110/council_budgets_and_spending"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
block = soup.find('section', {'class':'page-content inner_content'})
pageLists = block.findAll('li')

for pageList in pageLists:
	pageUrl = pageList.a['href']
	if 'CSV' in pageList.text: # Looks for 'CSV' in the text of the list tag
	  	html2 = urllib2.urlopen(pageUrl)
	  	soup2 = BeautifulSoup(html2)
	  	fileLinks = soup2.findAll('a', href=True)
	  	for fileLink in fileLinks:
	  		url = fileLink['href']
	  		if 'http://www.wandsworth.gov.uk/download/downloads/id/' in url:
	  			# create the right strings for the new filename
	  			title = fileLink.text
	  			csvYr = title.split(' ')[1]
	  			csvMth = title.split(' ')[0][:3]
	  			csvMth = csvMth.upper()
	  			csvMth = convert_mth_strings(csvMth);
	  			filename = entity_id + "_" + csvYr + "_" + csvMth + ".csv"
	  			todays_date = str(datetime.now())
	  			scraperwiki.sqlite.save(unique_keys=['l'], data={"l": url, "f": filename, "d": todays_date })
	  			print filename
