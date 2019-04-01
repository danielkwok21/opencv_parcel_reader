import cv2
import numpy as np
import math

def displayImage(img, option="name"):
	img = resize(img, 0.2)
	cv2.imshow(option, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return

def erode(img, x):
	kernel = np.ones((x,x), np.uint8)
	return cv2.erode(img, kernel, iterations=1)

def dilate(img, x):
	kernel = np.ones((x,x), np.uint8)
	return cv2.dilate(img, kernel, iterations=1)

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
	temp = img
	ret, thresh = binarize2(temp)
	img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return img2, contours, hierarchy

def getTopContours(contours, sensitivity):
	return sorted(contours, key=cv2.contourArea)[:sensitivity]

def drawContours(img, contours):
	cv2.drawContours(img, contours, -1, (255, 0, 0), 5)
	return

def rotateImage(img, angle):
	if angle < -45:
		angle = (90 + angle)

	(h, w) = img.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_TRANSPARENT)
	return rotated

# takes in coloured image
# returns 3 return values from cv2.minAreaRect, and a [box] for drawing purposes
def getMinAreaRect(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img2, contours, hierarchy = getContours(img)
	contours = np.concatenate(contours)
	center, rect, angle = cv2.minAreaRect(contours)
	minRect = (center, rect, angle)
	box = cv2.boxPoints(minRect)
	box = np.int0(box)
	return center, rect, angle, [box]

# draw rectangle around contours, return left, top, right and bottom
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

def rgb2hsv(img):
	img = np.asarray(img)
	col = len(img)
	row = len(img[0])

	for i in range(col):
		for j in range(row):
			b, g, r = img[i][j]

			_g = g/255.0
			_r = r/255.0
			_b = b/255.0
			cmax = max([_b, _g, _r])
			cmin = min([_b, _g, _r])
			delta = cmax-cmin

			# hue
			if delta == 0:
				hue = 0
			else:
				switcher = {
					_b: 60 * ((_r - _g) / delta + 4),
					_g: 60 * ((_b - _r) / delta + 2),
					_r: 60 * (((_g - _b) / delta) % 6)
				}
				hue = switcher.get(cmax)

			# saturation
			if cmax==0:
				sat = 0
			else:
				sat = delta/cmax

			# value
			val = cmax
			img[i][j] = [hue, sat, val]

	return img

def hsv2rgb(img):
	h, s, v = cv2.split(img)
	c = v*s
	x = c*(1-abs((h/60)%2-1))
	m = v-c

	print h

	if h in range(0, 60):
		_v = (c, 0, x)
	elif h in range(60, 120):
		_v = (x, c, 0)
	elif h in range(120, 180):
		_v = (0, x, c)
	elif h in range(180, 240):
		_v = (0, x, c)
	elif h in range(240, 300):
		_v = (x, 0, c)
	else:
		_v = (c, 0, x)

	(_r, _g, _b) = _v

	(r, g, b) = ((_r+m)*255, (_g+m)*255, (_b+m)*255)

	img = (r, g, b)

	return img

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











