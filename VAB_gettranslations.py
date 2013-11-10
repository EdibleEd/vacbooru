import Utility
import bs4
import requests

# Gets any floating translation boxes from a danbooru page
#
# Example URLs to use:
# 'http://danbooru.donmai.us/posts/1543230' Tags
# 'http://danbooru.donmai.us/posts/1543519' Tags and html in contents
# 'http://danbooru.donmai.us/posts/15438541543854' no tags

class GetTranslations:

    def __init__(self):
        pass
    
    def getTagsFromID(self, id):
        return self.getTagsFromUrl("http://danbooru.donmai.us/posts/" + str(id))
        
    # Takes a page URL, returns the tags
    # Gives a 6-tuple
    # ID, the actual image, xposition, yposition, width, height
    
    def getTagsFromUrl(self, url):
        full_page = requests.get(url)
        soup_page =  bs4.BeautifulSoup(full_page.text)
        notes_section = soup_page.body.find(id="notes")
        
        # If no tags, return none.
        if (notes_section == None):
            return None
            
        translations = []
        for single_note in notes_section:
            if (str(single_note).strip() != ""):
                translations.append(self.makeTuple(single_note))
        
        return translations
        
    def makeTuple(self, single_tag):
        height = int(single_tag["data-height"])
        width = int(single_tag["data-width"])
        data = str(single_tag.contents[0])
        id = int(single_tag["data-id"])
        xpos = int(single_tag["data-x"])
        ypos = int(single_tag["data-y"])
        return (id, data, xpos, ypos, width, height)
