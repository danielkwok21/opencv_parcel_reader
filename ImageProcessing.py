import cv2
import numpy as np
import math
import os

def displayImage(img, option="name"):
	cv2.imshow(option, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return

# draws display over a blank backgorund for temp display
def displayContours(contours, height, width):
	displayImage(getPlainDrawnContours(contours, height, width), 'contours')
	return

# binarizes img (any type)
def binarize(img):
	temp = img
	temp = grayscale(img)
	thresh, temp = cv2.threshold(temp,127,255,cv2.THRESH_OTSU)
	return thresh, temp

# enables indexed img path to be written to sample path provided
# useful to observe how images change with each iteration
def iterativeWrites(img, path, i):
	newPath = path.split('.')
	newPath = newPath[0]+str(i)+'.'+newPath[1]
	cv2.imwrite(newPath, img)

# less white
def erode(img, x=3, i=1):
	kernel = np.ones((x,x), np.uint8)
	return cv2.erode(img, kernel, iterations=i)

# more white
def dilate(img, x=3, i=1):
	kernel = np.ones((x,x), np.uint8)
	return cv2.dilate(img, kernel, iterations=i)

def resize(img, factor=0.3):
	temp = img
	return cv2.resize(temp, (0,0), fx=factor, fy=factor)

# grayscales img (returns img untouched if is already grayscale)
def grayscale(img):
	if len(img.shape) > 2:
		return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	else:
		return img

# returns if box provided is of horizontal orientation
# box is an array of tuples representing a rect contour
# sample parameter 
# [[709 475] [331 475] [332 257] [709 257]]
def isHorz(box):

	def sortBoxBy(box, i=0):
		if i == 'x':
			i = 0
		elif i == 'y':
			i = 1

		temp = box[:]
		temp = list(temp)
		temp.sort(key=lambda t: t[i])
		return temp

	boxY = sortBoxBy(box, 'y')
	boxX = sortBoxBy(box, 'x')
	height = abs(boxY[0][1] - boxY[2][1])
	width = abs(boxX[0][0] - boxX[2][0])

	# print 'boxY', boxY
	# print 'boxX', boxX
	# print 'height', height
	# print 'width', width

	if width/height<1:
		# print 'vert'
		return False
	else:
		# print 'horz'
		return True

def getPlainDrawnContours(contours, height, width, mark = False):
	img = np.zeros((height,width,3), np.uint8)

	try:
		if mark:
			for c in contours:
				img = drawContours(img, c, isHorz(c[0]))
		else:
			for c in contours:
				img = drawContours(img, c)
		return img
	except:
		if mark:
			return drawContours(img, contours, isHorz(c[0]))
		else:
			return drawContours(img, contours)

# grayscales & binarizes image 
# returns editedImage, contours, and hierarchy
def getContours(img):
	img = grayscale(img)
	img2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return img2, contours, hierarchy

# same as getContours() but sorted by area
def getSortedContours(img):
	img, contours, hierarchy = getContours(img)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)
	return img, contours, hierarchy

def drawDot(img, coor, color='black'):
	# white
	if color == 'white':
		color = (255, 255, 255)
	# red
	elif color == 'red':
		color = (0, 0, 255)
	# blue
	elif color == 'blue':
		color = (255, 0, 0)
	# green
	elif color == 'green':
		color = (0, 255, 0)
	# black
	else:
		color = (0, 0, 0)

	return cv2.circle(img,(coor[0], coor[1]), 5, color, -1)

# draws contours on img provided and returns the drawn image.
# horizontal boxes are red
# vertical boxes are blue
def drawContours(img, contours, redHorz = False):
	if not redHorz:
		# vert blue
		return cv2.drawContours(img, contours, -1, (255, 0, 0), 5)
	else:
		# horz red
		return cv2.drawContours(img, contours, -1, (0, 0, 255), 5)

# -ve angle = clockwise
# +ve angle = anti-clockwise
# returns rotated image based on angle provided
def rotateImage(img, angle):
	temp = img
	(h, w) = img.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(temp, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_TRANSPARENT)
	return rotated

# wraps a min area rect around a contour provided
# returns 3 return values from cv2.minAreaRect, 
# and a [box] for drawing purposes with drawContours()
def getMinAreaRectFromContour(contour):
	center, (w, h), angle = cv2.minAreaRect(contour)
	minRect = (center, (w, h), angle)
	box = cv2.boxPoints(minRect)
	box = np.int0(box)
	return center, (w, h), angle, [box]

# takes in any kind of image
# returns 3 return values from cv2.minAreaRect, 
# and a [box] for drawing purposes with drawContours()
def getMinAreaRectsFromImage(img):
	img2, contours, hierarchy = getContours(img)
	boxes = []
	angles = []
	for c in contours:
		center, (w, h), angle = cv2.minAreaRect(c)
		minRect = (center, (w, h), angle)
		box = cv2.boxPoints(minRect)
		box = np.int0(box)

		boxes.append([box])
		angles.append(angle)

	medianAngle = removeOutliers(angles)
	medianAngle = findAverageMedian(angles)
	return center, (w, h), medianAngle, boxes

