from bs4 import BeautifulSoup
import urllib
import requests
from pprint import pprint

base_url = "https://streeteasy.com"
base_rent_url = "https://streeteasy.com/for-rent/nyc"
default_search_vars = "price:-2500%7Carea:140,137%7Cbeds:1"
pet_friendly_no_fee = "pet-friendly-rentals/midtown-all/status:open%7Cprice:-2500%7Cbeds:1%7Cno_fee:1"
page_var = "?page="

listings = []

# This script has become defunct because streeteasy uses distil, blocking scraping efforts
# The logic in place for parsing the html can still be used if you manually navigate to the url and save the page to a file
#  but this ultimately defeats the point of the script

def get_page_url(page=1):
	url = "%s/%s%s" % (base_url, pet_friendly_no_fee, page_var)
	return url

for x in xrange(1, 2):
	url = get_page_url(x)
	r = urllib.urlopen(url).read()
	soup = BeautifulSoup(r, 'html.parser')
	lst = soup.find_all(lambda tag: tag.has_attr('data-id'))

	# soup = BeautifulSoup(open('ses.html'), 'html.parser')
	# lst = soup.find_all('article')

	for item in lst:
		listing = {'link':'', 'beds':'', 'baths':'', 'where':'', 'size':'', 'rent':'', 'address':''}
		# print(item)
		#link
		links = item.find_all('a', href=True)
		listing['link'] = "%s%s" % (base_url, links[0]['href'])

		#where
		if item.find_all('li', {'class':'details_info'}) == []:
			listing['where'] = ''
			pass
		else:
			tempstr = str(item.find_all('li', {'class':'details_info'})[0].string)
			if tempstr != 'None':
				listing['where'] = tempstr.split('in ')[1].strip()

		#rent
		if item.find_all('span', {'class':'price'}) == []:
			listing['rent'] = 'N/A'
		else:
			listing['rent'] = item.find_all('span', {'class':'price'})[0].string

		#beds
		if item.find_all('li', {'class':'first_detail_cell'}) == []:
			listing['beds'] = 'N/A'
		else:
			listing['beds'] = item.find_all('li', {'class':'first_detail_cell'})[0].string

		#baths
		#size
		if item.find_all('li', {'class':'detail_cell'}) == []:
			listing['size'] = ''
			if item.find_all('li', {'class':'last_detail_cell'}) == []:
				# listing['baths'] = 'N/A'
				pass
			else:
				listing['baths'] = item.find_all('li', {'class':'last_detail_cell'})[0].string
		else:
			listing['baths'] = item.find_all('li', {'class':'detail_cell'})[0].string
			if item.find_all('li', {'class':'last_detail_cell'}) == []:
				# listing['size'] = 'N/A'
				pass
			else:
				listing['size'] = "%s sqft" % item.find_all('li', {'class':'last_detail_cell'})[0].string.encode('utf-8').split(' ')[0]


		#street
		listing['address'] = links[1].get_text()

		listings.append(listing)

pprint(listings)
