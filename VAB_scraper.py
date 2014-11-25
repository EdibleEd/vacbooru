# TAKES a set of image paths
# OPTIONALLY TAKES alternate IQDB url, acceptable sites ORDERED
# RETURNS a set of 4 tuples of the form:
# {source_indicator + source_id, source_hash, filetype, [tags]}

# Make a request to IQDB with the image
# Find the highest res copy of the image, orders ties based on site
# Download image, as well as tags, other metadata, and source url
# make hash of image
# output all of this data

# #import Image as im
# import argparse
# import Utility as utl
# from bs4 import BeautifulSoup
# import requests
# import urllib.request #replace this asap
# import json
# from requests.auth import HTTPBasicAuth
# import sys
# import xmltodict
from Network import Network
from scrape_danbooru import DanbooruScraper as dbuScraper
from scrape_pixiv import PixivScraper as pxvScraper
import Utility as utl

class VAB_scraper:
    def __init__(self, pervmode, authConfig, network):
        # scrapeTarget is the filename we are currently inspecting
        # authConfig provides the credentials for the sites we will scrape
        self.authConfig = authConfig
        self.targetFile = ''
        self.network    = network
        self.scrapers   =   {
                                'donmai.us' : dbuScraper(authConfig['donmai.us'], self.network),
                                'pixiv.net' : pxvScraper(authConfig['pixiv.net'], self.network),
                            }

        self.lookup     = []

    def setupTarget(self, targetFile, serviceList):
        self.lookup = []
        self.targetFile = targetFile
        for service in serviceList:
            if service in self.scrapers.keys():
                self.lookup.append(service)
            else:
                print('Service ' + service + ' is not currently supported')

    def scrape(self):
        results = ''
        md5 = utl.md5(self.targetFile)
        for service in self.lookup:
            scraper = self.scrapers[service]
            scraper.setLocalFile(self.targetFile)
            
            postID = scraper.findPostByMD5(md5)

            #print('a' + str(postID))
            
            if postID == 0:
                postID = scraper.findPostByFileName(self.targetFile)
            
            #print('b' + str(postID))
            
            if postID != 0 and scraper.postExists(postID):
                rawData = scraper.generateRawData(postID)
                if rawData != 0:
                    tagList = scraper.extractPostInfo(rawData)
                    #print(tagList)
                    return tagList
        return 0


# x = Network('a')

# y = PixivScraper('b', x)
# y.setLocalFile('J:\\pictures\\_culled\\temp\\24382481.jpg')
# zz = y.findPostByFileName('J:\\pictures\\_culled\\touhou\\24382481.jpg')
# print(zz)
# z = y.generateRawData(zz)
# a = y.extractPostInfo(z)

# print(a)




# class VAB_scraper:
#     def __init__(self, pervmode, scrapeTarget, network_config, auth_config):
#         self.enablePervMode = pervmode
#         safeString = 'safe.'
#         if self.enablePervMode:
#             safeString = ''
#             #fun()

#         self.scrapeTarget = scrapeTarget

#         self.iqdbList = {
#         'Danbooru'          : ('http://'+safeString+'danbooru.iqdb.org/'),
#         'Gelbooru'          : ('http://'+safeString+'gelbooru.iqdb.org/'),
#         'eshuushuu'         : ('http://'+safeString+'e-shuushuu.iqdb.org/'),
#         'yande.re'          : ('http://'+safeString+'yandere.iqdb.org/'),
#         'The Anime Gallery' : ('http://'+safeString+'theanimegallery.iqdb.org/'),
#         'zerochan'          : ('http://'+safeString+'zerochan.iqdb.org/'),
#         'Manga Drawing'     : ('http://'+safeString+'mangadrawing.iqdb.org/'),
#         'Anime-Pictures'    : ('http://'+safeString+'anime-pictures.iqdb.org/')
#         }
#         self.urlSearchList = {
#         'Danbooru'          : 'http://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=md5%3A',
#         }
#         self.urlPostList = {
#         'Danbooru'          : 'http://danbooru.donmai.us/posts/',
#         'Pixiv'             : 'http://www.pixiv.net/member_illust.php?mode=medium&amp;illust_id='
#         }
#         self.urlDataList = {
#         'Danbooru'          : 'http://danbooru.donmai.us/data/',
#         }

