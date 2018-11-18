import numpy as np
import cv2
from matplotlib import pyplot as plt

class ML:
	def kmeans(list, k):
		# X = [[34, 36], [47, 35] ,[47, 25], [25, 43], [29, 34], [37, 47], [30, 29]]
		# Y = [[84, 75], [75, 65], [83, 81], [81, 81], [72, 80], [77, 82], [70, 71]]
		# Z = np.vstack((X,Y))

		# convert to np.float32
		Z = list
		Z = np.float32(Z)


		# define criteria and apply kmeans()
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		ret,label,center=cv2.kmeans(Z,k,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

		# Now separate the data, Note the flatten()
		categories = []
		for i in range(k):
			print i
			categories.append(Z[label.ravel()==i])

		# Plot the data

		for cat in categories:
			plt.scatter(cat[:,0],cat[:,1])
			# plt.scatter(B[:,0],B[:,1],c = 'r')
			plt.scatter(center[:,0],center[:,1],s = 80,c = 'y', marker = 's')

		plt.xlabel('Height'),plt.ylabel('Weight')
		plt.show()
