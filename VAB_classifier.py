import os, sys
import Image
import numpy as np_
import atexit
import time 
from math import exp
import scipy.signal as ss_
import scipy.misc as sm_

class VAB_classifier:

	#isn't recognised as a function
	# somethings broken.
	def sigmoid(y):
		return (1 / (1 + exp(-y)))
	
	# Comparator that creates a 6vector feature set
	# 	<meanR meanB meanG varR varB varG>
	# Performance on basic set is (117.4113 0.0014)
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

	# Compares image curvature in each of the R G and B pixel colours
	# Does not cope well with big image modifications like erasing sections
	# Performance on basic set is (117.6904459 0.00297808647156)
	# Or for actual scaled images (117.495517015 0.00292205810547)
	def curvature(image):
		r, g, b = image.split()
		rArray = np_.array(r)
		gArray = np_.array(g)
		bArray = np_.array(b)
		l = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
		rCurve = ss_.convolve2d(rArray, l)
		gCurve = ss_.convolve2d(gArray, l)
		bCurve = ss_.convolve2d(bArray, l)
		cr = 0
		cg = 0
		cb = 0
		for i in range(len(rCurve)):
			for j in range(len(rCurve[0])):
				cr += rCurve[i, j]**2
				cg += gCurve[i, j]**2
				cb += bCurve[i, j]**2
		return [cr, cb, cg]


	# This is the baseline comparator
	# Compare each pixel value to the corresponding pixel
	# 	Or if there is no pixel there due to aspect ratio difference, return maximum difference
	# Performance on basic set is (96.8937, 26.0121) (higher is worse)
	def pixDiff(image, image2):
		rows = image.size[0]
		cols = image.size[1]
		out = 0
		for i in range(rows):
			for j in range(cols):
				try:
					r, g, b = image.getpixel((i, j))
					r1, g1, b1 = image2.getpixel((i, j))
					out += ((r-r1)**2 + (g-g1)**2 + (b-b1)**2)
				except Exception:
					# the images are of different ratios
					# maximised error on any pixel that is not common to both
					out += ((255**2) * 3)
		return out 

	# This is needed because the source and target images we want to find exists within the test folder
	# And the source needs to be discarded 
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
		        fileDict[infile] = curvature(im)
		        #fileDict[infile] =  (rbgMV(im))
		    except Exception as e: #IOError
		       print "cannot create thumbnail for '%s'" % infile
		       print e
		# At this point we have the thumbnail to work with
		# if 'thumbnail' in infile:
		# 	continue
	time1 = time.time()
	for key in fileDict.keys():
		#dist = (fileDict[key] - fileDict['123_mod.jpg'])**2
		
		dist = 0
		for i in range(3):
			dist += (fileDict[key][i] - fileDict['123_mod4.jpg'][i])**2
			#dist += (fileDict[key] - fileDict['123_mod.jpg'])**2
		distDict[key]= dist
	print sec_lowest(distDict)
	time2 = time.time()
	print time1 - start
	print time2 - time1

VAB_classifier()