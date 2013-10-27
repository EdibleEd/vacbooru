# A bunch of utility functions
import hashlib
import requests
import configparser

def md5(filepath):
	return hashlib.md5(open(filepath, 'rb').read()).hexdigest().lower()

def dbuFilename(md5, imageType):
	return md5 + '.' + imageType

def fileExtension(filepath):
	tokens = filepath.split('.')
	return tokens[-1:][0]

def dbuExistsImage(dbuFile, proxies, auth):
    url = "http://danbooru.donmai.us/data/" + dbuFile
    r = requests.get(url, proxies=proxies, auth=auth)
    if r.status_code == 404:
    	return False
    else:
    	return True

def configMap(section, netFile):
    f = open(netFile, 'rb')
    config = configparser.ConfigParser()
    config.read(netFile)
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print(("exception on %s!" % option))
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
	return (useProxy, proxyAddr, int(proxyPort), username, password)



# Prints if the level of debug printing is greater or equal to this methods threshold to be printed
# typically 0 = never, 1 = standard running, 2-5 = various debug levels
def debugPrint(message, level, threshold):
	if (level >= threshold):
		print(message)