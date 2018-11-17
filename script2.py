import numpy as np
import cv2
from matplotlib import pyplot as plt

#k-means
x = [28, 90, 25, 90, 79, 90, 57, 76, 47, 55, 87, 29, 61, 31, 74, 50, 83, 49, 30, 45, 26, 88, 52, 99]
y = [249, 218, 247, 248, 177, 214, 233, 250, 246, 251, 182, 184, 197, 183, 240, 179, 199, 241,
 250, 233, 228, 247, 239, 177]

#joins lists
z = np.hstack((x,y))	

#transform
z = z.reshape((48,1))	

#change type to float32
z = np.float32(z)		

#plot on histogram
plt.hist(z,256,[0,256]),plt.show()

# Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

# Set flags (Just to avoid line break in the code)
flags = cv2.KMEANS_RANDOM_CENTERS

# Apply KMeans
compactness,labels,centers = cv2.kmeans(z,2,None,criteria,10,flags)

print compactness
print labels
print centers