# draws regular rect around all contours in image
# returns left, top, right and bottom
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

# takes in any kind of image
# returns an angle that would fix any misalignment based on contour orientation, e.g. text
def getAlignAngle(img):
	temp = img

	if len(temp.shape) > 2:
		temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	thresh, temp = binarize(temp)

	height, width = temp.shape

	# this erode and dilation is based on MAILROOM's context.
	# erode and dilate accordingly when dealing with different images
	temp = erode(temp, 5, 10)
	temp = dilate(temp, 5, 5)

	_, contours, hierarchy = getSortedContours(temp)

	contours = filter(lambda c: not isOutlier(cv2.contourArea(c), map(lambda c: cv2.contourArea(c), contours), 'upper'), contours)

	angles = [0]
	detectedContours = []
	horzCounter = 0
	vertCounter = 0

	# contour = contours[0]
	for contour in contours:
		center, (w, h), angle, [box] = getMinAreaRectFromContour(contour)

		detectedContours.append([box])
		if angle != 0:
			angles.append(angle)
		if isHorz([box][0]):	
			horzCounter = horzCounter + 1
		else:
			vertCounter = vertCounter + 1

	contoursImg = getPlainDrawnContours(detectedContours, height, width, True)
	angles = removeOutliers(angles)
	angle = findAverageMedian(angles)
	# print 'og angle: ', angle

	orientationIsHorz = horzCounter > vertCounter

	# if current orientation is perfect vert
	if not orientationIsHorz and angle == 0:
		# print 'is perfect vert. Forcing 90 degree turn'
		if angle < 0:
			angle = angle - 90
		else:
			angle = angle + 90

	# if current orientation is horz and rotation > 45 (causing a horz -> vert rotation)
	if orientationIsHorz:
		# print 'is horz. Preventing to-vert-rotation'
		if -45>angle>-90:
			angle = 90 + angle
	else:
		# print 'is vert. Converting -ve to +ve to maximize upright probability'
		angle = -angle

	# # diagnostics-
	# print 'post adjustment angle: ', angle
	# print 'horzCounter:', horzCounter
	# print 'vertCounter:', vertCounter
	
	return contoursImg, angle, orientationIsHorz

# returns quartiles
# e.g. range of 2 = 2nd Quartile
def getIQ(arr, range):
	if not len(arr)%2:
		# even
		return (arr[(len(arr)/4*range)-1] + arr[len(arr)/4*range])/2.0
	else:
		# odd
		return arr[(len(arr)/4*range)]

# returns a list of length > 2 with outliers removed
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

# returns if d is an outlier in arr
# bias is a parameter. e.g. a bias of 'upper' would mean d != outlier
# even if d is > upper limit
def isOutlier(d, arr, bias='none'):
	if len(arr) > 2:
		arr.sort()
		median = getIQ(arr, 2)
		IQ1 = getIQ(arr, 1)
		IQ3 = getIQ(arr, 3)
		IQR = IQ3 - IQ1
		lower_limit = IQ1 - IQR
		upper_limit = IQ3 + IQR

		# print 'arr: ', arr
		# print 'IQ1', IQ1
		# print 'IQ3', IQ3
		# print 'IQR', IQR
		# print 'lower_limit', lower_limit
		# print 'upper_limit', upper_limit

		if bias=='upper':
			return d<lower_limit
		elif bias=='lower':
			return d>upper_limit
		else:
			return d<lower_limit or d>upper_limit
	else:
		return False

# finds medians in a continous series
# returns the average of those medians
def findAverageMedian(arr):
	def findFrequency(arr):
		arr = map(lambda a:math.floor(a/10)*10, arr)
		frequencys = []
		for a in arr:
			match = filter(lambda f:f[0]==a, frequencys)
			if match:
				match = match[0]
				frequencys.remove(match)
				count = (a, match[1] + 1)
				frequencys.append(count)
			else:
				count = (a, 1)
				frequencys.append(count)
		return frequencys

	if arr:
		frequencys = findFrequency(arr)
		# print 'frequencys: ', frequencys
		lower_limit = filter(lambda f: f[1] == max(map(lambda f:f[1], frequencys)), frequencys)[0][0]
		range = (lower_limit, lower_limit+10)
		medians = filter(lambda a:range[0]<=a<=range[1], arr)
		averageMedians = sum(medians)/len(medians)
		return averageMedians
	else:
		return arr
		
def createMask(img, lower, upper):
	mask = cv2.inRange(img, lower, upper)
	mask = dilate(mask, x=5,i = 10)
	mask = erode(mask, x=5,i = 10)
	return mask

