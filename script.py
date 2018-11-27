import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2

ori = cv2.imread('samples/sample.jpg')
ori = ip.resize(ori)
img = ori
ip.displayImage(img)

img = cv2.blur(img, (5,5))
img = ip.cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
binary = ip.binarize(img)
img = cv2.Canny(img, 100, 200)

img = ip.dilate(img, 5)
ip.displayImage(img)

#get 200 smallest contours
sensitivity = 200
contours = ip.getTopContours(ip.getContours(img), sensitivity)
u.writeToFile(contours, 'contours')

left, top, right, bottom = ip.drawRects(ori, contours)

cropped = img[top:bottom, left:right]
ip.displayImage(cropped, "cropped")

# ml.kmeans(contours, 5)

