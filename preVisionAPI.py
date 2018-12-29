import ImageProcessing as ip
import Util as u
import numpy
import cv2

ori = cv2.imread('samples/sample1.jpg', cv2.IMREAD_COLOR)
img = ori

# rotate image
h, w, c = img.shape
print h
print w
print c

temp = ip.resize(img, 0.3)
ip.displayImage(temp)

if h > w:
	img = ip.rotateBound(img, 90)

temp = ip.resize(img, 0.3)
ip.displayImage(temp)

print 'PreVision script done.'

