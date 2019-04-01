import ImageProcessing as ip
import Util as u
import numpy as np
import cv2
import sys

imgPath = 'D:/Code/Python/OpenCV/samples/sample11.jpg'
newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/orange.jpg'
# imgPath = 'D:/Code/Python/OpenCV/samples/sample13.jpg'
# newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/purple.jpg'
# imgPath = 'D:/Code/Python/OpenCV/samples/sample4.jpg'
# newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/white.jpg'
ori = cv2.imread(imgPath, cv2.IMREAD_COLOR)
img = ori
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

img = cv2.GaussianBlur(img, (5,5), 0)

def onTrackbarChange(val):

	l_h = cv2.getTrackbarPos('L - H', 'Trackbars')
	l_s = cv2.getTrackbarPos('L - S', 'Trackbars')
	l_v = cv2.getTrackbarPos('L - V', 'Trackbars')
	u_h = cv2.getTrackbarPos('U - H', 'Trackbars')
	u_s = cv2.getTrackbarPos('U - S', 'Trackbars')
	u_v = cv2.getTrackbarPos('U - V', 'Trackbars')

	print(l_h, l_s, l_v)
	lower = np.array([l_h, l_s, l_v])
	upper = np.array([u_h, u_s, u_v])
	mask = cv2.inRange(img, lower, upper)
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

# createTrackbar()
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# lower_purple = np.array([120, 20, 40])
# upper_purple = np.array([179, 50, 255])
lower_purple = np.array([130, 60, 60])
upper_purple = np.array([179, 50, 255])
get_purple_mask = cv2.inRange(img, lower_purple, upper_purple)
get_purple_mask = ip.dilate(get_purple_mask, x=5,i = 10)
get_purple_mask = ip.erode(get_purple_mask, x=5,i = 10)
# result = cv2.bitwise_and(img, img, mask=get_purple_mask)

# lower_orange = np.array([0, 30, 20])
# upper_orange = np.array([179, 255, 255])
lower_purple = np.array([120, 20, 40])
upper_purple = np.array([179, 50, 255])
get_orange_mask = cv2.inRange(img, lower_orange, upper_orange)
get_orange_mask = ip.dilate(get_orange_mask, x=5,i = 10)
get_orange_mask = ip.erode(get_orange_mask, x=5,i = 10)
# result = cv2.bitwise_and(img, img, mask=get_orange_mask)

mask = cv2.bitwise_or(get_purple_mask, get_orange_mask)
result = cv2.bitwise_and(img, img, mask=mask)

h, s, v = cv2.split(result)
img = v

# ip.displayImage(img)
cv2.imwrite(newImgPath, img)


print 'PreVision script done.'