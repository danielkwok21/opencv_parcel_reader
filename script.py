import ImageProcessing as ip
import Util as u
import numpy
import cv2

oriReal = cv2.imread('real.jpeg', 0)
real = oriReal
oriTemplate = cv2.imread('template.jpeg', 0)
template = oriTemplate

# preprocess
real = ip.dilate(real, 13)
real = ip.erode(real, 20)
_, real = ip.binarize2(real)

# rotate
center, rect, angle, box = ip.getMinAreaRect(real)
ip.drawContours(real, box)
real = ip.rotateImage(real, angle)

cv2.imwrite('./result/realProcessed.jpg', real)
cv2.imwrite('./result/templateProcessed.jpg', template)



