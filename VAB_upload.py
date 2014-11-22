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
import os
import sys

# Actually builds the post request, then executes it on vacbooru
class VAB_upload:
	def __init__(self, config):
		self.config = config
		self.user = config['username']
		self.api_token = config['api_token']
		print('Uploader init')

	def go(self, tagset):
		# First thing to do, is retrieve a tage list for the image
		f = open(tagset['local_file'], 'rb')
		fileToSend	= { 'upload[file]' : f}
		fff = { 'upload[tag_string]' : tagset['tag_string_general'],
				'upload[rating]' : tagset['rating'], 
				'upload[source]' : tagset['source']}

		r = requests.post('http://anubis/uploads.json', files=fileToSend, data=fff, auth=HTTPBasicAuth(self.user, self.api_token), verify=False)
		f.close()
		print("Uploaded!")

		# Now that we have uploaded it, lets move it to a new location, so we don't reupload it later
		a = tagset['local_file'].rfind('\\')
		newDir = tagset['local_file'][:a] + '\\vab_successfulupload'
		try:
			if not os.path.exists(newDir):
				os.makedirs(newDir)
			print(tagset['local_file'])
			print(newDir + '\\' + tagset['local_file'][a+1:])
			os.rename(tagset['local_file'], newDir + '\\' + tagset['local_file'][a+1:])
		except:
			print('File ' + tagset['local_file'][a+1:] + ' could not be moved')
			print("Error:", sys.exc_info()[0])


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Upload an image to the local dbu server",  usage="%(prog)s [options]")
	parser.add_argument("image", help="Image to upload", metavar='I', type=str, nargs='+')
	args = parser.parse_args()
	loader = VAB_upload(args.image)
	loader.go()
