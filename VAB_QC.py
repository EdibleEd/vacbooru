# TAKES a set of tupples of the form
# {source_url, source_hash, [tags]}
# OPTIONALLY TAKES cull tags list, user name
# RETURNS a set of tupples of the form
# {source_url, source_hash, [tags]}

# A series of quality checking steps
# All do not alter the format of the data
# Steps projected are as follows:
# 1. Check if file is already uploaded
# 2. Cull file if it has certain tags
# 3. add user to tags
# 4. Add or remove existing tags
# 5. verify checksum is sane

class VAB_QC:

	def __init__(self, args):
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
	def cullTags(self, data, tags):
		pass
	
	# Add a set of tags to the data
	def addTags(self, data, tags):
		pass
		
	# Add a user tag to the data
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
