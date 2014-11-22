# A series of quality checking steps
# All do not alter the format of the data
# Steps projected are as follows:
# 1. Check if file is already uploaded
# 2. Cull file if it has certain tags
# 3. add user to tags
# 4. Add or remove existing tags
# 5. verify checksum is sane

class VAB_QC:



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
