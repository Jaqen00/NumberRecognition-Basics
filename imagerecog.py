from PIL import Image
import numpy as np
import sys

import matplotlib.pyplot as plt
import time
import copy
from collections import Counter

def createExamples():
	'''
	Read files we have and create a single file with all the data. We can read that
	file later to get back all the data regarding our examples.
	(Create a training dataset)
	Format: "Number :: array_data"
	'''
	numberArrExamples = open('numberArrExamples.txt', 'w')
	numbersWeHave = range(0, 10)
	versionsWeHave = range(1, 10)

	for number in numbersWeHave:
		for version in versionsWeHave:
			imgPath = 'images/numbers/' + str(number) + '.' + str(version) + '.png'
			imgCur = Image.open(imgPath)
			imgCurArr = threshold(np.array(imgCur))
			#Storage is easier if we just convert the matrix for each image into a string
			lineToWrite = str(number) +  "::" + str(imgCurArr.tolist()) + '\n'
			numberArrExamples.write(lineToWrite)



def identifyNumber(filePath):
	'''
	Works currently only on 8x8 images
	'''
	matchedArr = []
	loadExamples = open('numberArrExamples.txt', 'r').read().split('\n')

	img = Image.open(filePath)
	imgArr = threshold(np.array(img))
	imgArrList = imgArr.tolist()

	currentImgStr = str(imgArrList)

	for example in loadExamples:
		#Ignore blank lines etc
		if len(example) > 3:
			splitExample = example.split("::")
			exampleNumber = splitExample[0]
			exampleStr = splitExample[1]

			examplePixels = exampleStr.split('],')
			currentPixels = currentImgStr.split('],')

			for pixel in range(len(examplePixels)):
				if examplePixels[pixel][:3] == currentPixels[pixel][:3]:
					matchedArr.append(int(exampleNumber))

	#Gives us a map with "value":"matched_count" pairs
	matches = Counter(matchedArr)
	print matches

	max_match = -1
	match_value = 0
	for key in matches:
		if matches[key] > match_value:
			match_value = matches[key]
			max_match = key

	if match_value < 400:
		print 'NO MATCH FOUND'
	else:
		print 'MATCH FOUND: ' + str(max_match)

	#Comment from here if matplotlib is not installed or if the plot is not needed
	graphX = matches.keys()
	graphY = matches.values()

	figure = plt.figure()
	#Draw the image on the top
	ax1 = plt.subplot2grid((5, 4), (0, 0), rowspan=2, colspan=4)
	#Display the matches with a barchart
	ax2 = plt.subplot2grid((5, 4), (2, 0), rowspan=3, colspan=4)
	ax1.imshow(imgArr)
	ax2.bar(graphX, graphY, align="center")

	#Barchart show only values which are greater than 400
	plt.ylim(400)

	#Display all values on the x-axis instead of only multiples of 2 for the x-axis labels
	xloc = plt.MaxNLocator(10+2)
	ax2.xaxis.set_major_locator(xloc)

	plt.show()



def threshold(imgArr):
	'''
	Convert a color image to a black and white so that pattern detection will become easier later.
	(Only 2 colors will be used after this - White(Background) and Black(Context) )
	'''
	balanceArr = []
	newImgArr = copy.deepcopy(imgArr)

	for row in imgArr:
		for pixel in row:
			avgNum = np.sum(pixel[:3])/3
			balanceArr.append(avgNum)

	balance = np.sum(balanceArr)/len(balanceArr)

	greater = 0
	lesser = 0

	for row in imgArr:
		for pixel in row:
			if np.sum(pixel[:3])/3 > balance:
				greater += 1
			else:
				lesser += 1

	#We want to replace the maximum color with the background which in our case will be white

	for row in newImgArr:
		for pixel in row:
			if np.sum(pixel[:3])/3 > balance and greater>lesser:
				#Original image background was of a lighter color, so the lighter colors get replaced with white (our new background)
				pixel[0] = 255
				pixel[1] = 255
				pixel[2] = 255
				if len(pixel) > 3:
					pixel[3] = 255
			elif np.sum(pixel[:3])/3 < balance and greater<lesser:
				#Original image background was of a darker color, so the darker colors get replaced with white
				pixel[0] = 255
				pixel[1] = 255
				pixel[2] = 255
				if len(pixel) > 3:
					pixel[3] = 255
			else:
				#Original image non background parts, these get the color black
				pixel[0] = 0
				pixel[1] = 0
				pixel[2] = 0
				if len(pixel) > 3:
					pixel[3] = 255

	return newImgArr


createExamples()
identifyNumber(sys.argv[1])