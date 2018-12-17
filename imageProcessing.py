import cv2
import numpy

def displayImage(img, option="Image"):
	cv2.imshow(option, img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return

def erode(img, i):
	kernel = numpy.ones((3,3), numpy.uint8)
	return cv2.erode(img, kernel, iterations=i)

def dilate(img, i):
	kernel = numpy.ones((3,3), numpy.uint8)
	return cv2.dilate(img, kernel, iterations=i)
	
def resize(img, factor=0.3):
	return cv2.resize(img, (0,0), fx=factor, fy=factor) 

def binarize(img):
	(thresh, binary) = cv2.threshold(img, 200, 255, cv2.THRESH_OTSU)
	return (thresh, binary)

# binarizes image and returns contours
def getContours(img):
	temp = img
	ret, thresh = binarize(temp)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours

def removeBigContours(contours):
	newContours = []
	totalArea = 0
	for c in contours:
		totalArea = totalArea+cv2.contourArea(c)
	aveArea = totalArea/len(contours)
	for c in contours:
		if cv2.contourArea(c)<=aveArea:
			newContours.append(c)
	return newContours


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