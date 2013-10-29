import VAB_QC
import VAB_scraper
import VAB_upload
import utility
import VAB_loadfolder
import os
import argparse

# Wrapper class that runs the whole shabang
# Will take data from a bunch of configs primarily

class VAB_wrapper:

    def __init__(self, args):
        if (args.config == None):
            with open(os.path.join(os.getcwd(), "Config", "main.conf"), 'r', encoding='utf-8') as mainConfig:
                mainConf = loadSimpleConfig(config)
        else:
            with open(args.config), 'r', encoding='utf-8') as mainConfig:
                mainConf = loadSimpleConfig(config)

    def loadFolder(self, config):
        pass

    def scraperCall(self, config):
        pass

    def QC(self, config):
        pass

    def upload(self, config):
        pass

    def chain(self):
        
        # Load configs      
        with open(os.path.join(os.getcwd(), "Config", mainConf["folder"]), 'r', encoding='utf-8') as folder_conf:
            folder_config = loadSimpleConfig(f)
    
        with open(os.path.join(os.getcwd(), "Config", mainConf["scraper"]), 'r', encoding='utf-8') as scraper_conf:
            scraper_config = loadSimpleConfig(f)

        with open(os.path.join(os.getcwd(), "Config", mainConf["qc"]), 'r', encoding='utf-8') as QC_conf:
            qc_config = loadSimpleConfig(f)

        with open(os.path.join(os.getcwd(), "Config", mainConf["upload"]), 'r', encoding='utf-8') as upload_conf:
            upload_config = loadSimpleConfig(f)
        
        loadFolder(folder_config)
        

        scraperCall(scraper_config)


        QC(QC_config)


        upload(upload_config)        

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Import and upload a folder of images to vacbooru')
	parser.add_argument("config", help="Path to configuration script")
    wrap = VAB_wrapper()
    wrap.chain()
    
