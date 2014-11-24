from VAB_QC import VAB_QC
from VAB_scraper import VAB_scraper
from VAB_upload import VAB_upload
import Utility
from VAB_loadfolder import VAB_loadfolder
import os
import argparse

# Wrapper class that runs the whole shabang
# Will take data from a bunch of configs primarily

class VAB_wrapper:
    
    def __init__(self, args):
        
        self.folderToLoad = args.path
        self.mainConf = Utility.loadConfig('config/main.cfg')
          
                
    def loadFolder(self, config):
        loader = VAB_loadfolder()
        if (config['image_extensions']):
            loader.setImageExtensions(config['image_extensions'])
        return loader.loadFiles(config['path'], config['mode'], config['regex'], config['danbooru_mode'], config['tumblr_qual'])

    def scrapeTags(self, files, config, network_config, dbu_config):
        scraper = VAB_scraper(config['perv_mode'], config['scrape_target'], network_config, dbu_config)
        # Need error checking here
        results = []
        for image in files:
            scraper.setFile(image)
            tagList = scraper.goDbu()
            if tagList == 0:
                tagList = scraper.goScrape()
            if tagList != 0 and tagList != None:
                results.append(tagList)
            else:
                print ("Image " + image + " ignored")

        return results

    def QC(self, data, config):
        qc = VAB_QC(config)

        results = []
        for tagset in data:
            cleaned_tagset = qc.clean(tagset)
            results.append(tagset)

        return results

    def upload(self, files, config):
        uploader = VAB_upload(config)

        for upload_target in files:
            uploader.go(upload_target)

    def chain(self):
    
        # Load configs
        folder_config   = self.mainConf['Folder']
        folder_config['path'] = self.folderToLoad
        
        scraper_config  = self.mainConf['Scraper']
        qc_config       = self.mainConf['QC']
        upload_config   = self.mainConf['Upload']
        network_config  = self.mainConf['Network']
        dbu_config      = self.mainConf['SiteAccess']

        # Get the file list that we are going to work with
        files = self.loadFolder(folder_config)
        for image in files:
            tagged_file = self.scrapeTags([image], scraper_config, network_config, dbu_config)
            qc_file = self.QC(tagged_file, upload_config)
            self.upload(qc_file, upload_config)   
        #tagged_files = self.scrapeTags(files, scraper_config, network_config, dbu_config)

        #qc_files = self.QC(tagged_files, upload_config)

        #self.upload(qc_files, upload_config)        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import and upload a folder of images to vacbooru')
    parser.add_argument("path", help="Path to folder to load")
    wrap = VAB_wrapper(parser.parse_args())
    wrap.chain()
