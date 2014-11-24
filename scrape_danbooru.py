import abc
from abc_base import AbstractScraper

class DanbooruScraper(AbstractScraper):
    
    def init(self, input):
        """Setup the scraper"""
        return
    
    def postExists(self, postID):
        """Returns whether a given postID results in a valid post"""
        return

    def generateRawData(self, postID):
    	"""Given a postID, get the html/json/xml text containing the data we want"""
    	return

    def extractPostInfo(self, rawData):
    	"""Given raw html/json/xml, generate all data for the post"""
    	return