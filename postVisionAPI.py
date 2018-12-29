import ImageProcessing as ip
import Util as u
import numpy
import cv2
import json
import sys

ori = cv2.imread('samples/sample0.jpg')
img = ori

wordObjects = json.load(open('samples/wordObjects.json'))

w = wordObjects[37]
centre = (w['centre']['x'], w['centre']['y'])
topLeft = (w['topLeft']['x'], w['topLeft']['y'])
bottomRight = (w['bottomRight']['x'], w['bottomRight']['y'])

if w['field'] != '':
	cv2.rectangle(img, topLeft, bottomRight, (255, 0, 0), 3)
	cv2.circle(img, centre, 6, (255, 0, 0), -1)

	# draw neighbours
	for n in w['neighbours']:
		wordId = n.split('_')[1]

		for w2 in wordObjects:
			if w2['id'] == wordId:
				cv2.arrowedLine(img, (w['centre']['x'], w['centre']['y']), (w2['centre']['x'], w2['centre']['y']), (0, 0, 0), 2)

else:
	cv2.rectangle(img, topLeft, bottomRight, (0, 255, 0), 3)
	cv2.circle(img, centre, 6, (255, 0, 0), -1)

cv2.imwrite('samples/labelled/labelled.jpg', img)

print 'PostVision script done.'