#         self.proxies = None
#         self.auth = None

#         self.user = auth_config['username']
#         self.api_token = auth_config['api_token']


#         # useProxy, proxyAddr, proxyPort, username, password  = utl.loadNetworkConfig('config/network.conf') 
#         # if useProxy:
#         #     self.proxies = { 'http': 'http://%s:%d' % (proxyAddr, proxyPort) }
#         #     self.auth = requests.auth.HTTPProxyAuth(username, password)
#         # else:
#         #     self.proxies = None
#         #     self.auth = None

#     def setFile(self, path):
#         self.image      = path
#         self.md5        = utl.md5(path)
#         self.imageName  = self.md5 + '.' + utl.fileExtension(self.image)
#         self.flag       = False

#     def soupUrlRequest(self, url):
#         if 'danbooru' in url:
#             r = requests.get(url, auth=HTTPBasicAuth(self.user, self.api_token))#, proxies=self.proxies, auth=self.auth)
#         else:
#              r = requests.get(url)
#         if r.status_code == 200:
#             try:
#                 return BeautifulSoup(r.text, "html5lib")
#             except:
#                 print('HTML encoding error. Skipping file')
#                 return None
#         else:
#             return None
       
#     def getTagList(self, service, postID):
#         copyrights = []
#         characters = []
#         artists = []
#         tags = []
        
#         if service == 'Danbooru':
#             url = self.urlPostList[service] + postID
#             r = self.soupUrlRequest(url)
#             copyrightHTML = r.select('.category-3')
#             charactersHTML = r.select('.category-4')
#             artistHTML = r.select('.category-1')
#             tagsHTML = r.select('.category-0')

#             for instance in copyrightHTML:
#                 copyrights.append(instance.find_all('a')[1].string)
#             for instance in charactersHTML:
#                 characters.append(instance.find_all('a')[1].string)
#             for instance in artistHTML:
#                 artists.append(instance.find_all('a')[1].string)
#             for instance in tagsHTML:
#                 tags.append(instance.find_all('a')[1].string)

#             return [copyrights, characters, artists, tags]
#         elif service == 'Pixiv':
#             url = self.urlPostList[service] + postID
#             r = self.soupUrlRequest(url)
            
#             artists.append(r.select('.title')[4].string)

#             tagsHTML = r.select('.inline-list')

 
#             for instance in tagsHTML:
#                 # Don't open pixiv-encycopedia links
#                 if instance.find_all('img') == []:
#                     tags.append(instance.find_all('a')[1].string)
#             tags.append('tag_clean_request')


#         else:
#             print("Scraping " + service + "not currently supported" )
#             return None
#         return [copyrights, characters, artists, tags]

#     def formatTagList(self, tagList):
#         outList = []
#         for artist in tagList[2]:
#             outList.append('artist:' + artist)
#         for copyright in tagList[0]:
#             outList.append('copyright:' + copyright)
#         for character in tagList[1]:
#             outList.append('character:' + character)
#         for tag in tagList[3]:
#             outList.append(tag)
#         return outList

#     def scrapeIDfromAggregator(self, service, imageToFind):
#         # Scrape the image we are after off one of the aggregator sites
#         # I would like to supplement this with VAB_classify output

#         if service == 'iqdb':
#             # IQDB can take a URL or multi-part post image
#             # Only use the image post method as we have no reliable online storage at this step
            
#             print("Scraping IQDB")
#             postID          = 0
#             tagList         = []
#             fileToSend      = { 'file' : open(imageToFind,'rb')}
            
