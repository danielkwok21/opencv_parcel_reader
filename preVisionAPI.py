import ImageProcessing as ip
import Util as u
import numpy as np
import cv2
import sys

# imgPath = 'D:/Code/Python/OpenCV/samples/red.png'
# newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/red.png'
imgPath = 'D:/Code/Python/OpenCV/samples/sample13.jpg'
newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/sample13.jpg'

ori = cv2.imread(imgPath, cv2.IMREAD_COLOR)
img = ori
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def onTrackbarChange(val):

	l_h = cv2.getTrackbarPos('L - H', 'Trackbars')
	l_s = cv2.getTrackbarPos('L - S', 'Trackbars')
	l_v = cv2.getTrackbarPos('L - V', 'Trackbars')
	u_h = cv2.getTrackbarPos('U - H', 'Trackbars')
	u_s = cv2.getTrackbarPos('U - S', 'Trackbars')
	u_v = cv2.getTrackbarPos('U - V', 'Trackbars')

	print(l_h, l_s, l_v)
	lower_purple = np.array([l_h, l_s, l_v])
	upper_purple = np.array([u_h, u_s, u_v])
	mask = cv2.inRange(img, lower_purple, upper_purple)
	ip.displayImage(mask)

def createTrackbar():
	# trackbars
	cv2.namedWindow('Trackbars')
	cv2.createTrackbar('L - H', 'Trackbars', 0, 179, onTrackbarChange)
	cv2.createTrackbar('L - S', 'Trackbars', 0, 255, onTrackbarChange)
	cv2.createTrackbar('L - V', 'Trackbars', 0, 255, onTrackbarChange)
	cv2.createTrackbar('U - H', 'Trackbars', 179, 179, onTrackbarChange)
	cv2.createTrackbar('U - S', 'Trackbars', 255, 255, onTrackbarChange)
	cv2.createTrackbar('U - V', 'Trackbars', 255, 255, onTrackbarChange)


lower_purple = np.array([120, 20, 40])
upper_purple = np.array([179, 255, 255])
get_purple_mask = cv2.inRange(img, lower_purple, upper_purple)
result = cv2.bitwise_and(img, img, mask=get_purple_mask)
h, s, v = cv2.split(result)

cv2.imwrite(newImgPath, v)

print 'PreVision script done.'