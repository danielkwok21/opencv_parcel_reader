import ImageProcessing as ip
import Util as u
import numpy as np
import cv2
import sys
import os

vertImgPath = 'D:/Code/Python/OpenCV/samples/horzTilt.jpg'
newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/labelled.jpg'


ori = cv2.imread(vertImgPath, cv2.IMREAD_COLOR)
img = ori
img = ip.dilate(img)

cv2.imwrite(newImgPath, img)

print 'PreVision script done.'