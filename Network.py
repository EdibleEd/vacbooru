from bs4 import BeautifulSoup
import requests
import json
from requests.auth import HTTPBasicAuth
from tld import get_tld
import traceback


class Network:
    def __init__(self, proxyConfig=None):
        # Totally ignoring proxies for now.
        # But heres the boilerplate for them
        self.proxyUser  = ''
        self.proxyPass  = ''
        self.proxyAddr  = ''
        self.proxyPort  = ''
        self.useProxy   = ''

        self.siteAuth   = {} #        'donmai.us'          :  {user : '', api_token : ''}


    def setupAuth(self, site, siteConfig):
        self.siteAuth.update({site: siteConfig})
        #print(self.siteAuth)
        return 1

    def urlRequest(self, url, target):
        if 'anubis' not in url:
            tld = get_tld(url)
        else:
            tld = 'anubis'

        if tld in self.siteAuth.keys():
            user = self.siteAuth[tld]['user']
            pwd  = self.siteAuth[tld]['api_token']

            r = requests.get(url, auth=HTTPBasicAuth(user, pwd))
        else:
            r = requests.get(url)

        #header  = r.headers
        status  = r.status_code

        if target == 'json':
            content = r.json()
        else:
            content = r.text

        #print(content)
        return (status, content)

    def htmlEncode(self, data):
        try:
            data = data.encode('utf-8')
            return BeautifulSoup(data, "html5lib")
        except:
            traceback.print_exc()
            print('HTML encoding error. Skipping file')
            return 0
