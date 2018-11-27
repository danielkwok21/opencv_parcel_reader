import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2

ori = cv2.imread('samples/sample2.jpg')
ori = ip.resize(ori, 0.4)
img = ori
ip.displayImage(img)

img = cv2.blur(img, (7,7))
img = ip.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
binary = ip.binarize(img)
ip.displayImage(img)

img = cv2.Canny(img, 150, 200)
ip.displayImage(img)

img = ip.dilate(img, 5)
ip.displayImage(img)

#get 200 smallest contours
sensitivity = 200
contours = ip.getTopContours(ip.getContours(img), sensitivity)
u.writeToFile(contours, 'contours')

left, top, right, bottom = ip.drawRects(ori, contours)

cropped = ori[top:bottom, left:right]
ip.displayImage(cropped, "cropped")

# ml.kmeans(contours, 5)

