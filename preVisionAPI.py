import ImageProcessing as ip
import cv2
import numpy as np

# load ori image
ori = cv2.imread('samples/sample2.jpg', cv2.IMREAD_COLOR)
img = ori

# change from bgr to hls
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# extract l channel
h, s, v = cv2.split(img)

temp = ip.resize(v, 0.3)
ip.displayImage(temp, 'v')

# adaptive histogram equalization
clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(4,4))
cl = clahe.apply(v)

temp = ip.resize(cl, 0.3)
ip.displayImage(temp, 'cl')

cv2.imwrite('samples/hsv/hsv_v.jpg', cl)