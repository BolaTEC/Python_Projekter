""" *****************************************************
      Billeder der skal manipuleres, bør ligge
      i folderen 'python_images' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2

myfile = "Patterns2.png"
mydir = os.path.expanduser("python_images")
path = pathlib.Path(mydir, myfile)
image = cv2.imread(str(path))

# we need a grayscale version
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# setting threshold of gray image
thresValue, threshold = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY)

# using a findContours() function
contours, dummy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i = 0
# list for storing names of shapes
for contour in contours:

	# here we are ignoring first contour because
	# findcontour function detects whole image as shape
	if i == 0:
		i = 1
		continue

	# cv2.approxPloyDP() function to approximate the shape
	approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

	# using drawContours() function
	cv2.drawContours(image, [contour], 0, (0, 0, 255), 2)

	# finding center point of shape
	M = cv2.moments(contour)
	print(M)
	if M['m00'] != 0.0:
		x = int(M['m10']/M['m00'])
		y = int(M['m01']/M['m00'])

	# putting shape name at center of each shape
	if len(approx) == 3:
		cv2.putText(image, 'Triangle', (x, y),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1)

	elif len(approx) == 4:
		# compute the bounding box of the contour and use the
		# bounding box to compute the aspect ratio
		(x2, y2, w, h) = cv2.boundingRect(approx)

		ar = w / float(h)
		# a square will have an aspect ratio that is approximately
		# equal to one, otherwise, the shape is a rectangle
		shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

		cv2.putText(image, shape, (x, y),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1)

	elif len(approx) == 5:
		cv2.putText(image, 'Pentagon', (x, y),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1)

	elif len(approx) == 6:
		cv2.putText(image, 'Hexagon', (x, y),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1)

	else:
		cv2.putText(image, 'circle', (x, y),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1)

# displaying the image after drawing contours
cv2.imshow('shapes', image)

cv2.waitKey(0) # Waits for any key
cv2.destroyAllWindows()
