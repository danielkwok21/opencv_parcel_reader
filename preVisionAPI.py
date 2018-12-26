import ImageProcessing as ip
import cv2
import numpy as np

# load ori image
ori = cv2.imread('samples/sample2.jpg', cv2.IMREAD_COLOR)
img = ori
temp = ip.resize(img, 0.3)
ip.displayImage(temp, 'ori')

# change from bgr to lab
img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# extract l channel
l, a, b = cv2.split(img)

# adaptive histogram equalization
clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(4,4))
cl = clahe.apply(l)

# remerge to create new lab
img = cv2.merge((cl, a, b))

# convert lab to rgb
img = cv2.cvtColor(img, cv2.COLOR_LAB2BGR)
temp = ip.resize(img, 0.3)
ip.displayImage(temp, 'rgb')

# convert rgb to hsv (to remove orange words)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img)
temp = ip.resize(v, 0.3)
ip.displayImage(temp, 'v')