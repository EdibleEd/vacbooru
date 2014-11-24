# A bunch of utility functions
import hashlib
import requests
import configparser

# Prints if the level of debug printing is greater or equal to this methods threshold to be printed
# typically 0 = never, 1 = standard running, 2-5 = various debug levels
def debugPrint(message, level, threshold):
    if (level >= threshold):
        print(message)

def md5(filepath):
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest().lower()

def fileExtension(filepath):
    tokens = filepath.split('.')
    return tokens[-1:][0]

def sanitizeLoadedConfig(configDict):

    data = configDict['Folder']['tumblr_qual'].replace(" ", "")
    configDict['Folder']['tumblr_qual'] = data.split(',')

    data = configDict['Folder']['image_extensions'].replace(" ", "")
    configDict['Folder']['image_extensions'] = data.split(',')

# proxyaddr: www-cache.ecs.vuw.ac.nz
# proxyport: 8080

def loadConfig(configFile):
    #print(configFile)
    config = configparser.RawConfigParser()
    config.read(configFile)
    
    configDict = {}

    configDict = config._sections

    sanitizeLoadedConfig(configDict)

    return configDict

