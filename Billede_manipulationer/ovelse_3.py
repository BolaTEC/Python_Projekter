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

# We need a grayscale
# version to be able to
# detect objects
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Image - Gray",img_gray)

blur = cv2.GaussianBlur(img_gray, (3, 3), 0.5)
cv2.imshow("Image - Blur",blur)

thresh = cv2.threshold(blur, 1, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cv2.imshow("Image - Threshold",thresh)

cv2.waitKey(0) # Waits for any key
cv2.destroyAllWindows()
