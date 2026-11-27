""" *****************************************************
      Billeder der skal manipuleres, bør ligge
      i folderen 'python_images' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2

myfile = "En_firkant.png"
#myfile = "En_firkant_en_cirkel.png"
#myfile = "En_firkant_en_stor_cirkel.png"

mydir = os.path.expanduser("python_images")
path = pathlib.Path(mydir, myfile)

image = cv2.imread(str(path))
#print(image)
original = image.copy()
(h, w, c) = image.shape[:3]
# display the image width, height, and number of channels to our
# terminal
print("width: {} pixels".format(w))
print("height: {} pixels".format(h))
print("channels: {}".format(c))
cv2.imshow("Image - ORG",image)


cv2.waitKey(0) # Waits for any key
cv2.destroyAllWindows()
