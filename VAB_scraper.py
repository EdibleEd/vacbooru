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
            #postID = 0
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
