import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2
import math

ori = cv2.imread('samples/sample0.jpg')
img = ori

img = ip.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh, img = ip.binarize(img)
img = cv2.bilateralFilter(img,9,100,100)
temp = ip.resize(img, 0.3);
ip.displayImage(temp);

img = cv2.Canny(img, 150, 200)
img = ip.dilate(img, 10)
temp = ip.resize(img, 0.3);
ip.displayImage(temp);

#get x amount of smallest contours
contours = ip.getContours(img)
# x = len(contours)
# sensitivity = int(numpy.ceil(x/2))
# print sensitivity

# contours = ip.getTopContours(contours, sensitivity)
u.writeToFile(contours, 'contours')

left, top, right, bottom = ip.drawRects(ori, contours)

cropped = ori[top:bottom, left:right]

cropped = ip.resize(cropped, 0.3)
ip.displayImage(cropped, "cropped")

# ml.kmeans(contours, 5)

