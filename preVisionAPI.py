import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2
import math

ori = cv2.imread('samples/sample2.jpg')
img = ori
temp = ip.resize(img, 0.3)
ip.displayImage(temp)

img = cv2.bilateralFilter(img, 9, 75, 75)
img = ip.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh, img = ip.binarize(img)

temp = ip.resize(img, 0.3)
ip.displayImage(temp)

cv2.imwrite('samples/binSample2.jpg', img)
