import abc
import Utility as utl
from Network import Network

from AbstractScraper import AbstractScraper

class DanbooruScraper(AbstractScraper):
    
    def __init__(self, config, network):
        self.searchForMD5 	= 'http://danbooru.donmai.us/posts?utf8=%E2%9C%93&tags=md5%3A'
        self.urlPostBase    = 'http://danbooru.donmai.us/posts/'
        self.urlDataBase    = 'http://danbooru.donmai.us/data/'
        
        self.network        = network
        self.network.setupAuth('donmai.us', config)
        self.localFile = ''

    def setLocalFile(self, target):
    	self.localFile = target

    def findPostByMD5(self, md5):
        """Given an MD5, return the postID. May not be implemented, depending on the service"""
        url = self.searchForMD5 + md5
        response, data =  self.network.urlRequest(url, 'html')
        if response == 200:
            data = self.network.htmlEncode(data)
            try:
            	postID = data.article['id'][5:]
            	return postID
            except:
            	print('Error finding postID for MD5: ' + md5)
        return 0

    def postExists(self, postID):
        url = self.urlPostBase + str(postID)
        response, data = self.network.urlRequest(url, 'html')
        if response == 200:
            return True
        else:
            return False

    def generateRawData(self, postID):
        """Given a postID, get the html/json/xml text containing the data we want"""
        url = self.urlPostBase + postID + '.json'

        response, raw_data     = self.network.urlRequest(url, 'json')
        #clean_data     = self.network.urlEncode(raw_data) 
        
        return raw_data

    def extractPostInfo(self, rawData):
        """Given raw html/json/xml, generate all data for the post"""
        temp = {}
        temp['id'] = rawData['id'] 
        try:
            temp['source'] = rawData['source'] 
        except:
            temp['source'] = 'http://danbooru.donmai.us/posts/' + temp['id']
        temp['md5'] = rawData['md5'] 
        temp['rating'] = rawData['rating'] 
        temp['width'] = rawData['image_width'] 
        temp['height'] = rawData['image_height'] 
        #temp['tags'] = rawData['tag_string'] 
        temp['extension'] = rawData['file_ext'] 
        temp['pool'] = rawData['pool_string'] 
        temp['file_size'] = rawData['file_size'] 
        try:
            temp['tag_string_artist'] = rawData['tag_string_artist'] 
        except:
            temp['tag_string_artist'] = ''
        try:
            temp['tag_string_character'] = rawData['tag_string_character'] 
        except:
            temp['tag_string_character'] = ''
        try:
            temp['tag_string_copyright'] = rawData['tag_string_copyright'] 
        except:
            temp['tag_string_copyright'] = ''
        try:
            temp['tag_string_general'] = rawData['tag_string_general'] 
        except:
            temp['tag_string_general'] = ''
        temp['large_loc'] = 'http://danbooru.donmai.us/' + rawData['large_file_url'] 
        temp['local_file'] = self.localFile
        temp['tag_string'] = rawData['tag_string'] 
        #fin = self.image.rfind('\\')
        target = 'another temp line' #self.image[:fin] + '\\' + rawData['md5'] + '.' + rawData['file_ext']
        temp['target_file'] = target
        # if self.flag:
        #     temp['flag'] = 1
        # else:
        #     temp['flag'] = 0

        if rawData['is_pending'] == True:
            print("This file is yet to be approved on danbooru")
            print("Hence, it will show as malformed and will be redownloaded, even if the file is fine")

        return temp
