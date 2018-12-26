import ImageProcessing as ip
import cv2
import numpy as np

# load ori image
ori = cv2.imread('samples/sample2.jpg', cv2.IMREAD_COLOR)
img = ori

# change from bgr to hls
img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

# extract l channel
h, l, s = cv2.split(img)

# adaptive histogram equalization
clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(4,4))
cl = clahe.apply(l)

# remerge
img = cv2.merge((h, cl, s))

# convert hls to rgb
img = cv2.cvtColor(img, cv2.COLOR_HLS2BGR)

# convert rgb to hsv (to remove orange words)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img)
temp = ip.resize(v, 0.3)
ip.displayImage(temp, 'v')