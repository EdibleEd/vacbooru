import Utility
import bs4
import requests

def makeTuple(single_tag):
    height = int(single_tag["data-height"])
    width = int(single_tag["data-width"])
    data = str(single_tag.contents[0])
    id = int(single_tag["data-id"])
    xpos = int(single_tag["data-x"])
    ypos = int(single_tag["data-y"])
    return (id, data, xpos, ypos, width, height)
    
ex1 = 'http://danbooru.donmai.us/posts/1543230'
ex2html = 'http://danbooru.donmai.us/posts/1543519'
r = requests.get(ex2html)
dr =  bs4.BeautifulSoup(r.text)
dp = dr.body.find(id="notes")
translations = []

for i in dp:
	if (str(i).strip() != ""):
		translations.append(makeTuple(i))

for i in translations:
    print(i)