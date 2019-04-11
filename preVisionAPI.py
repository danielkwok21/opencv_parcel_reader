import ImageProcessing as ip
import Util as u
import numpy as np
import cv2
import sys

imgPath = 'D:/Code/Python/OpenCV/samples/sample3.jpg'
imgPath2 = 'D:/Code/Python/OpenCV/samples/labelled/ori.jpg'
newImgPath = 'D:/Code/Python/OpenCV/samples/labelled/filtered.jpg'

ori_image_path = imgPath
api_img_path = newImgPath

ori = cv2.imread(ori_image_path, cv2.IMREAD_COLOR)
cv2.imwrite(imgPath2, ori)
img = ori
img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img = cv2.GaussianBlur(img, (5,5), 0)

h, s, v = cv2.split(img)
thresh, binary = ip.binarize(v)

# align image
prepared = False
total_angle = 0
loops = 0
maxLoops = 50
while True:
    trial_angle, is_horz = ip.getAlignAngle(binary)
    binary = ip.rotateImage(binary, trial_angle)
    loops = loops + 1
    print loops
    if is_horz:
        prepared = True
    if loops > maxLoops:
        break
    if prepared	and not is_horz:
        break	
    else:
        total_angle = total_angle + trial_angle
        
img = ip.rotateImage(ori, total_angle)
h, s, v = cv2.split(img)
img = v
cv2.imwrite(api_img_path, img)

print 'PreVision script done.'