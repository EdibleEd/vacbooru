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
        

# Loads configuration dictionaries
# Uses # for comments
# Uses tab separators

def loadSimpleConfig(configF):
    configDict = {} 
    for line in configF:
        if (not(line.startswith("#"))): # Do not add comments
            if (not(line.strip() == '')): # Don't add whitespace lines or empty lines
                line = line.rstrip('\n') # Don't want newlines
                templ = line.split(None,1)
                if (len(templ[1].split(',')) != 1): # Load comma seperated values as lists
                    configDict[templ[0].strip()] = templ[1].split(',') # Put the first value as the key, then rest as values
                else:
                    configDict[templ[0].strip()] = (templ[1].strip()) # strips are to get rid of lose lines and whitespace
    return configDict

        
