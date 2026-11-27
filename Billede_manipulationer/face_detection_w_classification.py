import os
import pathlib
import cv2
import imutils
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the pre-trained model (replace 'model.h5' with your model file)
model = load_model("path/to/your/model.h5")


def convertToRGB(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
myfile = "Mig_2022.jpg"
#myfile = "Mig_2019.jpg"

#myfile = "Personale_21.jpg"
#myfile = "Personale_22.jpg"
#myfile = "Personale_24.jpg"
#myfile = "Personale_25.jpg"


#myfile = "B2m.jpg"
#myfile = "B2m2.jpg"

#myfile = "B_3m.jpg"
#myfile = "B3m Flip.jpg"
#myfile = "holdfoto.jpg"
#myfile = "fodboldhold.jpg"
myxml = os.path.expanduser(r"~/OneDrive - TEC/python/billede_manip")

xmlFile=pathlib.Path(myxml,"haarcascade_frontalface_default.xml")
haar_cascade_face = cv2.CascadeClassifier(str(xmlFile))
#haar_cascade_face = cv2.CascadeClassifier('haarcascade_eye.xml')
#haar_cascade_face = cv2.CascadeClassifier('haarcascade_smile.xml')
#haar_cascade_face = cv2.CascadeClassifier('haarcascade_profilefaces.xml')



mydir = os.path.expanduser("~\OneDrive - TEC\Billeder\Billedbehandling\python_images")
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

#blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
#thresh = cv2.threshold(blur, 1, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#cv2.imshow("Image - Threshold",thresh)

faces_rects = haar_cascade_face.detectMultiScale(img_gray, scaleFactor =1.102, minNeighbors = 7);

print("Number of faces found "+ str(len(faces_rects))+ "\n" +str(faces_rects))

for (x,y,w,h) in faces_rects:
     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Face found",image)

# Preprocess the image (resize and normalize)
image = cv2.resize(img_gray, (224, 224))  # Assuming the model expects 224x224 images
image = image / 255.0  # Normalize the image
image = np.expand_dims(image, axis=0)  # Add batch dimension

# Perform gender classification
predictions = model.predict(image)
gender = 'Male' if predictions[0][0] > 0.5 else 'Female'
confidence = predictions[0][0] if gender == 'Male' else 1 - predictions[0][0]

print(f"Gender: {gender}, Confidence: {confidence:.2f}")


cv2.waitKey(0) # Waits for any key
cv2.destroyAllWindows()