#             # Upload the image (this may take a while)
#             response = requests.post('http://iqdb.org/', files=fileToSend, proxies=self.proxies, auth=self.auth)
#             soup = BeautifulSoup(response.text)
            
#             if soup.find_all('table')[1].th.string == 'No relevant matches':
#                 # IQDB has failed us
#                 print("Image not found on any iqdb linkable site")
#                 return (0,[])
            
#             else:
#                 # IQDB has found a match
#                 result = soup.find_all('a')[1]
#                 if result['href'][7:15] == 'danbooru':
#                     print("IQDB search match on Dbu. ")
#                     postID = soup.find_all('a')[1]['href'][32:]
#                     print(postID)
#                     return (postID, 'Danbooru')
                
#                 elif result['href'][7:15] == 'gelbooru':
#                     print("IQDB search match on Gbu.")
#                     postID = soup.find_all('a')[1]['href'][50:]
#                     return (postID, 'Gelbooru')
                

        
#         elif service == 'sourcenao':
#             # sourceNAO takes 
            
#             print("Scraping sourceNAO")
#             postID =        0
#             tagList =       []
#             fileToSend =    { 'file' : open(imageToFind,'rb')}
#             tempURL =       None
            
#             response = requests.post('http://saucenao.com/search.php', files=fileToSend, proxies=self.proxies, auth=self.auth)
#             soup = BeautifulSoup(response.text)
            
#             # Unlike iqdb, sourcenao scrapes pixiv
#             # But if it returns a good danbooru result, we want to use that instead
#             # Even if the pixiv result is a better match
#             # This way we can use the tags from dbu rather than from pixiv
#             # SourceNAO shows characters and artist but that is all.
#             if 'Daily Search Limit Exceeded.' in soup.strong.string:
#                 print("sourceNAO search limit exceeded")
#                 return (-2,[])

#             try:
#                 if 'Low similarity' in soup.select('.result')[0].string:
#                     print("sourceNAO found nothing")
#                     return (-2,[])
#             except:
#                 pass
#             try:
#                 firstSourceLoc = soup.select('.result')[0].select('.linkify')[-2]['href']
#                 print("Image source is: " + firstSourceLoc)
#                 print(firstSourceLoc)
#             except:
#                 print('No result found')
#                 return (0,[])
#             if 'pixiv' in firstSourceLoc:
#                 # We want to try find some english tags if possible
#                 # So we'll check the second result for danbooru links
#                 # Lower than second and we can't guarentee correct results
#                 secondSource = soup.select('.result')[1]
#                 if not secondSource == None:
#                     if 'have been hidden' not in secondSource:
#                         # A result is worth checking for english tags!
#                         try:
#                             secondSourceLoc = secondSource.find_all('a')[1]['href']
#                             if 'danbooru' in secondSourceLoc:
#                                 # The second result contained a useful danbooru link. Lets use it
#                                 print("Roughly matching dbu source: " + secondSourceLoc)
#                                 postID = secondSourceLoc[36:]
#                         except:
#                             print('Only one source found')
#                 if postID == 0:
#                     # We need to look on pixiv
#                     postID = firstSourceLoc[61:]
#                     return (postID, 'Pixiv')

#             elif 'danbooru' in firstSourceLoc:
#                 pass
#                 # scrape the dbu resu
#                 # TODO

#             return (postID, 'Danbooru')

#         return (0,[])

#     def getPostIDfromMD5(self, service, imageMD5):
#         url = self.urlSearchList[service] + imageMD5
#         r = self.soupUrlRequest(url)
#         if not r == None:
#             # Some images exist as a direct link
#             # But have had their posts removed
#             res = r.article
#             if not res == None:
#                 return res['id'][5:]
#             else:
#                 print("Image exists but has no post.")
#         return 0

