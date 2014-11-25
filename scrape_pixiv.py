import abc
import Utility as utl
from Network import Network
import requests
import csv

from AbstractScraper import AbstractScraper

class PixivScraper(AbstractScraper):
    
    def __init__(self, config, network):  
        self.urlPostBase = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id='
        self.network        = network
        #self.network.setupAuth('donmai.us', config)
        self.localFile = ''

        self.headers = {
            'Referer': 'http://spapi.pixiv.net/',
            'User-Agent': 'PixivIOSApp/5.1.1',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        url = 'https://oauth.secure.pixiv.net/auth/token'

        data = {
            'username': 'aronyan',
            'password': 'suzumiya13',
            'grant_type': 'password',
            'client_id': 'bYGKuGVw91e0NMfPGp44euvGt59s',
            'client_secret': 'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK',
        }

        r = requests.post(url, headers=self.headers, data=data)
        if (not r.status_code in [200, 301, 302]):
            print('Error logging into pixiv!')

        token = None
        try:
            # get access_token
            token = r.json()
            
            self.access_token = token['response']['access_token']
            self.user_id = token['response']['user']['id']
            #print("AccessToken:", self.access_token)

        except:
            print('Get access_token error! Response: %s' % (token))

        try:
            # get PHPSESSID
            raw_cookie = r.headers.get('Set-Cookie')
            for cookie_str in raw_cookie.split('; '):
                if 'PHPSESSID=' in cookie_str:
                    self.session = cookie_str.split('=')[1]
            #print("Session:", self.session)

        except:
            print('Get PHPSESSID error! Set-Cookie: %s')

        # return auth/token response
        self.token = token

        self.authHeaders = {
            'Authorization': 'Bearer %s' % self.access_token,
            'Cookie': 'PHPSESSID=%s' % self.session,
        }


    def setLocalFile(self, target):
    	self.localFile = target

    def findPostByFileName(self, filename):
        partName = utl.fileName(filename)

        header = {
            'User-Agent': 'pixiv-ios-app(ver4.0.0)'
        }
        params = {
            'illust_id': partName,
        }

        url = 'http://spapi.pixiv.net/iphone/illust.php'
        r = requests.get(url, headers=header, params=params)
        #print(int(partName))
        if r.status_code == 200 and partName in r.text:
            return partName
        return 0

    def findPostByMD5(self, filename):
        return 0

    def postExists(self, postID):
        url = self.urlPostBase + str(postID)
        response, data = self.network.urlRequest(url, 'html')
        if response == 200:
            return True
        else:
            return False
       
    def generateRawData(self, postID):
        header = {
            'User-Agent': 'pixiv-ios-app(ver4.0.0)'
        }
        params = {
            'illust_id': postID,
        }

        url = 'http://spapi.pixiv.net/iphone/illust.php'
        r = requests.get(url, headers=header, params=params)
        try:
            if r.status_code == 200 and postID in r.text:
                # Here is the data.
                return r.text
        except:
            return 0
        return 0

    def extractPostInfo(self, rawData):
        res = []
        for row in csv.reader(rawData):
            if len(row) > 0:
                res.append(row[0])

        print(res)


        temp = {}
        temp['id'] = res[0]
        temp['extension'] = res[4]
        temp['title'] = res[6]
        temp['tag_string_artist_japanese'] = res[10] 
        temp['tag_string_artist'] = res[41]
        if len(temp['tag_string_artist']) < 2:
            temp['tag_string_artist'] = temp['tag_string_artist_japanese']
        temp['source'] = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + temp['id']
        temp['md5'] = utl.md5(self.localFile)
        temp['tag_string_general'] = res[22]
        temp['tag_string'] = res[22]
        temp['description'] = res[32]

        # These three values are not given.
        # So, set them to -1 to indicate we don't want QC to care
        temp['width'] = -1
        temp['height'] = -1 

        temp['file_size'] = -1 

        temp['large_loc'] = res[16]
        temp['local_file'] = self.localFile


        return temp


# x = Network('a')

# y = PixivScraper('b', x)
# y.setLocalFile('J:\\pictures\\_culled\\temp\\24382481.jpg')
# zz = y.findPostByFileName('J:\\pictures\\_culled\\touhou\\24382481.jpg')
# print(zz)
# z = y.generateRawData(zz)
# a = y.extractPostInfo(z)

# print(a)

