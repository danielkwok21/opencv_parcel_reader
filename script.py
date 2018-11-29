import ImageProcessing as ip
import Util as u
import MachineLearning as ml
import numpy
import cv2
import json
from matplotlib import pyplot as plt

ori = cv2.imread('samples/sample0.jpg')
img = ori

wordObjects = json.load(open('samples/wordObjects.json'))


for w in wordObjects:
	if w['field']!='':		
		# topleft
		x1 = w['vertices'][3]['x']
		y1 = w['vertices'][3]['y']

		#bottom right
		x2 = w['vertices'][1]['x']
		y2 = w['vertices'][1]['y']

		topLeft = (x1, y1)
		bottomRight = (x2, y2)

		# draw rect from json	
		cv2.rectangle(img, topLeft, bottomRight, (0,255,0), 3)

		#find centroid
		mid_x = (x1+x2)/2
		mid_y = (y1+y2)/2

		cv2.circle(img, (mid_x, mid_y), 6, (255,0,0), -1)

		# plot centroids w diff colour according to fields
		if(w['field']=='location'):
			plt.scatter(mid_x,mid_y,20,'b','o')
		elif(w['field']=='person'):
			plt.scatter(mid_x,mid_y,20,'g','o')


img = ip.resize(img, 0.35)
ip.displayImage(img)
plt.show()