#     def directLinkExists(self, service, query, urlType):
#         url = ''
#         if urlType == 'post':
#             url = self.urlPostList[service] + str(query)
#         elif urlType == 'file':
#             url = self.urlDataList[service] + str(query)
#         print(url)
#         return self.soupUrlRequest(url) != None

#     def parseJSONResponse(self, response):
#         temp = response.contents[0]
#         temp = temp.encode(encoding='ascii',errors='replace')
#         try:
#             temp = json.load(temp.decode("utf-8"))#ast.literal_eval(temp)
#         except:
#             print("Exception parsing JSON. Retry with xml")
#             return 0
#         return temp

#     def parseJSONResponse2(self, url):
#         #print(response)
#         try:
#             results = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
#         except:
#             print("Http error. This file will need to be retried")
#             return 0
#         return results


#     def parseXMLResponse(self, response):
#         temp = response.contents[0]
#         try:
#             temp = xmltodict.parse(temp)#ast.literal_eval(temp)
#         except:
#             print("Exception parsing XML. Scraping from html directly")
#             return 0
#         return temp

#     def constructTags(self, metadata):
#         temp = {}
#         temp['id'] = metadata['id'] 
#         try:
#             temp['source'] = metadata['source'] 
#         except:
#             temp['source'] = 'http://danbooru.donmai.us/posts/' + temp['id']
#         temp['md5'] = metadata['md5'] 
#         temp['rating'] = metadata['rating'] 
#         temp['width'] = metadata['image_width'] 
#         temp['height'] = metadata['image_height'] 
#         #temp['tags'] = metadata['tag_string'] 
#         temp['extension'] = metadata['file_ext'] 
#         temp['pool'] = metadata['pool_string'] 
#         temp['file_size'] = metadata['file_size'] 
#         try:
#             temp['tag_string_artist'] = metadata['tag_string_artist'] 
#         except:
#             temp['tag_string_artist'] = ''
#         try:
#             temp['tag_string_character'] = metadata['tag_string_character'] 
#         except:
#             temp['tag_string_character'] = ''
#         try:
#             temp['tag_string_copyright'] = metadata['tag_string_copyright'] 
#         except:
#             temp['tag_string_copyright'] = ''
#         try:
#             temp['tag_string_general'] = metadata['tag_string_general'] 
#         except:
#             temp['tag_string_general'] = ''
#         temp['large_loc'] = 'http://danbooru.donmai.us/' + metadata['large_file_url'] 
#         temp['local_file'] = self.image
#         temp['tag_string'] = metadata['tag_string'] 
#         fin = self.image.rfind('\\')
#         target = self.image[:fin] + '\\' + metadata['md5'] + '.' + metadata['file_ext']
#         temp['target_file'] = target
#         if self.flag:
#             temp['flag'] = 1
#         else:
#             temp['flag'] = 0

#         if metadata['is_pending'] == True:
#             print("This file is yet to be approved on danbooru")
#             print("Hence, it will show as malformed and will be redownloaded, even if the file is fine")

#         return temp

#     def constructTags2(self, metadata, flag=0):
#         temp = {}
#         if metadata['lastrunstatus'] != 'success':
#             print("Kimono labs scrape broke")
#             return {}
#         metadata = metadata['results']
#         print(metadata['all_tags'][1])
        
