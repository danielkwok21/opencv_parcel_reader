import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2
import math

ori = cv2.imread('samples/sample0.jpg')
img = ori
temp = ip.resize(img, 0.3)
ip.displayImage(temp)

img = cv2.bilateralFilter(img, 9, 75, 75)
img = ip.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh, img = ip.binarize(img)
temp = ip.resize(img, 0.3)
ip.displayImage(temp)

# img = cv2.Canny(img, 150, 200)
# temp = ip.resize(img, 0.3)
# ip.displayImage(temp)

img = ip.erode(img, 30)
temp = ip.resize(img, 0.3)
ip.displayImage(temp, 'dilated')

#get x amount of smallest contours
contours = ip.getContours(img)
u.writeToFile(contours, 'contours')

left, top, right, bottom = ip.drawRects(ori, contours)

cropped = ori[top:bottom, left:right]
temp = ip.resize(cropped, 0.3)
ip.displayImage(temp)

# ml.kmeans(contours, 5)

