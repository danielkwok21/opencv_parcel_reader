import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2

ori = ip.read('samples/sample.png')
# ori = ip.resize(ori)
img = ori

img = ip.blur(img)
img = ip.grayScale(img)
binary = ip.binarize(img)
img = ip.detectEdges(img)

img = ip.dilate(img, 5)

#get 200 smallest contours
sensitivity = 200
contours = ip.getTopContours(ip.getContours(img), sensitivity)
u.writeToFile(contours, 'contours')

left, top, right, bottom = ip.drawRects(ori, contours)

cropped = img[top:bottom, left:right]
ip.displayImage("cropped", cropped)

# ml.kmeans(contours, 5)

