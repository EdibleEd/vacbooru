# A series of quality checking steps
# All do not alter the format of the data
# Steps projected are as follows:
# 1. Check if file is already uploaded
# 2. Cull file if it has certain tags
# 3. add user to tags
# 4. Add or remove existing tags
# 5. verify checksum is sane

from PIL import Image
import shutil
import requests
import os
from bs4 import BeautifulSoup

class VAB_QC:

    def __init__(self, config, network):
        self.bannedTags         = []
        self.questionableTags   = ['nude']
        self.explicitTags       = ['sex']
        self.proxies = None
        self.auth = None
        self.network = network

    def getPostIDfromMD5(self, imageMD5):
        url = 'http://anubis/posts?utf8=%E2%9C%93&tags=md5%3A' + imageMD5
        response, data =  self.network.urlRequest(url, 'html')
        if response == 200:
            try:
                postID = data.article['id'][5:]
                return 1
            except:
                print('Image not uploaded yet')
                return 0
        return 1



    def fileCheck(self, tagset):

        image = Image.open(tagset['local_file'])
        x = image.size[0]
        y = image.size[1]
        size = os.path.getsize(tagset['local_file'])
        image.close()

        print(tagset['local_file'], x, tagset['width'], y, tagset['height'], size, tagset['file_size'])
        print(tagset['rating'])
        if (x < tagset['width'] or y < tagset ['height']) and (size != int(tagset['file_size'])) and(tagset['width'] > 0 and tagset['height'] > 0):
            # The copy we have is smaller than the one hosted on dbu
            # We want to delete this image, and download the higher res version
            print('Local file ' + tagset['local_file'] + ' does not correctly match target. Moving old file')
            #os.remove(tagset['local_file'])
            
            a = tagset['local_file'].rfind('\\')
            newDir = tagset['local_file'][:a] + '\\vab_replacedfiles'
            try:
                if not os.path.exists(newDir):
                    os.makedirs(newDir)
                print(tagset['local_file'])
                print(newDir + '\\' + tagset['local_file'][a+1:])
                os.rename(tagset['local_file'], newDir + '\\' + tagset['local_file'][a+1:])
            except:
                print('Moving old file failed')

            print('Downloading larger file')
            url =       tagset['large_loc']
            target =    tagset['local_file']
            response = requests.get(url, stream=True)
            with open(target, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            os.rename(tagset['local_file'], tagset['target_file'])
            print('Download of ' + url + ' complete')
            tagset['local_file'] = tagset['target_file']
        return 1

    def tagCheck(self, tagset):

        if len(tagset['tag_string']) < 2:
            return 0
        for tag in self.bannedTags:
            for applied_tag in tagset['tag_string'].split(' '):
                if tag == applied_tag:
                    return 0

        temp = tagset['tag_string_general']
        # Merge the tags for the dbu format
        for tag in tagset['tag_string_artist'].split(' '):
            if len(tag) > 1:
                temp = temp + " artist:" + tag
        for tag in tagset['tag_string_character'].split(' '):
            if len(tag) > 1:
                temp = temp + " character:" + tag
        for tag in tagset['tag_string_copyright'].split(' '):
            if len(tag) > 1:
                temp = temp + " copyright:" + tag

        tagList = temp.split(' ')
        for i in range(0,len(tagList)):
            if 'users入り' in tagList[i]:
                tagList[i] = ''

        temp = ' '.join(tagList)

        print(temp)

        tagset['tag_string'] = temp

        return tagset    

    def safeCheck(self, tagset):
        res = 1
        if tagset['rating'] == 's':
            for tag in self.questionableTags:
                for applied_tag in tagset['tag_string'].split(' '):
                    if tag == applied_tag:
                        tagset['rating'] == 'q'
                        res = 2
        if tagset['rating'] == 'q':
            for tag in self.explicitTags:
                for applied_tag in tagset['tag_string'].split(' '):
                    if tag == applied_tag:
                        tagset['rating'] == 'e'
                        res = 3
        return res

    def uploadCheck(self, tagset):
        if self.getPostIDfromMD5(tagset['md5']) == 0:
            # The image does not exist. We can look at uploading it
            return 1
        else:
            return 0

    def clean(self, tagset):

        if self.safeCheck(tagset) != 1:
            print("File rating modified")

        tagset = self.tagCheck(tagset)
        #print(tagset)
        if tagset == 0:
            print("Modifying tags failed.")
            return 0
        elif self.fileCheck(tagset) != 1:
            print("File checking failed.")
        elif self.uploadCheck(tagset) != 1:
            print("Image already uploaded. Ignoring")
        else:
            return tagset
        #Failure case
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean-up a image tagset. Do not run this file directly: use VAB_wrapper instead')
    args = parser.parse_args()
    QC(args)
#     def __init__(self, data, tags):
#         self.unique_tag_prefixes = set["r::","s::","x::","y::"]
#         this.data = data
#         # if in interactive mode, prompt the user to perform actions
#         if(args.interactive):
#             mainLoop(args)
                    
#         # Otherwise perform all automated tasks specified
#         else:
#             pass
            
#     # Interactive quality checking
#     def mainLoop(self, args):
#         mainloop = True
#         while (mainloop):
#             pass 
            
#     # Cull a file if it has any of a specific set of tags
#     def cullIfTags(self, data, to_remove):
#         for item in data:
#             for tag in to_remove:
#                 if tag in item:
#                     data.remove(item)

#     # Cull a set of tags from every image, naive version
#     def cullSpecificTags(self, data, to_remove):
#         for item in data:
#             for tag in to_remove:
#                 if tag in data[3]:
#                     data[3].remove(tag)

#     # Add a set of non control tags to each image
#     def addTags(self, data, new_tags):
#         for item in data:
#             for tag in new_tags:
#                 if (tag not in set(item[3])):
#                     item[3].append(tag)
#                     new_tags.remove(tag)

#     # Add some control tags while never allowing two of some tags
#     def addControlTags(self, data, new_tags):
#         for item in data:
#             for tag in new_tags:
#                 if (tag[0:2] in unique_tag_prefixes):
#                     for old_tag in data[3]:
#                         if (tag[0:2] == old_tag[0:2]):
#                             data.remove(old_tag)
#                         data.append(tag)
#                         new_tags.remove(tag)
#                 else:
#                     data.append(tag)
#                     new_tags.remove(tag)

#     # Interactively add tags to data
#     def interactiveEdit(self, data):
#         running = True  
#         print ("Enter command, Exit to stop altering data.")        
#         while (Running):
            
#             command = input("> ")
#             running = self.evaluateCommand(data, command)


#     def evaluateCommand(self, tags, command, args):
    
#         # Clean up data      
#         command = command.strip().lower()
#         command_options = {"print": printTags, "exit":exit, "remove":removeTags, "replace":replaceTags}
#         return command_options[command](tags, args)
    
#     def exit(self,tags,args):
#         return 0
        
#     def printTags(self, tags, args):
#         print ("Current tags are: " + formatPrint(tags))
#         return 1
        
#     def removeTags(self, tags, args):

#         return 1

#     def replaceTags(self, tags, new_mappings):
#         for item in tags:         
#             if item in new_mappings.getKeys():
#                 item = new_mappings[item]
        
        
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Cull an image list')
#     parser.add_argument('tags', metavar='N', nargs='+', help='A single tag list for the program')
#     parser.add_argument('-i', '-interactive',type=bool, help="Set if running in interactive mode")
#     args = parser.parse_args()
#     QC(args)
