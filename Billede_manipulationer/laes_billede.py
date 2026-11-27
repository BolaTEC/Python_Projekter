""" *****************************************************
      Billeder der skal manipuleres, bør ligge
      i folderen 'python_images' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2

myfile = "En_firkant.png"

mydir = os.path.expanduser("python_images")
path = pathlib.Path(mydir, myfile)

image = cv2.imread(str(path)) # load original image

(h, w, c) = image.shape[:3]
# display the image width, height, and number of channels to our
# terminal
print("width: {} pixels".format(w))
print("height: {}  pixels".format(h))
print("channels: {}".format(c))
cv2.imshow("Image - ORG",image) # show original image

# scale picture up or down
scale_percent = 60 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv2.resize(image, dim, interpolation = cv2.INTER_CUBIC)
cv2.imshow("Resized",resized)

cv2.waitKey(0) # Waits for any key
cv2.destroyAllWindows()

