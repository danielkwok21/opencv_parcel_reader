import ImageProcessing as ip
import Util as u
import numpy as np
import cv2
import sys
import os

imgPath = 'D:/Code/Python/OpenCV/samples/arrow.png'
imgPath2 = 'D:/Code/Python/OpenCV/samples/labelled/ori.jpg'
newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/filtered.jpg'
whitePath = 'D:/Code/Python/OpenCV/samples/labelled/white.jpg'

ori = cv2.imread(imgPath, cv2.IMREAD_COLOR)
cv2.imwrite(imgPath2, ori)
img = ori

center, (w, h), angle, [box] = ip.getMinAreaRectFromImage(img)


cv2.imwrite(newImgPath, img)


print 'PreVision script done.'