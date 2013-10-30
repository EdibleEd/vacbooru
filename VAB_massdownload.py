import urllib2
import urllib
import os, sys
from bs4 import *

argv = sys.argv[1:]
begin = int(argv[0])
count = int(argv[1])

for i in range(begin, begin+count):
	try:
		url = 'http://danbooru.donmai.us/posts/' + str(i)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		
		html = response.read()
		soup = BeautifulSoup(html)
		
		relURL = soup.select('#image')[0]['src'].split('/data/')[1]
		if 'sample' in relURL:
			# Image was too big and thus was resized. 
			relURL = relURL.split('sample-')[1]

		newPath = 'http://danbooru.donmai.us/data/' + relURL
		newFile = 'C:\\programming\\vacbooru-master\\dbu\\' + relURL
		if not os.path.exists(newFile):
			f = open(newFile,'wb')
			f.write(urllib.urlopen(newPath).read())
			f.close()
			print str(i) + " downloaded"
		else:
			print str(i) + " already exists"
	except Exception as e:
		print str(i) + " download failed: " + str(e)
		if 'list index out of range' in str(e):
			print "\t This is likley a image that needs dbu gold"