# TAKES a list of tupples of the form
# {source_url, source_hash, image_extension [tags]}
# RETURNS a set of tupples of the form
# {source_url, source_hash, image_extension [tags]}
# Control tasgs are prefixed with <letter>:: and are
#
# a::   Artist
# p::   Copyright
# c::   Characters
# r::   Rating
# s::   Origional Source
# v::   Username to upload under
# x::   Resolution, x axis
# y::   Resolution, y axis

# A series of quality checking steps
# All do not alter the format of the data
# Steps projected are as follows:
# 1. Check if file is already uploaded
# 2. Cull file if it has certain tags
# 3. add user to tags
# 4. Add or remove existing tags
# 5. verify checksum is sane

class VAB_QC:

	def __init__(self, data, tags):
        
        this.data = data
		# if in interactive mode, prompt the user to perform actions
		if(args.interactive):
			mainLoop(args)
        			
		# Otherwise perform all automated tasks specified
		else:
			pass
			
	# Interactive quality checking
	def mainLoop(self, args):
        mainloop = True
        while (mainloop):
            pass	
    
	
	# Cull a set of tags from the data
	def cullTags(self, toremove):
        pass

	# Add a set of tags to each image
	def addTags(self, newtags):
        pass
		
	# Add a user tag to each image
	def addUser(self, data, user):
		pass    
	
	# Interactively add tags to data
	def editTags(self, data):
		pass
		
	# Verify that the data has a correctly calculated checksum
	def verifyChecksum(self, data):
		pass
		
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Cull an image list')
	parser.add_argument('tags', metavar='N', nargs='+', help='A single tag list for the program')
	parser.add_argument('-i', '-interactive',type=bool help="Set if running in interactive mode")
	args = parser.parse_args()
	QC(args)
