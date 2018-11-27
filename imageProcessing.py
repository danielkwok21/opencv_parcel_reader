import cv2
import numpy

def read(path):
	return cv2.imread(path)

def displayImage(option, img):
	cv2.imshow(option, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return

def erode(img):
	kernel = numpy.ones((3,3), numpy.uint8)
	return cv2.erode(img, kernel, iterations=1)

def dilate(img, x):
	kernel = numpy.ones((x,x), numpy.uint8)
	return cv2.dilate(img, kernel, iterations=1)
	
def grayScale(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def blur(img):
	return cv2.blur(img, (5,5))

def complement(img):
	return cv2.bitwise_not(img)

def resize(img):
	return cv2.resize(img, (0,0), fx=0.3, fy=0.3) 

def binarize(img):
	(thresh, binary) = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)
	return binary
	# return cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]

def detectEdges(img):
	return cv2.Canny(img, 100, 200)

# binarizes image and returns contours
def getContours(img):
	temp = img
	ret, thresh = cv2.threshold(temp, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours

def getTopContours(contours, sensitivity):
	return sorted(contours, key = cv2.contourArea)[:sensitivity]

def drawContours(img, contours):
	cv2.drawContours(img, contours, -1, (0, 255, 0), 5)
	return


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