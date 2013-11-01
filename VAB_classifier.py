import os, sys
import Image
import numpy as np_
import atexit
import time 
from math import exp

class VAB_classifier:

	#isn't recognised as a function
	# somethings broken.
	def sigmoid(y):
		return (1 / (1 + exp(-y)))
	
	def rbgMV(image):
		rows = image.size[0]
		cols = image.size[1]
		npixels = rows*cols
		clrs = image.getcolors(npixels)
		mean = [0,0,0]
		for colour in clrs:
			mean[0]+= colour[0] * colour[1][0]
			mean[1]+= colour[0] * colour[1][1]
			mean[2]+= colour[0] * colour[1][2]
		mean[0] = mean[0] / npixels
		mean[1] = mean[1] / npixels
		mean[2] = mean[2] / npixels
		
		var = [0,0,0]
		for colour in clrs:
			var[0] += (colour[0] * ((colour[1][0] - mean[0])**2))
			var[1] += (colour[0] * ((colour[1][1] - mean[1])**2))
			var[2] += (colour[0] * ((colour[1][2] - mean[2])**2))
		var[0] = var[0] / npixels
		var[1] = var[1] / npixels
		var[2] = var[2] / npixels
		out = [mean[0], mean[1], mean[2], var[0], var[1], var[2]]
		return out 
	
	def valForBS(features):
		# a = sigmoid(features[0])
		# b = sigmoid(features[1])
		# c = sigmoid(features[2])
		# d = sigmoid(features[3])
		# e = sigmoid(features[4])
		# f = sigmoid(features[5])
		a = (1. / (1 + exp(-features[0])))
		b = (1. / (1 + exp(-features[1])))
		c = (1. / (1 + exp(-features[2])))
		d = (1. / (1 + exp(-features[3])))
		e = (1. / (1 + exp(-features[4])))
		f = (1. / (1 + exp(-features[5])))
		return a + b + c + d + e + f
		# signoid (each feature)
		# then do binary search onit

	def sec_lowest(dicti):
		minVal = 9e19
		minKey = ''
		for key in dicti:
			if abs(dicti[key]) < minVal and (not abs(dicti[key]) == 0):
				minVal = dicti[key];
				minKey = key
		return (minKey, minVal)

	size = 128, 128
	fileDict = {}
	distDict = {}
	
	start = time.time()
	os.chdir('classify')
	for infile in os.listdir('.'):
		outfile = os.path.splitext(infile)[0] + ".thumbnail"
		if infile != outfile:
		    try:
		        im = Image.open(infile).convert('RGB')
		        im.thumbnail(size, Image.ANTIALIAS)
		        im.save(outfile, "png")
		        fileDict[infile] =  valForBS(rbgMV(Image.open(outfile)))
		    except Exception as e: #IOError
		       print "cannot create thumbnail for '%s'" % infile
		       print e
		# At this point we have the thumbnail to work with
		# if 'thumbnail' in infile:
		# 	continue
	time1 = time.time()
	for key in fileDict.keys():
		dist = 0
		for i in range(6):
			#dist += (fileDict[key][i] - fileDict['123_mod.jpg'][i])**2
			dist += (fileDict[key] - fileDict['123_mod.jpg'])**2
		distDict[key]= dist
	print sec_lowest(distDict)
	time2 = time.time()
	print time1 - start
	print time2 - time1

VAB_classifier()