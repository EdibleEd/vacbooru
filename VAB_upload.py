# TAKES a set of tupples of the form
# {source_url, source_hash, [tags]}
# OPTIONALLY TAKES 
# RETURNS return code

import VAB_scraper
import argparse
import Utility as utl
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# Actually builds the post request, then executes it on vacbooru
class VAB_upload:
	def __init__(self, image):
		self.image = image
		self.scraper = VAB_scraper.VAB_scraper(False, 'iqdb', image)
		useProxy, proxyAddr, proxyPort, username, password  = utl.loadNetworkConfig('config/network.conf') 
		if useProxy:
			self.proxies = { 'http': 'http://%s:%d' % (proxyAddr, proxyPort) }
			self.auth = requests.auth.HTTPProxyAuth(username, password)
		else:
			self.proxies = None
			self.auth = None


	def go(self):
		# First thing to do, is retrieve a tage list for the image
		tag_list = self.scraper.go()
		
		fileToSend	= { 'upload[file]' : open(self.image[0], 'rb')}
		fff = { 'upload[tag_string]' : ' '.join(tag_list),
				'upload[rating]' : 's' }
		r = requests.post('http://anubis/uploads.json', files=fileToSend, data=fff, auth=HTTPBasicAuth('kotarou', 'MZsTCjO0bVqJgbPZWFNBs8tl7UrwG3wv9TVGKrKNL1U'), verify=False)

		print(r.text)












		#s = requests.session()
		#r = s.get(url,verify = False)
		#r = s.post(url,data=data,verify = False)
		#r = s.get('http://anubis/',verify = False)
		#print(r.text)

		# requests.get('http://anubis/session/new/', auth=('kotarou', 'suzumiya13'))
		# response = requests.post('http://anubis/uploads', files=fileToSend, proxies=self.proxies, auth=self.auth)
		# soup = BeautifulSoup(response.text)
		# print(soup.prettify().encode('utf-8'))
		# with requests.Session() as s:
		# 	s.post('http://anubis/session/new/', data=data)
		# 	r = s.get('http://anubis/posts')
		# 	soup = BeautifulSoup(r.text)
		# 	print(soup.prettify().encode('utf-8'))
		#response = requests.post('http://anubis/session/new/', params=data, proxies=self.proxies, auth=self.auth)

		# Upload the image (this may take a while)
		# response = requests.post('http://anubis/uploads', files=fileToSend, proxies=self.proxies, auth=self.auth)
		

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Upload an image to the local dbu server",  usage="%(prog)s [options]")
	parser.add_argument("image", help="Image to upload", metavar='I', type=str, nargs='+')
	args = parser.parse_args()
	loader = VAB_upload(args.image)
	loader.go()
