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
        html = response.read()
        soup = BeautifulSoup(html)
        postID = soup.article['id'][5:]
        return postID
        
    
    def getDbuTagList(postID):
        url = "http://danbooru.donmai.us/posts/" + postID
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html)
        tagHTML = soup.select('#tag-list')[0]
        linkList = tagHTML.find_all('li')

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

        # print 'copyrights:' + str(copyrights)
        # print 'characters:' + str(characters)
        # print 'artists:' + str(artists)
        # print 'tags:' + str(tags)

        return [copyrights, characters, artists, tags]

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
    #print fileToTest
    if utl.dbuExistsImage(fileToTest):
        print "scraping dbu"
        postID = getDbuPostID(md5List[0])
        tagList = getDbuTagList(postID)
        print 'copyrights:' + str(tagList[0])
        print 'characters:' + str(tagList[1])
        print 'artists:' + str(tagList[2])
        print 'tags:' + str(tagList[3])
        
    else:
        print "scraping iqdb"
        opener2 = poster.streaminghttp.register_openers()
        datagen, headers = poster.encode.multipart_encode({'file': open(fileNames[0],'rb')})
        response = opener2.open(urllib2.Request("http://danbooru.iqdb.org/?", datagen, headers))
        html = response.read()
        soup = BeautifulSoup(html)
        postID = soup.find_all('a')[1]['href'][36:]
        tagList = getDbuTagList(postID)
        print 'copyrights:' + str(tagList[0])
        print 'characters:' + str(tagList[1])
        print 'artists:' + str(tagList[2])
        print 'tags:' + str(tagList[3])







        # print "scraping iqdb"
        # url = "http://iqdb.yande.re"
        # values = {}
        # values["url"] = "danbooru.donmai.us/data/d9bec15a23c25bf14fc9d8404a0b31ee.png"
        # #values["filename"] = "/u/students/kotarou/projects/vacbooru/USETOTEST.png"

        # data = urllib.urlencode(values)
        # request = urllib2.Request(url + "/" +"?"+ data)
        # response = urllib2.urlopen(request)
        # html = response.read()
        # soup = BeautifulSoup(html)

        # imageSource = soup.div
        # imageSource = str(imageSource)[31:-68].replace("\n", "")
        
        # imgs = soup.find_all('img')
        # tagList = str(imgs[1])
        # print (imageSource)
        # print tagList




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