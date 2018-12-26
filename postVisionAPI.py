import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2
import json
from matplotlib import pyplot as plt

ori = cv2.imread('samples/sample3.jpg')
img = ori

width, height = ori.shape[:2]
blank = numpy.zeros((width, height, 3), numpy.uint8)

wordObjects = json.load(open('samples/wordObjects.json'))

for w in wordObjects:
	if w['field']!='':
		print w['string']

		# topleft
		x1 = w['vertices'][3]['x']
		y1 = w['vertices'][3]['y']

		#bottom right
		x2 = w['vertices'][1]['x']
		y2 = w['vertices'][1]['y']

		topLeft = (x1, y1)
		bottomRight = (x2, y2)

		# draw rect from json
		cv2.rectangle(blank, topLeft, bottomRight, (255, 0, 0), 3)
		cv2.rectangle(img, topLeft, bottomRight, (255, 0, 0), 3)

		#find centroid
		mid_x = (x1+x2)/2
		mid_y = (y1+y2)/2
		centroid = (mid_x, mid_y)

		cv2.circle(blank, centroid, 6, (255, 0, 0), -1)
		cv2.circle(img, centroid, 6, (255, 0, 0), -1)

center, rect, angle, box = ip.getMinAreaRect(blank)
cv2.drawContours(blank, box, 0, (0, 0, 255), 5)
temp = ip.resize(blank, 0.3)
ip.displayImage(temp, 'minRect')

img = ip.rotateImage(img, angle)
temp = ip.resize(img, 0.3)
ip.displayImage(temp, 'rotated')

