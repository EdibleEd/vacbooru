import abc

class AbstractScraper(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def init(self, input):
        """Setup the scraper"""
        return
    
    @abc.abstractmethod
    def postExists(self, postID):
        """Returns whether a given postID results in a valid post"""
        return

    @abc.abstractmethod
    def generateRawData(self, postID):
    	"""Given a postID, get the html/json/xml text containing the data we want"""
    	return

 	@abc.abstractmethod
    def extractPostInfo(self, rawData):
    	"""Given raw html/json/xml, generate all data for the post"""
    	return