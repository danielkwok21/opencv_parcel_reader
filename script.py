from imageProcessing import ImageProcessing
from Util import Util
from MachineLearning import ML
import numpy
import cv2

ip = ImageProcessing()
u = Util()
ml = ML()

ori = ip.read('samples/sample.png')
# ori = ip.resize(ori)
img = ori

img = ip.blur(img)
img = ip.grayScale(img)
binary = ip.binarize(img)
img = ip.detectEdges(img)

kernel = numpy.ones((5,5), numpy.uint8)
img = cv2.dilate(img, kernel, iterations=1)

#get 200 smallest contours
sensitivity = 200
contours = ip.getTopContours(ip.getContours(img), sensitivity)
flat_contours = [y for x in contours for y in x]
u.writeToFile(flat_contours, 'flat_contours')

# ip.drawContours(ori, contours)

# drawrect
rects = []
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    x, y, w, h = cv2.boundingRect(approx)
    
    rect = (x, y, w, h)
    rects.append(rect)
    cv2.rectangle(ori, (x, y), (x+w, y+h), (0, 255, 0), 1);

ip.displayImage(ori);

ml.kmeans(contours, 5)
