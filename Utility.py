# A bunch of utility functions
import hashlib

def md5(image):
	return hashlib.md5(image.tostring()).hexdigest().lower()

def dbuFilename(imageType, md5):
	return md5 + '.' + imageType

def fileExtension(filepath):
	tokens = filepath.split('.')
	return tokens[-1:][0]

def dbuExistsImage(md5):
	#placeholder for now
	return False