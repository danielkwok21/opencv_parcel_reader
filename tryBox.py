import ImageProcessing as ip
import Util as u
import numpy as np
import cv2
import sys
import os

# vertImgPath = 'D:/Code/Python/OpenCV/samples/horzTilt.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/horzTilt2.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/vertTilt.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/vertTilt2.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/vertTilt3.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/vert.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/horz.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/text.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/sample4.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/sample7.jpg'
# vertImgPath = 'D:/Code/Python/OpenCV/samples/sample15.jpg'

imgPath2 = 'D:/Code/Python/OpenCV/samples/labelled/ori.jpg'
newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/filtered.jpg'
rotatedPath = 'D:/Code/Python/OpenCV/samples/labelled/rotated.jpg'
contoursPath = 'D:/Code/Python/OpenCV/samples/labelled/contours.jpg'

ori = cv2.imread(vertImgPath, cv2.IMREAD_COLOR)
cv2.imwrite(imgPath2, ori)
img = ori

contourImg, angle, isHorz = ip.getAlignAngle(img)
print 'angle: ', angle
print 'isHorz: ', isHorz

cv2.imwrite(contoursPath, contourImg)
img = ip.rotateImage(img, angle)
cv2.imwrite(rotatedPath, img)

print 'PreVision script done.'