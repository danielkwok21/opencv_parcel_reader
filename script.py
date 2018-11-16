import numpy
import cv2

def displayImage(img):
	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def grayScale(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def blur(img):
	return cv2.blur(img, (5,5))

def complement(img):
	return cv2.bitwise_not(img)

def resize(img):
	return cv2.resize(img, (0,0), fx=0.3, fy=0.3) 

def binarize(img):
	img = grayScale(img)
	(thresh, binary) = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)
	return cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]

def detectEdges(img):
	return cv2.Canny(img, 100, 200)

def getContours(img):
	thresh, binary = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)
	(img2, contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours

ori = cv2.imread('sample.jpg')
img = resize(ori)
img = blur(img)
img = binarize(img)
img = complement(img)
displayImage(img)
img = detectEdges(img)
print getContours(img)

# https://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/