#         temp['id'] = metadata['id'][0]['1']
#         try:
#             temp['source'] = metadata['source'][0]['1']['href']
#         except:
#             temp['source'] = 'http://danbooru.donmai.us/posts/' + temp['id']
#         temp['md5'] = self.md5
#         try:
#             print(metadata['rating'][0]['1'])
#             if metadata['rating'][0]['1'] == 'Safe':
#                 temp['rating'] = 's'
#             elif metadata['rating'][0]['1'] == 'Questionable':
#                 temp['rating'] = 'q'
#             else:
#                 temp['rating'] = 'e'
#         except:
#             temp['rating'] = 's'
#         try:
#             res = metadata['resolution'][0]['1']['text']
#             a = res.rfind('x')
#             x = int(res[a+1:])
#             y = int(res[:a])
#             temp['width'] = x
#             temp['height'] = y
#         except:
#             temp['width'] = 100
#             temp['height'] = 100
#         tags = ''
#         for item in metadata['tags']:
#             tags = tags + " " + item['1']['text']
#         temp['tag_string'] = tags
#         temp['extension'] = utl.fileExtension(self.image)
#         temp['pool'] = ''
#         temp['file_size'] = 0
#         tags = ''
#         try:
#             for item in metadata['artist']:
#                 tags = tags + " " + (item['1']['text'].replace(' ', '_'))
#             temp['tag_string_artist'] = tags 
#         except:
#             temp['tag_string_artist'] = ''
#         tags = ''
#         try:
#             for item in metadata['chcracters']:
#                 tags = tags + " " + (item['1']['text'].replace(' ', '_'))
#             temp['tag_string_character'] = tags
#         except:
#             temp['tag_string_character'] = ''
#         tags = ''
#         try:
#             for item in metadata['copyrights']:
#                 tags = tags + " " + (item['1']['text'].replace(' ', '_'))
#             temp['tag_string_copyright'] = tags
#         except: 
#             temp['tag_string_copyright'] = ''
#         tags = ''
#         for item in metadata['all_tags']:
#             tags = tags + " " + (item['1']['text'].replace(' ', '_')) 
#         temp['tag_string_general'] = tags 
#         temp['large_loc'] = 'http://danbooru.donmai.us/data/' + self.md5 + '.' + utl.fileExtension(self.image)
#         temp['local_file'] = self.image

#         target = temp['local_file']
#         temp['target_file'] = target
#         temp['flag'] = flag

#         #print(temp)
#         return temp


#     def goDbu(self):

#         # Simpler method.
#         # 
#         print('-----------------------------------------------')
#         dbu_md5FileNameMatch = self.directLinkExists('Danbooru', self.imageName, 'file')
#         if not dbu_md5FileNameMatch:
#             # We have failed to find using the generated md5
#             # Try again, with the md5 from the file name
#             #print('Generated md5 cannot find file')
#             a = self.image.rfind('\\')+1
#             b = self.image.rfind('.')
#             md5 = self.image[a:]
#             #print(md5)
#             dbu_md5FileNameMatch = self.directLinkExists('Danbooru', md5, 'file')
#             if dbu_md5FileNameMatch:
#                 #print('File name md5 finds file successfully. Updating known md5')
#                 a = md5.rfind('.')
#                 self.md5 = md5[:a]
#                 self.flag = True
        
#         if dbu_md5FileNameMatch:
#             # We have found an identical image on danbooru
#             #print('File exists on Dbu. Getting post ID')
#             postID = self.getPostIDfromMD5('Danbooru', self.md5)
#             if postID == 0:
#                 if "sample" in self.image:
#                     #print("Sample image found. Attempting to find original image")
#                     # We have the sample version of the image
#                     a = self.image.rfind('-')+1
#                     b = self.image.rfind('.')
#                     brutemd5 = self.image[a:b]
#                     postID = self.getPostIDfromMD5('Danbooru', brutemd5)
#                     if postID != 0:
#                         #print("Original post found. Updating.")
#                         self.md5 = brutemd5
#                 else:
#                     # We have the image, but named differently
#                     print("Shits gone wrong on: " + self.image)
#                     return 0

#             #print('Querying Dbu for tags')
#             #print(postID)
#             idurl   = 'http://danbooru.donmai.us/posts/' + postID + '.json'
#             idurl2  = 'http://danbooru.donmai.us/posts/' + postID + '.xml'
#             idurl3  = 'https://www.kimonolabs.com/api/34xtvd52?apikey=913520d0b372fd125c0c4bb579b73d11&kimpath2=' + postID


#             post_data = self.soupUrlRequest(idurl)
#             image_metadata = self.parseJSONResponse(post_data)
            
