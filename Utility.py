# A bunch of utility functions
import hashlib
import requests
import configparser

def md5(filepath):
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest().lower()

def fileExtension(filepath):
    tokens = filepath.split('.')
    return tokens[-1:][0]

def sanitizeLoadedConfig(configDict):
    result = {}
    # for section in configDict:
    #     print(section)
    #     for subsection in configDict[section]:
            # if subsection == 'tumblr_qual':
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

