import ImageProcessing as ip
import Util as u
import cv2

ori = cv2.imread('samples/sample1.jpg')
img = ori
smooth = cv2.bilateralFilter(img,9,100,100)

# binarize and smoothening
img = ip.cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)
thresh, img = ip.binarize(img)

# edge detection by canny & dilate all edges
img = cv2.Canny(img, 150, 200)
img = ip.dilate(img, 10)

# extracts all contours from image
# writes it to a file to store
# crops a rectangle to encapsulate all contours
contours = ip.getContours(img)
u.writeToFile(contours, 'contours')
left, top, right, bottom = ip.drawRects(smooth, contours)
cropped = smooth[top:bottom, left:right]

# resize and display
cropped = ip.resize(cropped, 0.3)
ip.displayImage(cropped, "cropped")


