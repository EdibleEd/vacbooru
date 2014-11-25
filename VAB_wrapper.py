from VAB_QC import VAB_QC
from VAB_scraper import VAB_scraper
from VAB_upload import VAB_upload
import Utility
from VAB_loadfolder import VAB_loadfolder
import os
import argparse
from Network import Network
import json

# Wrapper class that runs the whole shabang
# Will take data from a bunch of configs primarily

class VAB_wrapper:
    
    def __init__(self, args):
        
        self.folderToLoad   = args.path
        self.mainConf       = Utility.loadConfig('config/main.cfg')
        self.network        = Network('a')
          
                
    def loadFolder(self, config):
        loader = VAB_loadfolder()
        if (config['image_extensions']):
            loader.setImageExtensions(config['image_extensions'])
        return loader.loadFiles(config['path'], config['mode'], config['regex'], config['danbooru_mode'], config['tumblr_qual'])

    def scrapeTags(self, target, config, network_config, dbu_config, pxv_config):
        auth = {'donmai.us' : {'user': dbu_config['username'], 'api_token' : dbu_config['api_token']},
                'pixiv.net' : {'username': pxv_config['username'], 'password' : pxv_config['password']}}
        y = VAB_scraper(False, auth, self.network)
        y.setupTarget(target[0], ['pixiv.net', 'donmai.us'])
        tags = y.scrape()

        # try:
        #     print(tags)
        # except:
        #     print("Encoding error. Printing utf-8 version")
        #     print(json.dumps(tags, ensure_ascii=False).encode('utf8'))
        return tags

    def QC(self, data, config):
        qc = VAB_QC(config, self.network)

        cleaned_tagset = qc.clean(data)
        return cleaned_tagset

    def upload(self, target, config):
        uploader = VAB_upload(config)

        uploader.go(target)

    def chain(self):
    
        # Load configs
        folder_config   = self.mainConf['Folder']
        folder_config['path'] = self.folderToLoad
        
        scraper_config  = self.mainConf['Scraper']
        qc_config       = self.mainConf['QC']
        upload_config   = self.mainConf['Upload']
        network_config  = self.mainConf['Network']
        dbu_config      = self.mainConf['SiteAccess']
        pxv_config      = self.mainConf['pixiv']

        # Get the file list that we are going to work with
        files = self.loadFolder(folder_config)
        for image in files:
            tagged_file = self.scrapeTags([image], scraper_config, network_config, dbu_config, pxv_config)
            if tagged_file == 0:
                print('File info not found. Ignoring: ' + image)
            # else:
                # qc_file = self.QC(tagged_file, upload_config)
                # if qc_file !=0:
                #      self.upload(qc_file, upload_config) 
                # else:
                #     print('File ' + image + ' failed QC')  



        #tagged_files = self.scrapeTags(files, scraper_config, network_config, dbu_config)

        #qc_files = self.QC(tagged_files, upload_config)

        #self.upload(qc_files, upload_config)        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import and upload a folder of images to vacbooru')
    parser.add_argument("path", help="Path to folder to load")
    wrap = VAB_wrapper(parser.parse_args())
    wrap.chain()