#             # Don't bother with the XML for now.
#             # if image_metadata == 0:
#             #     post_data = self.soupUrlRequest(idurl2)
#             #     image_metadata = self.parseXMLResponse(post_data)
            
#             if image_metadata == 0:
#                 # The page is being stubborn and won't load using danbooru's api
#                 # So, lets use an external one!
#                 image_metadata = self.parseJSONResponse2(idurl3)
#                 if image_metadata == 0:
#                     return 0
#                 result = self.constructTags2(image_metadata)
#             else:
#                 result = self.constructTags(image_metadata)
#             print('-----------------------------------------------')
#             if len(result) < 2:
#                 return 0 
#             return result
#         else:
#             print('Image not findable on danbooru')
#             return 0


#     def goScrape(self):

#         postID = 0
#         postID, service = self.scrapeIDfromAggregator('iqdb', self.image)

#         if postID == 0:
#             postID, service = self.scrapeIDfromAggregator('sourcenao', self.image)

#         if service == 'pixiv':
#             print('Image only found on pixiv')
#             return 0

#         if postID != 0 and service == 'Danbooru':
#             idurl3  = 'https://www.kimonolabs.com/api/34xtvd52?apikey=913520d0b372fd125c0c4bb579b73d11&kimpath2=' + postID
#             image_metadata = self.parseJSONResponse2(idurl3)
#             if image_metadata == 0:
#                 return 0
#             return self.constructTags2(image_metadata, 2)


#         # # We don't mind at this point if the image is already on vacbooru
#         # # As it may have new tags that get added by the current user

#         # fileToTest =    self.md5 + utl.fileExtension(self.image)
#         # onDbu =         self.directLinkExists('Danbooru', fileToTest, 'file')
#         # postID =        0
#         # service =       None
#         # tagList =       []
        
#         # if onDbu:
#         #     # The image exists on dbu with an identical md5 hash
#         #     print("Scraping Dbu")
#         #     postID = self.getPostIDfromMD5('Danbooru', self.md5)

#         #     # Some images exist viw direct link but have had their posts removed
#         #     # This normally means the image is flagged for deletion but is not yet removed 
#         #     if not self.directLinkExists('Danbooru', postID, 'post'):
#         #         postID = 0
#         #     else:
#         #         service = 'Danbooru'
        
#         # if postID == 0:
#         #     # Either the image isn't on Dbu, or it is but the post is deleted so we can't get the tags
#         #     # So instead, find the image off a scraping service
#         #     # Two services are supported: sourceNAO and IQDB
#         #     #   IQDB puts the user in a queue if under high load
#         #     #   sourceNAO has a limit of 100 uploads per day for a non-user
#         #     # Differing user browsing habits will benifit choosing one site over the other
#         #     #   game cgs or risque -    iqdb
#         #     #   pixiv or quality -      sourceNAO     
            
#         #     if self.scrapeTarget == 'iqdb':
#         #         postID, service = self.scrapeIDfromAggregator('iqdb', self.image)
            
#         #     if postID == 0:
#         #         # The scrape target is sourceNAO or IQDB scrape failed
#         #         postID, service = self.scrapeIDfromAggregator('sourcenao', self.image)
                
#         # # A > 0 postID means a taglist was found
#         # # 0 means no post was found
#         # # -1 means a post was found but no tags were (this shouldn't ever occur normally)
#         # # -2 means sourceNAO or IQDB returned an unhelpful page like upload limit exceeded
#         # if int(postID) <= 0:
#         #     print("Tag retrieval unsuccessful")
#         # else:
#         #     tagList = self.getTagList(service, postID)  
#         #     tagList = self.formatTagList(tagList)
#         #     for tag in tagList:
#         #         tag.replace(' ', '_')
#         #     return(tagList)
#         # return 0



#     def fun(self):
#         # Fun might go here        
#         pass

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description="Don't run this file by itself. Use VAB_wrapper instead")
