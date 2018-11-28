import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2
import math

ori = cv2.imread('samples/sample11.jpg')
ori = ip.resize(ori, 0.3)
img = ori
ip.displayImage(img)

img = cv2.bilateralFilter(img, 9, 75, 75)
img = ip.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh, img = ip.binarize(img)
ip.displayImage(img)

img = cv2.Canny(img, 150, 200)
ip.displayImage(img)

img = ip.dilate(img, 5)
ip.displayImage(img)

#get x amount of smallest contours
contours = ip.getContours(img)
x = len(contours)
print x

sensitivity = int(numpy.ceil(x/4))
print sensitivity

contours = ip.getTopContours(contours, sensitivity)
u.writeToFile(contours, 'contours')

left, top, right, bottom = ip.drawRects(ori, contours)

cropped = ori[top:bottom, left:right]
ip.displayImage(cropped, "cropped")

# ml.kmeans(contours, 5)

