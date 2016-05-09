from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
import time
import copy

def threshold(imgArr):
	'''
	Convert a color image to a black and white so that pattern detection will become easier later.
	(Only 2 colors will be used after this - White and Black)
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
				pixel[3] = 255
			elif np.sum(pixel[:3])/3 < balance and greater<lesser:
				#Original image background was of a darker color, so the darker colors get replaced with white
				pixel[0] = 255
				pixel[1] = 255
				pixel[2] = 255
				pixel[3] = 255
			else:
				#Original image non background parts, these get the color black
				pixel[0] = 0
				pixel[1] = 0
				pixel[2] = 0
				pixel[3] = 255

	return newImgArr
		

img = Image.open('images/numbers/0.1.png')
#Create a 3D array where each cell has 4 values - RGBA
imgarr = np.asarray(img)
img2 = Image.open('images/numbers/y0.4.png')
imgarr2 = np.asarray(img2)
img3 = Image.open('images/numbers/y0.5.png')
imgarr3 = np.asarray(img3)
img4 = Image.open('images/sentdex.png')
imgarr4 = np.asarray(img4)

imgarr = threshold(imgarr)
imgarr2 = threshold(imgarr2)
imgarr3 = threshold(imgarr3)
imgarr4 = threshold(imgarr4)

'''
#Display a single image
plt.imshow(img)
plt.show()
'''

'''
#Display 4 images putting them next to each other (2x2 grid)
figure = plt.figure()
ax1 = plt.subplot2grid((8, 6), (0, 0), rowspan=4, colspan=3)
ax2 = plt.subplot2grid((8, 6), (4, 0), rowspan=4, colspan=3)
ax3 = plt.subplot2grid((8, 6), (0, 3), rowspan=4, colspan=3)
ax4 = plt.subplot2grid((8, 6), (4, 3), rowspan=4, colspan=3)

ax1.imshow(imgarr)
ax2.imshow(imgarr2)
ax3.imshow(imgarr3)
ax4.imshow(imgarr4)

plt.show()
'''