import argparse
import re

# TAKES a directory path
# OPTIONALLY TAKES a regex OR a flag indicating standard danbooru format, a flag indicating not just image files
# RETURNS a list of image file paths

# Takes a folder and returns all files that fit either the danbooru standard format, all image files, or all files that fit a regex depending on flags provided

class VAB_loadfolder:

    image_extensions = []
	debugLevel = 5
	
	def __init__(self):
		pass
    
    # Gets the file list
    def loadFiles(self, path):
        path_to_file = ""        
        rel_path = True       
        output_list = []        
        if os.access(os.path.join(os.getcwd(), args.path), os.R_OK):
            path_to_file = os.path.join(os.getcwd(), path)
        
        elif os.access(path, os.R_OK):       
            path_to_file = args.path
        else:
            debugPrint("Folder not found " + path, debugLevel, 2):

        for root, dirs, files in os.walk(path_to_file):
            for name in files:
                if args.regex:
                    output_list.append(cullRegex(os.path.join(root, name), args.regex))            

                elif args.d:
                    output_list.append(cullDanbooru(os.path.join(root, name)))

                elif args.all:
                    output_list.append(os.path.join(root, name))

                else:
                    output_list.append(cullNonImage(os.path.join(root, name)))

        print(output_list)
            
    # Cull file based on regex
    def cullRegex(self, data, regex):
        return (re.match(data, regex) != None)

    # Cull file to only danbooru style filenames
    def cullDanbooru(self, data):
        return (([data.split('.')[1] in image_extensions) && ((re.match(data.split('.')[0],"[0-9a-f]{64}") != None)))

    # Cull non image files (by extension)
    def cullNonImage(self, data):
        return (([data.split('.')[1] in image_extensions))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Recursively load a folder of images')
	parser.add_argument("path", help="folder to use as a source of images")
	parser.add_argument('--regex', '-r',action="store_true", help="optionally supply a regex and only load files that fit it")
	parser.add_argument('-d',  help="only load images that fit the danbooru naming scheme")
	parser.add_argument('--all', '-a', help="load any file not just one that fits known image file extensions")
	args = parser.parse_args()
	VAB_loadFolder(args)

