# import the necessary packages
import ast
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from pathlib import Path

HSV_VALUES_PATH = Path(__file__).with_name("hsv_values.txt")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the objects in the HSV color space,
# then initialize the list of tracked points
hsvLower = (29, 86, 56)            # <------ GUL TENNISBOLD
hsvUpper = (64, 255, 255)

if HSV_VALUES_PATH.exists():
	loaded_hsv = {}
	with HSV_VALUES_PATH.open(encoding="utf-8") as values_file:
		for line_number, line in enumerate(values_file, start=1):
			if not line.strip():
				continue
			name, separator, value_text = line.partition("=")
			name = name.strip()
			if not separator or name not in ("hsvLower", "hsvUpper") or name in loaded_hsv:
				raise ValueError(f"Invalid HSV values file at line {line_number}")
			values = ast.literal_eval(value_text.strip())
			if (
				not isinstance(values, tuple)
				or len(values) != 3
				or any(type(value) is not int or not 0 <= value <= 255 for value in values)
			):
				raise ValueError(f"Invalid HSV tuple at line {line_number}")
			loaded_hsv[name] = values

	if set(loaded_hsv) != {"hsvLower", "hsvUpper"}:
		raise ValueError(f"HSV values file must contain hsvLower and hsvUpper: {HSV_VALUES_PATH}")

	hsvLower = loaded_hsv["hsvLower"]
	hsvUpper = loaded_hsv["hsvUpper"]

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()  # <------  Check your camera source here *********
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)
# keep looping
while True:
	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=1024) # main image size is set here
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)


	# construct a mask for the color, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	# ------------------------------------------------------
	mask = cv2.inRange(hsv, hsvLower, hsvUpper)
	
	# ------------------------------------------------------
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	cnts = cnts[1] if imutils.is_cv2() else cnts[0] # Interchanged cnts[1] with cnts[0] and vise versa bola 2022
	center = None
	
	if cnts is None:
		cnts = []
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# update the points queue
	pts.appendleft(center)
		# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	cv2.imshow("Frame - Press q to exit", frame)
	cv2.imshow("MASK - HSV",mask)

	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()
