""" *****************************************************
      XML filer skal bruges, bør ligge
      i folderen 'xml_filer' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2
import imutils
import time
from imutils.video import VideoStream


def convertToRGB(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

myxml = os.path.expanduser("xml_filer")

xmlFile=pathlib.Path(myxml,"haarcascade_frontalface_default.xml")
#xmlFile=pathlib.Path(myxml,'haarcascade_eye.xml')
#xmlFile=pathlib.Path(myxml,'haarcascade_smile.xml')
#xmlFile=pathlib.Path(myxml,'haarcascade_profilefaces.xml')
#xmlFile=pathlib.Path(myxml,'haarcascade_eye_tree_eyeglasses.xml')

haar_cascade_face = cv2.CascadeClassifier(str(xmlFile))


print("Starting camera ... 6 sec.")
vs = VideoStream(src=0).start()
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
	# grab the current frame
	image = vs.read()

	original = image.copy()

	# OpenCV opens images as BRG 
	# but we want it as RGB and 
	# we also need a grayscale 
	# version
	img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces_rects = haar_cascade_face.detectMultiScale(img_gray, scaleFactor =1.33, minNeighbors = 5);

	#----- debug purposes
	#print("Number of faces found"+str(faces_rects))
	#-----
	for (x,y,w,h) in faces_rects:
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

	#cv2.imshow("Face found",image)


	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if image is None:
		break

	# show the frame to our screen
	cv2.imshow("Frame - Press q to exit | Press s to save face", image)

	key = cv2.waitKey(1) & 0xFF

	# if the 's' key is pressed, stop the loop
	if key == ord("s"):
		c = max(faces_rects)
		#print(c)
		x,y,w,h = c
		#save the largest object in own file
		ROI = original[y:y+h, x:x+w]
		cv2.imwrite('Face.png', ROI)
		
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# close all windows
cv2.destroyAllWindows()

