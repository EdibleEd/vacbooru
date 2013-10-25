# A bunch of utility functions
import hashlib
import urllib2
from urllib2 import URLError
import urllib

def md5(filepath):
	return hashlib.md5(open(filepath).read()).hexdigest().lower()

def dbuFilename(md5, imageType):
	return md5 + '.' + imageType

def fileExtension(filepath):
	tokens = filepath.split('.')
	return tokens[-1:][0]

def dbuExistsImage(dbuFile):
	url = "http://danbooru.donmai.us/data/" + dbuFile
	request = urllib2.Request(url)
	try:
		response = urllib2.urlopen(request)
		return True
	except URLError, e:
		print e.reason
	return False

def generateOpener(username, password, useECSProxy = False):
	proxy = 'www-cache.ecs.vuw.ac.nz'
	if useECSProxy:
		passwordMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		proxies = {"http":"http://%s" % proxy}
		proxy_info = {
		'user' : username,
		'pass' : password,
		'host' : proxy,
		'port' : 8080 
		}
		# build a new opener that uses a proxy requiring authorization
		proxy_support = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info})
		return urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
	else:
		return None;
		
# Prints if the level of debug printing is greater or equal to this methods threshold to be printed
# typically 0 = never, 1 = standard running, 2-5 = various debug levels
def debugPrint(message, level, threshold):
	if (level >= threshold):
		print(message)