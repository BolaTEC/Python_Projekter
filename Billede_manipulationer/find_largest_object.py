""" *****************************************************
      Billeder der skal manipuleres, bør ligge
      i folderen 'python_images' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2

myfile = "Patterns2.png"
#myfile = "test2.jpg"
#myfile = "En_firkant.png"
"""
myfile = "En_firkant_en_cirkel.png"
myfile = "En_firkant_en_stor_cirkel.png"
"""

mydir = os.path.expanduser("python_images")
path = pathlib.Path(mydir, myfile)

image = cv2.imread(str(path))
#print(image)
original = image.copy()
(h, w, c) = image.shape[:3]
# display the image width, height, and number of channels to our
# terminal
print("width: {} pixels".format(w))
print("height: {}  pixels".format(h))
print("channels: {}".format(c))
cv2.imshow("Image - ORG",image)

# We need a grayscale 
# version to be able to
# detect objects
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Image - Gray",img_gray)

blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
thresh = cv2.threshold(blur, 1, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#print("Threshold value used: ", thres)
cv2.imshow("Image - Threshold",thresh)

# using a findContours() function
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Avoid using the whole image as an area
#contours = contours[1:] if len(contours) > 0 else contours[0:]

# Find the largest contour in the mask, then use
# it to compute the minimum enclosing circle and
# centroid
c = max(contours, key=cv2.contourArea)
#print(c)
x,y,w,h = cv2.boundingRect(c)

# Draw rectangle
cv2.rectangle(image, (x-1, y-1), (x + w+1, y + h+1), (0,0,255), 4)
cv2.imshow("Largest",image)

#save the largest object in own file
ROI = original[y:y+h, x:x+w]
cv2.imwrite('ROI.png', ROI)

cv2.waitKey(0) # Waits for any key
cv2.destroyAllWindows()

