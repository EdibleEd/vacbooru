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

class VAB_scraper:
    def __init__(self, args):
        self.enablePervMode = args.pervMode
        safeString = 'safe.'
        if self.enablePervMode:
            safeString = ''
            fun()

        self.scrapeTarget = args.scrapeTarget

        self.iqdbList = {
        'Danbooru'          : ('http://'+safeString+'danbooru.iqdb.org/'),
        'Gelbooru'          : ('http://'+safeString+'gelbooru.iqdb.org/'),
        'eshuushuu'         : ('http://'+safeString+'e-shuushuu.iqdb.org/'),
        'yande.re'          : ('http://'+safeString+'yandere.iqdb.org/'),
        'The Anime Gallery' : ('http://'+safeString+'theanimegallery.iqdb.org/'),
        'zerochan'          : ('http://'+safeString+'zerochan.iqdb.org/'),
        'Manga Drawing'     : ('http://'+safeString+'mangadrawing.iqdb.org/'),
        'Anime-Pictures'    : ('http://'+safeString+'anime-pictures.iqdb.org/')
        }
        self.urlSearchList = {
        'Danbooru'          : 'http://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=md5%3A',
        }
        self.urlPostList = {
        'Danbooru'          : 'http://danbooru.donmai.us/posts/',
        'pixiv'             : 'http://www.pixiv.net/member_illust.php?mode=medium&amp;illust_id='
        }
        self.urlDataList = {
        'Danbooru'          : 'http://danbooru.donmai.us/posts/',
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
        if service == 'Danbooru':
            url = self.urlPostList[service] + postID
            r = self.soupUrlRequest(url)
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
        else:
            print("Scraping" + service + "not currently supported" )
        return None

    def printTagList(self, tagList):
        print('copyrights:' + str(tagList[0]))
        print('characters:' + str(tagList[1]))
        print('artists:' + str(tagList[2]))
        print('tags:' + str(tagList[3]))


    def directLinkExists(self, service, query, urlType):
        url = ''
        if urlType == 'post':
            url = self.urlPostList[service] + query
        elif urlType == 'file':
            url = self.urlDataList[service] + query
        r = requests.get(url, proxies=self.proxies, auth=self.auth)
        if r.status_code == 404:
            return False
        else:
            return True

    def scrape(self, service, imageToFind):
        if service == 'iqdb':
            print("Scraping IQDB")
            files = { 'file' : open(imageToFind,'rb')}
            r = requests.post('http://iqdb.org/', files=files, proxies=self.proxies, auth=self.auth)
            soup = BeautifulSoup(r.text)
            if soup.find_all('table')[1].th.string == 'No relevant matches':
                print("Image not found on any iqdb linkable site")
                return None
            else:
                result = soup.find_all('a')[1]
                tagList = []
                if result['href'][7:15] == 'gelbooru':
                    print("Image match on Gbu. ")
                    postID = soup.find_all('a')[1]['href'][50:]
                    return self.getTagList('Gelbooru', postID)
                elif result['href'][7:15] == 'danbooru':
                    print("Image match on Dbu. ")
                    postID = soup.find_all('a')[1]['href'][36:]
                    return self.getTagList('Danbooru', postID)
        elif service == 'sourcenao':
            print("Scraping sourceNAO")
            files = { 'file' : open(imageToFind,'rb')}
            r = requests.post('http://saucenao.com/search.php', files=files, proxies=self.proxies, auth=self.auth)
            soup = BeautifulSoup(r.text)
            # Unlike iqdb, sourcenao scrapes pixiv
            # But if it returns a good danbooru result, we want to use that instead
            # Even if the pixiv result is a better match
            # This way we can use the tags from dbu rather than from pixiv
            # SourceNAO shows characters and artist but that is all.
            if 'Daily Search Limit Exceeded.' in soup.strong.string:
                print("sourceNAO search limit exceeded")
                return None

            firstSourceLoc = soup.select('.result')[0].select('.linkify')[-2]['href']
            print("Image source is: " + firstSourceLoc)
            
            if 'pixiv' in firstSourceLoc:
                secondSource = soup.select('.result')[1]
                # We want to try find some english tags if possible
                if not secondSource == None:
                    if 'have been hidden' not in secondSource.string:
                        # Some results worth checking for english tags!
                        secondSourceLoc = secondSource.find_all('img')[0]['title']
                        if "Danbooru" in secondSourceLoc:
                            print("Roughly matching dbu source: " + secondSourceLoc)
                            postID = secondSource.select('.resultmiscinfo')[0].find_all('a')[0]['href'].split('show/')[1]
                            return self.getTagList('Danbooru', postID)
                else:
                    # No results worth checking for english tags
                    print("Pixiv scraping not currently enabled")
                    # TODO
        return None


    def go(self):
        numImages = len(self.imageList)
        for i in range(numImages):
            fileToTest = self.md5List[i] + utl.fileExtension(self.imageList[i])
            aggregator =    True
            
            if not self.directLinkExists('Danbooru', fileToTest, 'file'):
                aggregator = False
                # The image exists on dbu with an identical md5
                print("Scraping Dbu")
                postID = self.getPostIDfromMD5('Danbooru', self.md5List[i])
                if not postID == None and self.directLinkExists('Danbooru', postID, 'post'):
                    tagList = self.getTagList('Danbooru', postID)
                    self.printTagList(tagList)
                else:
                    print("No tag findable on dbu")
                    aggregator = True
            
            if aggregator:
                # Scrape an aggregator service
                # Depending on your browsing habits, either iqdb or sourcenao work here
                # Be careful of upload limits, these are not tested yet        
                if self.scrapeTarget == 'iqdb':
                    tagList = self.scrape('iqbd', self.imageList[i])
                    if tagList == None:
                        tagList = self.scrape('sourcenao', self.imageList[i])
                else:
                    #self.scrapeTarget == 'sourcenao'
                    tagList = self.scrape('sourcenao', self.imageList[i])
                    if tagList == None:
                        tagList = self.scrape('iqbd', self.imageList[i])
                if tagList == None:
                    print("Tag retrieval unsuccessful")
                else:
                    self.printTagList(tagList)

    def fun(self):
        # Fun might go here        
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape the web for a set of passed images",  usage="%(prog)s [options]")
    parser.add_argument("path", help="Images to load", metavar='I', type=str, nargs='+')
    parser.add_argument('-e', '--massivePervert', dest='pervMode', action='store_true', help="Enable MASSIVEPERVERT mode aka non-safe scraping")
    parser.add_argument('-s', '--source', dest='scrapeTarget', type=str, default='iqdb', help="Select the service to scrape first: idqd (iqdb) or sourceNAO (sourenao)" )
    args = parser.parse_args()
    loader = VAB_scraper(args)
    loader.go()
