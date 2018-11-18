from imageProcessing import ImageProcessing
from Util import Util
import cv2

ip = ImageProcessing()
u = Util()

ori = ip.read('samples/sample.jpg')
ori = ip.resize(ori)
img = ori

img = ip.blur(img)
img = ip.grayScale(img)
binary = ip.binarize(img)

#get 200 smallest contours
sensitivity = 200
contours = ip.getTopContours(ip.getContours(img), sensitivity)
u.writeToFile(contours)
ip.drawContours(ori, contours)
ip.displayImage(ori)
