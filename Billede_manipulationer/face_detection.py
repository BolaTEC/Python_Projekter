""" *****************************************************
      Billeder der skal manipuleres, bør ligge
      i folderen 'python_images' i samme folder som py-filerne
      og XML filer skal bruges, bør ligge
      i folderen 'xml_filer' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2
import imutils

def convertToRGB(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
myfile = "Random_AI_person.png"
#myfile = "holdfoto.jpg"
#myfile = "fodboldhold.jpg"

myxml = os.path.expanduser("xml_filer")

xmlFile=pathlib.Path(myxml,"haarcascade_frontalface_default.xml")
#xmlFile=pathlib.Path(myxml,'haarcascade_eye_tree_eyeglasses.xml')
#xmlFile=pathlib.Path(myxml,'haarcascade_eye.xml')
#xmlFile=pathlib.Path(myxml,'haarcascade_smile.xml')
#xmlFile=pathlib.Path(myxml,'haarcascade_profilefaces.xml')

haar_cascade_face = cv2.CascadeClassifier(str(xmlFile))

mydir = os.path.expanduser("python_images")
path = pathlib.Path(mydir, myfile)
image = cv2.imread(str(path))

original = image.copy()
(h, w, c) = image.shape[:3]
# display the image width, height, and number of channels to our
# terminal
print("width: {} pixels".format(w))
print("height: {}  pixels".format(h))
print("channels: {}".format(c))
cv2.imshow("Image - ORG",image)

# OpenCV opens images as BRG 
# but we want it as RGB and 
# we also need a grayscale 
# version
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Image - Gray",img_gray)

blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
thresh = cv2.threshold(blur, 1, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cv2.imshow("Image - Threshold",thresh)

#faces_rects = haar_cascade_face.detectMultiScale(img_gray, scaleFactor =1.102, minNeighbors = 7);
#faces_rects = haar_cascade_face.detectMultiScale(img_gray, scaleFactor =1.102, minNeighbors = 12);
faces_rects = haar_cascade_face.detectMultiScale(img_gray, scaleFactor =1.105, minNeighbors = 12);


print("Number of faces found "+ str(len(faces_rects))+ "\n" +str(faces_rects))

for (x,y,w,h) in faces_rects:
     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Face found",image)

cv2.waitKey(0) # Waits for any key
cv2.destroyAllWindows()

