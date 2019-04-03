import ImageProcessing as ip
import Util as u
import numpy as np
import cv2
import sys

imgPath = 'D:/Code/Python/OpenCV/samples/sample4.jpg'
newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/rotated.jpg'
contoursImgPath = 'D:/Code/Python/OpenCV/samples/labelled/contours.jpg'

ori = cv2.imread(imgPath, cv2.IMREAD_COLOR)
img = ori
height, width, channels = img.shape
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(img)
img = v

thresh, bin = ip.binarize(img)

angle = ip.getAlignAngle(bin)

aligned = ip.rotateImage(ori, angle)

# diagnostics-
cv2.imwrite(newImgPath, aligned)

print 'PreVision script done.'