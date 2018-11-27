import numpy as np
import cv2
import Util as u
from matplotlib import pyplot as plt

def kmeans(list, k):
	print 'running kmeans...'
	# X = [[34, 36], [47, 35] ,[47, 25], [25, 43], [29, 34], [37, 47], [30, 29]]
	# Y = [[84, 75], [75, 65], [83, 81], [81, 81], [72, 80], [77, 82], [70, 71]]
	# Z = np.vstack((X,Y))

	# convert to np.float32
	Z = list
	flat_contours = [y for x in Z for y in x]
	Z = np.float32(flat_contours)

	# define criteria and apply kmeans()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	ret,label,center=cv2.kmeans(Z,k,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

	# Now separate the data, Note the flatten()
	categories = []
	for i in range(k):
		categories.append(Z[label.ravel()==i])

	# Plot the data

	# x = u.getCol(categories[0], 0)
	# y = u.getCol(categories[0], 1)
	# plt.scatter(x, y)

	# x = u.getCol(categories[1], 0)
	# y = u.getCol(categories[1], 1)
	# plt.scatter(x, y)

	for cat in categories:
		x = u.getCol(cat, 0)
		y =  u.getCol(cat, 1)
		plt.scatter(x, y)
	# plt.scatter(center[:,0],center[:,1],s = 80,c = 'b', marker = 's')

	plt.xlabel('X'),plt.ylabel('Y')
	plt.show()
