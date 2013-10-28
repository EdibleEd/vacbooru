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
import argparse
import Utility as utl
from bs4 import *
import requests

class VAB_IQDB:
    def __init__(self, args):
        self.enablePervMode = args.pervMode
        safeString = 'safe.'
        if self.enablePervMode:
            safeString = ''
        self.iqdbList = {
        'Danbooru' : ('http://'+safeString+'danbooru.iqdb.org/'),
        'Gelbooru' : ('http://'+safeString+'gelbooru.iqdb.org/'),
        'eshuushuu' : ('http://'+safeString+'e-shuushuu.iqdb.org/'),
        'yande.re' : ('http://'+safeString+'yandere.iqdb.org/'),
        'The Anime Gallery' : ('http://'+safeString+'theanimegallery.iqdb.org/'),
        'zerochan' : ('http://'+safeString+'zerochan.iqdb.org/'),
        'Manga Drawing' : ('http://'+safeString+'mangadrawing.iqdb.org/'),
        'Anime-Pictures' : ('http://'+safeString+'anime-pictures.iqdb.org/')
        }
        self.urlSearchList = {
        'Danbooru' : 'http://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=md5%3A',
        }
        self.urlPostList = {
        'Danbooru' : 'http://danbooru.donmai.us/posts/',
        }
        useProxy, proxyAddr, proxyPort, username, password  = utl.loadNetworkConfig('networkFile') 
        if useProxy:
            self.proxies = { 'http': 'http://%s:%d' % (proxyAddr, proxyPort) }
            self.auth = requests.auth.HTTPProxyAuth(username, password)
        else:
            self.proxies = None
            self.auth = None

        self.imageList = args.path
        self.md5List = []
        for filename in self.imageList:
            self.md5List.append(utl.md5(filename))

    def soupUrlRequest(self, url):
        r = requests.get(url, proxies=self.proxies, auth=self.auth)
        if r.status_code == 200:
            return BeautifulSoup(r.text)
        else:
            return None
  
    def getPostIDfromMD5(self, service, imageMD5):
        url = self.urlSearchList[service] + imageMD5
        r = self.soupUrlRequest(url)
        if not r == None:
            # Some images exist as a direct link
            # But have ahd their posts removed
            res = r.article
            if not res == None:
                return r.article['id'][5:]
            else:
                print("Image exists but has no post")
        return None
       
    def getTagList(self, service, postID):
        if not service == 'Danbooru':
            print("Scraping" + service + "not currently supported" )
        else:
            if not postID == None:
                url = self.urlPostList[service] + postID
                r = self.soupUrlRequest(url)
                if not r == None:
                    copyrightHTML = r.select('.category-3')
                    charactersHTML = r.select('.category-4')
                    artistHTML = r.select('.category-1')
                    tagsHTML = r.select('.category-0')

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
        return None

    def printTagList(self, tagList):
        print('copyrights:' + str(tagList[0]))
        print('characters:' + str(tagList[1]))
        print('artists:' + str(tagList[2]))
        print('tags:' + str(tagList[3]))

   # def iqdbScrape(url, fileToTest):
   
    def go(self):
        numImages = len(self.imageList)
        for i in range(numImages):
            fileToTest = utl.dbuFilename(self.md5List[i], utl.fileExtension(self.imageList[i]))

            if utl.dbuExistsImage(fileToTest, self.proxies, self.auth):
                # This does not guarentee the image is still linkable
                # Images that have been removed have no postID
                # But still remain direct linkable for some time
                print("Scraping Dbu")
                postID = self.getPostIDfromMD5('Danbooru', self.md5List[i])
                tagList = self.getTagList('Danbooru', postID)
                if tagList == None:
                    print("No tags findable")
                else:
                    self.printTagList(tagList)
            else:
                print("Scraping IQDB")
                files = { 'file' : open(fileNames[0],'rb')}
                r = requests.post('http://iqdb.org/', files=files, proxies=self.proxies, auth=self.auth)
                soup = BeautifulSoup(r.text)
                
                if soup.find_all('table')[1].th.string == 'No relevant matches':
                    print("Image not found on any iqdb linkable site")
                else:        
                    result = soup.find_all('a')[1]
                    tagList = []
                    if result['href'][7:15] == 'gelbooru':
                        print("Image match on Gbu. ")
                        postID = soup.find_all('a')[1]['href'][50:]
                        tagList = self.getTagList('Gelbooru', postID)
                    elif result['href'][7:15] == 'danbooru':
                        print("Image match on Dbu. ")
                        postID = soup.find_all('a')[1]['href'][36:]
                        tagList = self.getTagList('Danbooru', postID)
                    self.printTagList(tagList)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape the web for a set of passed images',  usage='%(prog)s [options]')
    parser.add_argument("path", help="Images to load", metavar='I', type=str, nargs='+')
    parser.add_argument('-e', '--massivePervert', dest='pervMode', action='store_true', help='Enable MASSIVEPERVERT mode aka non-safe scraping')
    args = parser.parse_args()
    loader = VAB_IQDB(args)
    loader.go()