# TAKES a set of image paths
# OPTIONALLY TAKES alternate IQDB url, acceptable sites ORDERED
# RETURNS a set of 3 tupples of the form:
# {source_url, source_hash, [tags]}

# Make a request to IQDB with the image
# Find the highest res copy of the image, orders ties based on site
# Download image, as well as tags, other metadata, and source url
# make hash of image
# output all of this data
#import Image as im
import sys
#	depreciacted by urllib.request and uurllib.error in python 3
import urllib2
import urllib
import Utility as utl
from bs4 import *
from poster import *

class VAB_IQDB:
  
    def getDbuPostID(imageMD5):
        url = "http://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=md5%3A" + imageMD5
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response.read())
        postID = soup.article['id'][5:]
        return postID
       
    def getDbuTagList(postID):
        url = "http://danbooru.donmai.us/posts/" + postID
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        soup = BeautifulSoup(response.read())
        
        copyrightHTML = soup.select('.category-3')
        charactersHTML = soup.select('.category-4')
        artistHTML = soup.select('.category-1')
        tagsHTML = soup.select('.category-0')

        copyrights = []
        characters = []
        artists = []
        tags = []
        for instance in copyrightHTML:
            copyrights.append(instance.find_all('a')[1].string)
        for instance in charactersHTML:
            characters.append(instance.find_all('a')[1].string)
        for instance in artistHTML:
            artists.append(instance.find_all('a')[1].string)
        for instance in tagsHTML:
            tags.append(instance.find_all('a')[1].string)

        return [copyrights, characters, artists, tags]

    def getGbuTagList(postID):
        print "Scraping Gbu is not currently supported"
        return None

    def printTagList(tagList):
        print 'copyrights:' + str(tagList[0])
        print 'characters:' + str(tagList[1])
        print 'artists:' + str(tagList[2])
        print 'tags:' + str(tagList[3])

    fileNames = sys.argv[1:]

    md5List = []
    for filename in fileNames:
        md5List.append(utl.md5(filename))

    TEMPPASSWORD = '' #ADD PASSWORD HERE.
        
    username = 'kotarou'
    password = TEMPPASSWORD
    useECSProxy = False
    
    opener = utl.generateOpener(username, password, useECSProxy)
    urllib2.install_opener(opener)

    fileToTest = utl.dbuFilename(md5List[0], utl.fileExtension(fileNames[0]))

    if utl.dbuExistsImage(fileToTest):
        print "Scraping Dbu"
        postID = getDbuPostID(md5List[0])
        tagList = getDbuTagList(postID)
        printTagList(tagList)

    else:
        print "Scraping IQDB"
        opener2 = poster.streaminghttp.register_openers()
        
        #datagen, headers = poster.encode.multipart_encode({'url': URL_TO_CHECK})
        datagen, headers = poster.encode.multipart_encode({'file': open(fileNames[0],'rb')})
        
        response = opener2.open(urllib2.Request("http://iqdb.org/?", datagen, headers))
        soup = BeautifulSoup(response.read())
        result = soup.find_all('a')[1]
        if result['href'][7:15] == "gelbooru":
            print "Image match on Gbu. "
            postID = soup.find_all('a')[1]['href'][50:]
            tagList = getGbuTagList(postID)
        elif result['href'][7:15] == "danbooru":
            print "Image match on Dbu. "
            postID = soup.find_all('a')[1]['href'][36:]
            tagList = getDbuTagList(postID)
            printTagList(tagList)