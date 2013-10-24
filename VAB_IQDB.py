# TAKES a set of image paths
# OPTIONALLY TAKES alternate IQDB url, acceptable sites ORDERED
# RETURNS a set of 3 tupples of the form:
# {source_url, source_hash, [tags]}

# Make a request to IQDB with the image
# Find the highest res copy of the image, orders ties based on site
# Download image, as well as tags, other metadata, and source url
# make hash of image
# output all of this data
import Image as im
import os, sys
import urllib2
import urllib
from bs4 import *


class VAB_IQDB:
	#temp variable for now
	useECSProxy = False
	
	proxy = 'www-cache.ecs.vuw.ac.nz'
	username = 'kotarou'
	password = ''
	url = "http://iqdb.yande.re"
	if useECSProxy:
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		proxies = {"http":"http://%s" % proxy}

		proxy_info = {
		'user' : username,
		'pass' : password,
		'host' : proxy,
		'port' : 8080 
		}

		# build a new opener that uses a proxy requiring authorization
		proxy_support = urllib2.ProxyHandler({"http" : \
		"http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info})
		opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)

		# install it
		urllib2.install_opener(opener)

		values = {}
	values["url"] = "danbooru.donmai.us/data/d9bec15a23c25bf14fc9d8404a0b31ee.png"

	data = urllib.urlencode(values)
	request = urllib2.Request(url + "/" +"?"+ data)
	response = urllib2.urlopen(request)
	html = response.read()
	soup = BeautifulSoup(html)

	imageSource = soup.div
	imageSource = str(imageSource)[31:-68].replace("\n", "")
	
	imgs = soup.find_all('img')
	tagList = str(imgs[1])
	print (imageSource)
	#r = requests.post(url, payload)




# <form action="/" method="post" enctype="multipart/form-data">
# <p class="flow">Upload an image or thumbnail from a file or URL to find it (or similar images)
# among:</p>
# <input type="hidden" name="MAX_FILE_SIZE"  value="8388608">
# <br>
# <table class="form" style="font-size: 100%;">
# <tr><th><label for="file">File</label></th><td>
# <input type="file" name="file" id="file" size="50">
# </td></tr><tr><td>or</td></tr><tr><th><label for="url">Source URL</label></th><td>
# <input type="text" name="url" id="url" size="50" value="http://"><tr><td>
# <input type="submit" value="submit" accesskey="s">
# </td><td>
# <label>[ <input type="checkbox" name="forcegray"> ignore colors ]</label>
# </td></tr></table>
# <ul><li>Supported file types are JPEG, PNG and GIF</li>
# <li>Maximum file size: 8192 KB</li>
# <li>Maximum image dimensions: 7500x7500</li>
# </ul>
# </form>
