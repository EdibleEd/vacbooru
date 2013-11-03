import argparse
import re
import os

#import Utility

# inlining utility here for py2/3 issues
# Prints if the level of debug printing is greater or equal to this methods threshold to be printed
# typically 0 = never, 1 = standard running, 2-5 = various debug levels
def debugPrint(message, level, threshold):
	if (level >= threshold):
		print(message)

# TAKES a directory path
# OPTIONALLY TAKES a regex OR a flag indicating standard danbooru format, a flag indicating not just image files
# RETURNS a list of image file paths

# Takes a folder and returns any files that fit the danbooru standard formats, all image files or all files that fit a regex depending on flags provided

class VAB_loadfolder:
    def __init__(self):
        self.image_extensions = ["jpg","png","gif"]
        self.debug_level = 5
        
    # Gets the file list
    def loadFiles(self, path, regex, isdanbooru, isall):
        
        path_to_file = os.path.join(os.getcwd(), path)     
        rel_path = True
        output_list = []
        if not(os.access(os.path.join(os.getcwd(), path), os.R_OK)):
            if os.access(path, os.R_OK):       
                path_to_file = path
            else:
                debugPrint("Folder not found " + path, debug_level, 2)

        for root, dirs, files in os.walk(path_to_file):
            for name in files:
                if regex:
                    if self.cullRegex(name, regex):
                        output_list.append(os.path.join(root, name))            

                elif isdanbooru:
                    if self.cullDanbooru(name):
                        output_list.append(os.path.join(root, name))

                elif isall:
                    output_list.append(os.path.join(root, name))

                else:
                    if self.cullNonImage(os.path.join(root, name)):
                        output_list.append(os.path.join(root, name))

        return(output_list)
            
    # Cull file based on regex
    def cullRegex(self, data, regex):
        reg = re.compile(regex)
        return (re.match(data, reg) != None)

    # Cull file to only danbooru style filenames
    def cullDanbooru(self, data):
        
        # Treat sample DBU files as regular files    
        data = data.strip("sample-")
        
        # Danbooru images are 32 hex characters, then an image extension
        reg = re.compile("[0-9a-f]{32}")
        if (len(data.split('.')[0]) != 32):
            return False
        return ((data.split('.')[1] in set(self.image_extensions)) and ((re.match(data.split('.')[0],reg) != None)))

    # Cull non image files (by extension)
    def cullNonImage(self, data):
        return ((data.split('.')[1] in set(self.image_extensions)))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Recursively load a folder of images')
	parser.add_argument("path", help="folder to use as a source of images")
	parser.add_argument('--regex', '-r',action="store_true", help="optionally supply a regex and only load files that fit it")
	parser.add_argument('-d',  help="only load images that fit the danbooru naming scheme")
	parser.add_argument('--all', '-a', help="load any file not just one that fits known image file extensions")
	args = parser.parse_args()
	loader = VAB_loadfolder()
    print(loader.loadFiles(args.path, args.regex, args.d, args.all))

