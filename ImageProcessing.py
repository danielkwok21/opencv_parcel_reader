import cv2
import numpy as np
import math

def displayImage(img, option="name"):
	img = resize(img, 0.2)
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

def binarize(img, threshold = 127):
	(thresh, binary) = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
	return (thresh, binary)

def binarize2(img, threshold = 127):
	(thresh, binary) = cv2.threshold(img, threshold, 255, cv2.THRESH_OTSU)
	return (thresh, binary)

# binarizes image and returns editedImage, contours, and hierarchy
def getContours(img):
	img2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return img2, contours, hierarchy

def getSortedContours(contours):
	return sorted(contours, key=cv2.contourArea, reverse=True)

def drawContours(img, contours):
	cv2.drawContours(img, contours, -1, (255, 0, 0), 5)
	return img

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
# returns 3 return values from cv2.minAreaRect, and a [box] for drawing purposes with drawContours()
def getMinAreaRect(img):
	# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img2, contours, hierarchy = getContours(img)
	contours = np.concatenate(contours)
	center, rect, angle = cv2.minAreaRect(contours)
	minRect = (center, rect, angle)
	box = cv2.boxPoints(minRect)
	box = np.int0(box)
	return center, rect, angle, [box]

# draw rectangle around contours directly around image
# return left, top, right and bottom
# of largest contour (for cropping purposes)
def drawRects(img, contours):
	rects = []
	for c in contours:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		x, y, w, h = cv2.boundingRect(approx)
		rects.append([x, y, x+w, y+h])
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1);

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

	cv2.rectangle(img, (left,top), (right,bottom), (255, 0, 0), 2)
	return left, top, right, bottom

def rotateBound(img, angle):
	h, w, c = img.shape
	cx = w/2
	cy = h/2
	center = (cx, cy)

	M = cv2.getRotationMatrix2D(center, -angle, 1.0)
	cos = np.abs(M[0, 0])
	sin = np.abs(M[0, 1])

	_w = int((h*sin)+(w*cos))
	_h = int((h*cos)+(w*sin))

	M[0, 2] += (_w/2)-cx
	M[1, 2] += (_h/2)-cy

	return cv2.warpAffine(img, M, (_w, _h))

# gets img as bin
# returns an angle that would fix any misalignment based on text orientation
def getAlignAngle(binary):
	temp = binary
	height, width = temp.shape

	temp = erode(temp, 5, 10)

	temp = dilate(temp, 5, 5)

	temp, contours, hierarchy = getContours(temp)

	# contours = getSortedContours(contours)[:len(contours)/4]

	horzCounter = 0
	vertCounter = 0
	angles = []
	aveAngle = 0

	# diagnostics-
	white_blank = np.ones((height, width, 1))
	print 'len(contours): ', len(contours)	

	for contour in contours:
	# contour = contours[20]
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
	print 'this angle:', angle

	# # diagnostics-
	# print 'horzCounter ', horzCounter
	# print 'vertCounter', vertCounter

	if horzCounter>=vertCounter:
		# print 'is horz - correct orientation'
		return -angle
	else:
		# print 'is vert - wrong orientation'
		return -(angle+90)

def getIQ(arr, range):
	if not len(arr)%2:
		# even
		return (arr[(len(arr)/4*range)-1] + arr[len(arr)/4*range])/2.0
	else:
		# odd
		return arr[(len(arr)/4*range)]

def removeOutliers(arr):
	median = getIQ(arr, 2)
	IQ1 = getIQ(arr, 1)
	IQ3 = getIQ(arr, 3)
	IQR = IQ3 - IQ1
	lower_limit = IQ1 - IQR
	upper_limit = IQ3 + IQR

	for a in arr:
		if a<lower_limit or a>upper_limit:
			arr.remove(a)

	return arr

def createMask(img, lower, upper):
	mask = cv2.inRange(img, lower, upper)
	mask = dilate(mask, x=5,i = 10)
	mask = erode(mask, x=5,i = 10)
	return mask

