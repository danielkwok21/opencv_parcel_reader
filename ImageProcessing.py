import cv2
import numpy as np
import math
import os

def displayImage(img, option="name"):
	cv2.imshow(option, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return

def erode(img, x=3, i=1):
	kernel = np.ones((x,x), np.uint8)
	return cv2.erode(img, kernel, iterations=i)

def dilate(img, x=3, i=1):
	kernel = np.ones((x,x), np.uint8)
	return cv2.dilate(img, kernel, iterations=i)

def resize(img, factor=0.3):
	temp = img
	return cv2.resize(temp, (0,0), fx=factor, fy=factor)

# def binarize(img, threshold = 127, algo=cv2.THRESH_BINARY):
# 	if algo == 'otsu':
# 		algo = cv2.THRESH_OTSU
# 	else:
# 		algo = cv2.THRESH_BINARY
# 	print 'algo: ', algo
# 	(thresh, binary) = cv2.threshold(img, threshold, 255, algo)
# 	return (thresh, binary)

# grayscales & binarizes image 
# returns editedImage, contours, and hierarchy
def getContours(img):
	if len(img.shape) > 2:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return img2, contours, hierarchy

# same as getContours() but sorted
def getSortedContours(img):
	if len(img.shape) > 2:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)
	return img2, contours, hierarchy

def drawDot(img, coor, color):
	# white
	if color == 1:
		color = (255, 255, 255)
	# red
	elif color == 2:
		color = (0, 0, 255)
	# blue
	elif color == 3:
		color = (255, 0, 0)
	# green
	elif color == 4:
		color = (0, 255, 0)
	# black
	else:
		color = (0, 0, 0)

	return cv2.circle(img,(coor[0], coor[1]), 5, color, -1)

def drawContours(img, contours):
	return cv2.drawContours(img, contours, -1, (255, 255, 255), 5)

def rotateImage(img, angle):
	temp = img
	if angle < -45:
		angle = (90 + angle)

	(h, w) = img.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(temp, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_TRANSPARENT)
	return rotated

def getMinAreaRectFromContour(contour):
	center, (w, h), angle = cv2.minAreaRect(contour)
	minRect = (center, (w, h), angle)
	box = cv2.boxPoints(minRect)
	box = np.int0(box)
	return center, (w, h), angle, [box]

# takes in coloured image
# returns 3 return values from cv2.minAreaRect, 
# and a [box] for drawing purposes with drawContours()
def getMinAreaRectFromImage(img):
	img2, contours, hierarchy = getContours(img)
	contours = np.concatenate(contours)
	center, (w, h), angle = cv2.minAreaRect(contours)
	minRect = (center, (w, h), angle)
	box = cv2.boxPoints(minRect)
	box = np.int0(box)
	return center, (w, h), angle, [box]

# draw rectangle around all contours in image
# return left, top, right and bottom
# of largest contour (for cropping purposes)
def drawRects(img, contours):
	temp = img
	rects = []
	for c in contours:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		x, y, w, h = cv2.boundingRect(approx)
		rects.append([x, y, x+w, y+h])
		cv2.rectangle(temp, (x, y), (x+w, y+h), (0, 255, 0), 1);

	xs = []
	ys = []
	ws = []
	hs = []

	for rect in rects:
		x, y, w, h = rect
		xs.append(x);
		ys.append(y);
		ws.append(w);
		hs.append(h);

	left = min(xs)
	top = min(ys)
	right = max(ws)
	bottom = max(hs)

	cv2.rectangle(temp, (left,top), (right,bottom), (255, 0, 0), 2)
	return temp,(left, top, right, bottom)


# gets img as bin
# returns an angle that would fix any misalignment based on text orientation
def getAlignAngle(img):
	temp = img

	if len(temp.shape) > 2:
		temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	height, width = temp.shape

	# temp = erode(temp, 5, 10)
	# temp = dilate(temp, 5, 5)

	# contours = getSortedContours(contours)[:len(contours)/4]
	_, contours, hierarchy = getSortedContours(temp)
	contours = filter(lambda c: not isOutlier(cv2.contourArea(c), map(lambda c: cv2.contourArea(c), contours), 'upper'), contours)


	horzCounter = 0
	vertCounter = 0
	angles = []

	# diagnostics-
	white_blank = np.ones((height, width, 1))
	# print 'len(contours): ', len(contours)	

	for contour in contours:
	# contour = contours[10]
		center, (w, h), angle, [box] = getMinAreaRectFromContour(contour)

		# diagnostics-
		white_blank = drawContours(white_blank, [box])

		if w/h>1:
			horzCounter = horzCounter+1
			angles.append(angle)
		else:
			vertCounter = vertCounter+1

	cv2.imwrite('D:/Code/Python/OpenCV/samples/labelled/whiteblank.jpg', white_blank)

	angles = removeOutliers(angles)
	angle = sum(angles)/len(angles)

	# # diagnostics-
	# print 'horzCounter ', horzCounter
	# print 'vertCounter', vertCounter

	if horzCounter>=vertCounter:
		# print 'is horz - correct orientation'
		# print 'angle:', angle
		return angle, True
	else:
		angle = 360 - angle
		# print 'is vert - wrong orientation'
		# print 'angle:', angle
		return angle, False

def getIQ(arr, range):
	if not len(arr)%2:
		# even
		return (arr[(len(arr)/4*range)-1] + arr[len(arr)/4*range])/2.0
	else:
		# odd
		return arr[(len(arr)/4*range)]

def removeOutliers(arr):
	if len(arr) > 2:
		arr.sort()
		IQ1 = getIQ(arr, 1)
		IQ3 = getIQ(arr, 3)
		IQR = IQ3 - IQ1
		lower_limit = IQ1 - IQR
		upper_limit = IQ3 + IQR

		for a in arr:
			if a<lower_limit or a>upper_limit:
				arr.remove(a)
		return arr
	else:
		return arr

def isOutlier(d, arr, bias='none'):
	if len(arr) > 2:
		arr.sort()
		median = getIQ(arr, 2)
		IQ1 = getIQ(arr, 1)
		IQ3 = getIQ(arr, 3)
		IQR = IQ3 - IQ1
		lower_limit = IQ1 - IQR
		upper_limit = IQ3 + IQR

		if bias=='upper':
			return d<lower_limit
		elif bias=='lower':
			return d>upper_limit
		else:
			return d<lower_limit or d>upper_limit
	else:
		return false
		
def createMask(img, lower, upper):
	mask = cv2.inRange(img, lower, upper)
	mask = dilate(mask, x=5,i = 10)
	mask = erode(mask, x=5,i = 10)
	return mask

