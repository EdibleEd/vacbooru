import os, sys
import Image
import numpy as np_
import atexit
import time 


class VAB_classifier:
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

	def sec_lowest(dicti):
		minVal = 999999999
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
	os.chdir('dbu\\')
	for infile in os.listdir('.'):
		outfile = os.path.splitext(infile)[0] + ".thumbnail"
		if infile != outfile:
		    try:
		        im = Image.open(infile).convert('RGB')
		        im.thumbnail(size, Image.ANTIALIAS)
		        im.save(outfile, "png")
		        fileDict[infile] =  rbgMV(Image.open(outfile))
		    except Exception: #IOError
		       print "cannot create thumbnail for '%s'" % infile
		# At this point we have the thumbnail to work with
		# if 'thumbnail' in infile:
		# 	continue
	time1 = time.time()
	for key in fileDict.keys():
		dist = 0
		for i in range(6):
			dist += (fileDict[key][i] - fileDict['000aaaaaa_3.jpg'][i])**2
		distDict[key]= dist
	print sec_lowest(distDict)
	time2 = time.time()
	print time1 - start
	print time2 - time1

VAB_classifier()