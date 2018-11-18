from imageProcessing import ImageProcessing
from Util import Util
from MachineLearning import ML
import numpy
import cv2

ip = ImageProcessing()
u = Util()
ml = ML()

ori = ip.read('samples/sample2.jpg')
ori = ip.resize(ori)
img = ori

img = ip.blur(img)
img = ip.grayScale(img)
binary = ip.binarize(img)
img = ip.detectEdges(img)

kernel = numpy.ones((3,3), numpy.uint8)
img = cv2.dilate(img, kernel, iterations=1)
ip.displayImage(img)

#get 200 smallest contours
sensitivity = 200
contours = ip.getTopContours(ip.getContours(img), sensitivity)

ip.drawContours(ori, contours)
ip.displayImage(ori)
#ml.kmeans(flat_contours, 5)
