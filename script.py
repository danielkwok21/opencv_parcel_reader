import ImageProcessing as ip
import Util as u
import numpy
import cv2

oriReal = cv2.imread('real.jpeg', 0)
real = oriReal
oriTemplate = cv2.imread('template.jpeg', 0)
template = oriTemplate

real = ip.dilate(real, 13)
real = ip.erode(real, 25)
_, real = ip.binarize(real)

template = ip.erode(template, 10)
template = ip.dilate(template, 10)
_, template = ip.binarize(template)
template = 255-template

cv2.imwrite('./result/realProcessed.jpg', real)
cv2.imwrite('./result/templateProcessed.jpg', template)