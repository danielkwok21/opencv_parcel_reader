import cv2

class ImageProcessing:
	def read(self, path):
		return cv2.imread(path)

	def displayImage(self, img):
		cv2.imshow('image', img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def grayScale(self, img):
		return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	def blur(self, img):
		return cv2.blur(img, (5,5))

	def complement(self, img):
		return cv2.bitwise_not(img)

	def resize(self, img):
		return cv2.resize(img, (0,0), fx=0.3, fy=0.3) 

	def binarize(self, img):
		(thresh, binary) = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)
		return binary
		# return cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]

	def detectEdges(self, img):
		return cv2.Canny(img, 100, 200)

	# binarizes image and returns contours
	def getContours(self, img):
		temp = img
		ret, thresh = cv2.threshold(temp, 127, 255, 0)
		contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		return contours

	def getTopContours(self, contours, sensitivity):
		return sorted(contours, key = cv2.contourArea)[:sensitivity]

	def drawContours(self, img, contours):
		cv2.drawContours(img, contours, -1, (0, 255, 0), 5)