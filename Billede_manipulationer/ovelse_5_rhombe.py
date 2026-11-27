""" *****************************************************
      Billeder der skal manipuleres, bør ligge
      i folderen 'python_images' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2
import numpy as np


def angle(p1, p2, p3):
    """
    Beregner vinklen i punkt p2 mellem linjerne
    p1-p2 og p3-p2
    """
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)

    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_theta = np.clip(cos_theta, -1, 1)

    return np.degrees(np.arccos(cos_theta))
    
def distance(p1, p2):
	return np.linalg.norm(np.array(p1) - np.array(p2))


myfile = "Patterns5.png"
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

	# here we are ignoring first counter because
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
		pts = [p[0] for p in approx]

		angles = [angle(pts[3], pts[0], pts[1]),
			angle(pts[0], pts[1], pts[2]),
			angle(pts[1], pts[2], pts[3]),
			angle(pts[2], pts[3], pts[0])
			]
			
		# Beregn sidelængder
		sides = [
			distance(pts[0], pts[1]),
			distance(pts[1], pts[2]),
			distance(pts[2], pts[3]),
			distance(pts[3], pts[0])
		]
		print(f"{sides}")
		# Tjek om alle sider er næsten lige lange
		mean_side1 = (sides[0]+sides[2])/2.0
		mean_side2 = (sides[1]+sides[3])/2.0
		
		
		equal_sides = abs(sides[0] - mean_side2) < 0.1 * mean_side2
		equal_sides &= abs(sides[2] - mean_side2) < 0.1 * mean_side2
		equal_sides &= abs(sides[1] - mean_side1) < 0.1 * mean_side1
		equal_sides &= abs(sides[3] - mean_side1) < 0.1 * mean_side1

		# Alle vinkler skal være tæt på 90 grader
		#print(f"{angles}") 

		right_angles = all(abs(a - 90) < 10 for a in angles)
		
		print(f"{right_angles}") 
		print(f"{equal_sides}")
		ar = w / float(h)
		print(ar)
		# a square will have an aspect ratio that is approximately
		# equal to one, otherwise, the shape is a rectangle
		if (ar >= 0.95 and ar <= 1.05):
			shape = "square"
			#Rhombe overrule
			if not right_angles:
				shape = "rhombe"
		else: 
			#Parallelogram overrule
			if equal_sides:
				shape = "rhombe"
			elif right_angles:
				shape = "rectangle"
			else:
				shape = "parallelogram"

				
	#	#Rhombe overrule
	#	if not right_angles:
	#		shape = "rhombe"
		
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
