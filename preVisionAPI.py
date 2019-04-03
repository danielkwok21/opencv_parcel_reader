import ImageProcessing as ip
import Util as u
import numpy as np
import cv2
import sys

imgPath = 'D:/Code/Python/OpenCV/samples/sample2.jpg'
newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/filtered.jpg'

ori = cv2.imread(imgPath, cv2.IMREAD_COLOR)
img = ori
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img = cv2.GaussianBlur(img, (5,5), 0)

h, s, v = cv2.split(img)
thresh, binary = ip.binarize(v)

# align image
angle = ip.getAlignAngle(binary)
img = ip.rotateImage(ori, angle)


# colour mask
lower_purple = np.array([40, 0, 0])
upper_purple = np.array([179, 255, 255])
purple_mask = ip.createMask(img, lower_purple, upper_purple)
lower_orange = np.array([0, 30, 0])
upper_orange = np.array([179, 255, 255])
orange_mask = ip.createMask(img, lower_orange, upper_orange)
mask = cv2.bitwise_or(purple_mask, orange_mask)
result = cv2.bitwise_and(img, img, mask=mask)

h, s, v = cv2.split(result)
img = v

# ip.displayImage(img)
cv2.imwrite(newImgPath, img)


print 'PreVision script done.'