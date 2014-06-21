# TAKES a set of image paths
# OPTIONALLY TAKES alternate IQDB url, acceptable sites ORDERED
# RETURNS a set of 4 tuples of the form:
# {source_indicator + source_id, source_hash, filetype, [tags]}

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
    def __init__(self, pervmode, scrapeTarget, path):
        self.enablePervMode = pervmode
        safeString = 'safe.'
        if self.enablePervMode:
            safeString = ''
            fun()

        self.scrapeTarget = scrapeTarget

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
        'Pixiv'             : 'http://www.pixiv.net/member_illust.php?mode=medium&amp;illust_id='
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

        self.imageList = path
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
            # But have had their posts removed
            res = r.article
            if not res == None:
                return r.article['id'][5:]
            else:
                print("Image exists but has no post")
        return 0
       
    def getTagList(self, service, postID):
        copyrights = []
        characters = []
        artists = []
        tags = []
        
        if service == 'Danbooru':
            url = self.urlPostList[service] + postID
            r = self.soupUrlRequest(url)
            copyrightHTML = r.select('.category-3')
            charactersHTML = r.select('.category-4')
            artistHTML = r.select('.category-1')
            tagsHTML = r.select('.category-0')

            for instance in copyrightHTML:
                copyrights.append(instance.find_all('a')[1].string)
            for instance in charactersHTML:
                characters.append(instance.find_all('a')[1].string)
            for instance in artistHTML:
                artists.append(instance.find_all('a')[1].string)
            for instance in tagsHTML:
                tags.append(instance.find_all('a')[1].string)

            return [copyrights, characters, artists, tags]
        elif service == 'Pixiv':
            url = self.urlPostList[service] + postID
            r = self.soupUrlRequest(url)
            
            artists.append(r.select('.title')[4].string)

            tagsHTML = r.select('.inline-list')

 
            for instance in tagsHTML:
                # Don't open pixiv-encycopedia links
                if instance.find_all('img') == []:
                    tags.append(instance.find_all('a')[1].string)
            tags.append('tag_clean_request')


        else:
            print("Scraping " + service + "not currently supported" )
            return None
        return [copyrights, characters, artists, tags]

    def formatTagList(self, tagList):
        outList = []
        for artist in tagList[2]:
            outList.append('a::' + artist)
        for copyright in tagList[0]:
            outList.append('p::' + copyright)
        for character in tagList[1]:
            outList.append('c::' + character)
        for tag in tagList[3]:
            outList.append(tag)
        return outList


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

    def scrapeIDfromAggregator(self, service, imageToFind):
        # Scrape the image we are after off one of the aggregator sites
        # I would like to supplement this with VAB_classify output

        if service == 'iqdb':
            # IQDB can take a URL or multi-part post image
            # Only use the image post method as we have no reliable online storage at this step
            
            print("Scraping IQDB")
            postID          = 0
            tagList         = []
            fileToSend      = { 'file' : open(imageToFind,'rb')}
            
            # Upload the image (this may take a while)
            response = requests.post('http://iqdb.org/', files=fileToSend, proxies=self.proxies, auth=self.auth)
            soup = BeautifulSoup(response.text)
            
            if soup.find_all('table')[1].th.string == 'No relevant matches':
                # IQDB has failed us
                print("Image not found on any iqdb linkable site")
                return (0,[])
            
            else:
                # IQDB has found a match
                result = soup.find_all('a')[1]
                if result['href'][7:15] == 'danbooru':
                    print("IQDB search match on Dbu. ")
                    postID = soup.find_all('a')[1]['href'][36:]
                    return (postID, 'Danbooru')
                
                elif result['href'][7:15] == 'gelbooru':
                    print("IQDB search match on Gbu.")
                    postID = soup.find_all('a')[1]['href'][50:]
                    return (postID, 'Gelbooru')
                

        
        elif service == 'sourcenao':
            # sourceNAO takes 
            
            print("Scraping sourceNAO")
            postID =        0
            tagList =       []
            fileToSend =    { 'file' : open(imageToFind,'rb')}
            tempURL =       None
            
            response = requests.post('http://saucenao.com/search.php', files=fileToSend, proxies=self.proxies, auth=self.auth)
            soup = BeautifulSoup(response.text)
            
            # Unlike iqdb, sourcenao scrapes pixiv
            # But if it returns a good danbooru result, we want to use that instead
            # Even if the pixiv result is a better match
            # This way we can use the tags from dbu rather than from pixiv
            # SourceNAO shows characters and artist but that is all.
            if 'Daily Search Limit Exceeded.' in soup.strong.string:
                print("sourceNAO search limit exceeded")
                return (-2,[])

            try:
                if 'Low similarity' in soup.select('.result')[0].string:
                    print("sourceNAO found nothing")
                    return (-2,[])
            except:
                pass

            firstSourceLoc = soup.select('.result')[0].select('.linkify')[-2]['href']
            print("Image source is: " + firstSourceLoc)
            print(firstSourceLoc)
            if 'pixiv' in firstSourceLoc:
                # We want to try find some english tags if possible
                # So we'll check the second result for danbooru links
                # Lower than second and we can't guarentee correct results
                secondSource = soup.select('.result')[1]
                if not secondSource == None:
                    if 'have been hidden' not in secondSource:
                        # A result is worth checking for english tags!
                        secondSourceLoc = secondSource.find_all('a')[1]['href']
                        if 'danbooru' in secondSourceLoc:
                            # The second result contained a useful danbooru link. Lets use it
                            print("Roughly matching dbu source: " + secondSourceLoc)
                            postID = secondSourceLoc[36:]
                if postID == 0:
                    # We need to look on pixiv
                    postID = firstSourceLoc[61:]
                    return (postID, 'Pixiv')

            elif 'danbooru' in firstSourceLoc:
                pass
                # scrape the dbu result
                # TODO

            return (postID, 'Danbooru')

        return (0,[])


    def go(self):
        # We don't mind at this point if the image is already on vacbooru
        # As it may have new tags that get added by the current user

        numImages = len(self.imageList)
        for i in range(numImages):
            fileToTest =    self.md5List[i] + utl.fileExtension(self.imageList[i])
            onDbu =         self.directLinkExists('Danbooru', fileToTest, 'file')
            postID =        0
            service =       None
            tagList =       []
            
            if onDbu:
                # The image exists on dbu with an identical md5 hash
                print("Scraping Dbu")
                postID = self.getPostIDfromMD5('Danbooru', self.md5List[i])

                # Some images exist viw direct link but have had their posts removed
                # This normally means the image is flagged for deletion but is not yet removed 
                if not self.directLinkExists('Danbooru', postID, 'post'):
                    postID = 0
                else:
                    service = 'Danbooru'
            
            if postID == 0:
                # Either the image isn't on Dbu, or it is but the post is deleted so we can't get the tags
                # So instead, find the image off a scraping service
                # Two services are supported: sourceNAO and IQDB
                #   IQDB puts the user in a queue if under high load
                #   sourceNAO has a limit of 100 uploads per day for a non-user
                # Differing user browsing habits will benifit choosing one site over the other
                #   game cgs or risque -    iqdb
                #   pixiv or quality -      sourceNAO     
                
                if self.scrapeTarget == 'iqdb':
                    postID, service = self.scrapeIDfromAggregator('iqdb', self.imageList[i])
                
                if postID == 0:
                    # The scrape target is sourceNAO or IQDB scrape failed
                    postID, service = self.scrapeIDfromAggregator('sourcenao', self.imageList[i])
                    
            # A > 0 postID means a taglist was found
            # 0 means no post was found
            # -1 means a post was found but no tags were (this shouldn't ever occur normally)
            # -2 means sourceNAO or IQDB returned an unhelpful page like upload limit exceeded
            if int(postID) <= 0:
                print("Tag retrieval unsuccessful")
            else:
                tagList = self.getTagList(service, postID)  
                tagList = self.formatTagList(tagList)
                print(tagList)

    def fun(self):
        # Fun might go here        
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape the web for a set of passed images",  usage="%(prog)s [options]")
    parser.add_argument("path", help="Images to load", metavar='I', type=str, nargs='+')
    parser.add_argument('-e', '--massivePervert', dest='pervMode', action='store_true', help="Enable MASSIVEPERVERT mode aka non-safe scraping")
    parser.add_argument('-s', '--source', dest='scrapeTarget', type=str, default='iqdb', help="Select the service to scrape first: idqd (iqdb) or sourceNAO (sourenao)" )
    args = parser.parse_args()
    loader = VAB_scraper(args.pervMode, args.scrapeTarget, args.path)
    loader.go()
