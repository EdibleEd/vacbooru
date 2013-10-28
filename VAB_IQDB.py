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
        self.iqdbList = {
        'Danbooru' : 'http://danbooru.iqdb.org/',
        'Gelbooru' : 'http://gelbooru.iqdb.org/',
        'eshuushuu' : 'http://e-shuushuu.iqdb.org/',
        'yande.re' : 'http://yandere.iqdb.org/',
        'The Anime Gallery' : 'http://theanimegallery.iqdb.org/',
        'zerochan' : 'http://zerochan.iqdb.org/',
        'Manga Drawing' : 'http://mangadrawing.iqdb.org/',
        'Anime-Pictures' : 'http://anime-pictures.iqdb.org/'
        }
        self.urlList = {
        'Danbooru' : 'http://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=md5%3A',
        }
        useProxy, proxyAddr, proxyPort, username, password  = utl.loadNetworkConfig('networkFile') 
        if useProxy:
            self.proxies = { 'http': 'http://%s:%d' % (proxyAddr, proxyPort) }
            self.auth = requests.auth.HTTPProxyAuth(username, password)
        else:
            self.proxies = None
            self.auth = None


    def urlRequest(self, url):
        r = requests.get(url, proxies=self.proxies, auth=self.auth)
        if r.status_code == 200:
            return r
        else:
            return None
  
    def getPostIDfromMD5(self, service, imageMD5):
        url = self.urlList[service] + imageMD5
        r = self.urlRequest(url)
        if not r == None:
            postID = BeautifulSoup(r.text).article['id'][5:]
            if not postID == None:
                return postID
        return None
       
    def getTagList(self, service, postID):
        url = "http://danbooru.donmai.us/posts/" + postID
        r = requests.get(url, proxies=self.proxies, auth=self.auth)

        soup = BeautifulSoup(r.text)
        
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

    def getGbuTagList(self, postID):
        print("Scraping Gbu is not currently supported")
        return None

    def printTagList(self, tagList):
        print('copyrights:' + str(tagList[0]))
        print('characters:' + str(tagList[1]))
        print('artists:' + str(tagList[2]))
        print('tags:' + str(tagList[3]))

   # def iqdbScrape(url, fileToTest):
   
    def go(self, path):
        fileName = path
        # md5List = []
        # for filename in fileNames:
        #     md5List.append(utl.md5(filename))
        md5List = utl.md5(fileName)
        useProxy, proxyAddr, proxyPort, username, password  = utl.loadNetworkConfig('networkFile') 

        fileToTest = utl.dbuFilename(md5List, utl.fileExtension(fileName))

        if utl.dbuExistsImage(fileToTest, self.proxies, self.auth):
            # This does not guarentee the image is still linkable
            # Images that have been removed have no postID
            # But still remain direct linkable for some time
            print("Scraping Dbu")
            postID = self.getPostIDfromMD5('Danbooru', md5List)
            tagList = self.getTagList('Danbooru', postID)
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
                if result['href'][7:15] == 'gelbooru':
                    print("Image match on Gbu. ")
                    postID = soup.find_all('a')[1]['href'][50:]
                    tagList = self.getGbuTagList(postID)
                elif result['href'][7:15] == 'danbooru':
                    print("Image match on Dbu. ")
                    postID = soup.find_all('a')[1]['href'][36:]
                    tagList = self.getDbuTagList(postID)
                    self.printTagList(tagList)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape the web for a set of passed images')
    parser.add_argument("path", help="Image to load")
    args = parser.parse_args()
    loader = VAB_IQDB(args)
    loader.go(args.path)