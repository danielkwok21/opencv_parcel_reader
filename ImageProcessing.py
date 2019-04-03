import cv2
import numpy as np
import math

def displayImage(img, option="name"):
	# img = resize(img, 0.2)
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
	center, rect, angle = cv2.minAreaRect(contour)
	minRect = (center, rect, angle)
	box = cv2.boxPoints(minRect)
	box = np.int0(box)
	return center, rect, angle, [box]

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
def getAlignAngle(bin):
	temp = bin

	temp = erode(temp, 5, 10)
	# ip.displayImage(ip.resize(temp))

	temp = dilate(temp, 5, 5)
	# ip.displayImage(ip.resize(temp))

	temp, contours, hierarchy = getContours(temp)

	contours = getSortedContours(contours)[:len(contours)/4]

	horzCounter = 0
	vertCounter = 0
	totalAngle = 0
	aveAngle = 0

	# # diagnostics-
	# white_blank = np.ones((height, width, 1))
	# print 'len(contours): ', len(contours)	

	for contour in contours:
	# contour = contours[8]
		center, rect, angle, [box] = getMinAreaRectFromContour(contour)

		# # diagnostics-
		# white_blank = ip.drawContours(white_blank, [box])
		boxWidth = abs(box[0][0] - box[2][0])
		boxHeight = abs(box[0][1] - box[2][1])

		if boxWidth/boxHeight>1:
			horzCounter = horzCounter+1
			totalAngle = totalAngle+angle
		else:
			vertCounter = vertCounter+1


	aveAngle = totalAngle/len(contours)

	# # diagnostics-
	# print 'horzCounter ', horzCounter
	# print 'vertCounter', vertCounter
	# print '\ntotalAngle ', totalAngle
	# print 'aveAngle', aveAngle

	if horzCounter>=vertCounter:
		# print 'is horz - correct orientation'
		return aveAngle
	else:
		# print 'is vert - wrong orientation'
		return aveAngle+90