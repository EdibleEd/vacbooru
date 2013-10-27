# A bunch of utility functions
import hashlib
import urllib2
from urllib2 import URLError
import urllib
import ConfigParser

def md5(filepath):
	return hashlib.md5(open(filepath, 'rb').read()).hexdigest().lower()

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
    	print "Exact image not found on Dbu."
        #print e     #2.7
        #print e    #3
    return False

def generateProxyHandle(username, password, proxyAddr, proxyPort):
	passwordMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	proxies = {'http':"http://%s" % proxyAddr}
	proxy_info = {
	'user' : username,
	'pass' : password,
	'host' : proxyAddr,
	'port' : proxyPort 
	}
	# build a new opener that uses a proxy requiring authorization
	proxy_support = urllib2.ProxyHandler({'http' : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxy_info})
	return proxy_support
	#return urllib2.build_opener(proxy_support, urllib2.HTTPHandler)

def configMap(section, netFile):
    f = open(netFile, 'rb')
    config = ConfigParser.ConfigParser()
    config.read(netFile)
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    f.close()
    return dict1

#	Example network file
# [Default]
# username: blah
# password: blah
# proxyaddr: www-cache.ecs.vuw.ac.nz
# proxyport: 8080

def loadNetworkConfig(netFile):
	loadedConfig = configMap('Default', netFile)
	username = loadedConfig['username']
	password = loadedConfig['password']
	proxyAddr = loadedConfig['proxyaddr']
	proxyPort = loadedConfig['proxyport']
	useProxy = True
	if proxyAddr == 'None' or proxyPort == 'None':
		useProxy = False
	return {useProxy, proxyAddr, int(proxyPort), username, password}



# Prints if the level of debug printing is greater or equal to this methods threshold to be printed
# typically 0 = never, 1 = standard running, 2-5 = various debug levels
def debugPrint(message, level, threshold):
	if (level >= threshold):
		print(message)