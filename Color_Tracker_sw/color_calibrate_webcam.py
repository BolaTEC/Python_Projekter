import ast
import cv2
import numpy as np
from pathlib import Path

HSV_VALUES_PATH = Path(__file__).with_name("hsv_values.txt")

# Make sure the lower value is always less than the upper value and vice versa. 
# This is done by using a mutable dictionary to track whether the callbacks are ready
def trackbar_pair_callbacks(lower_name, upper_name):
    ready = {"value": False}

    def update_lower(value):
        if ready["value"] and value > cv2.getTrackbarPos(upper_name, "Control"):
            cv2.setTrackbarPos(upper_name, "Control", value)

    def update_upper(value):
        if ready["value"] and value < cv2.getTrackbarPos(lower_name, "Control"):
            cv2.setTrackbarPos(lower_name, "Control", value)

    return update_lower, update_upper, ready

# Contours w/ greatest number of points
# TODO max by area
def biggestContourI(contours):
    maxVal = 0
    maxI = None
    for i in range(0, len(contours) - 1):
        if len(contours[i]) > maxVal:
            cs = contours[i]
            maxVal = len(contours[i])
            maxI = i
    return maxI
            

iLowH = 100;
iHighH = 150;
iLowS = 100; 
iHighS = 150;
iLowV = 100;
iHighV = 150;

# Load saved HSV values if they exist
if HSV_VALUES_PATH.exists():
    saved_hsv = {}
    with HSV_VALUES_PATH.open(encoding="utf-8") as values_file:
        for line_number, line in enumerate(values_file, start=1):
            if not line.strip():
                continue
            name, separator, value_text = line.partition("=")
            name = name.strip()
            if not separator or name not in ("hsvLower", "hsvUpper") or name in saved_hsv:
                raise ValueError(f"Invalid HSV values file at line {line_number}")
            values = ast.literal_eval(value_text.strip())
            if (
                not isinstance(values, tuple)
                or len(values) != 3
                or any(type(value) is not int or not 0 <= value <= 255 for value in values)
            ):
                raise ValueError(f"Invalid HSV tuple at line {line_number}")
            saved_hsv[name] = values

    if set(saved_hsv) != {"hsvLower", "hsvUpper"}:
        raise ValueError(f"HSV values file must contain hsvLower and hsvUpper: {HSV_VALUES_PATH}")

    iLowH, iLowS, iLowV = saved_hsv["hsvLower"]
    iHighH, iHighS, iHighV = saved_hsv["hsvUpper"]

iHighH = max(iLowH, iHighH)
iHighS = max(iLowS, iHighS)
iHighV = max(iLowV, iHighV)

contourOn=True;

cv2.namedWindow('Control')
h_lower_callback, h_upper_callback, h_callbacks_ready = trackbar_pair_callbacks("LowH", "HighH")
s_lower_callback, s_upper_callback, s_callbacks_ready = trackbar_pair_callbacks("LowS", "HighS")
v_lower_callback, v_upper_callback, v_callbacks_ready = trackbar_pair_callbacks("LowV", "HighV")
cv2.createTrackbar("LowH", "Control", iLowH, 255, h_lower_callback);
cv2.createTrackbar("HighH", "Control", iHighH, 255, h_upper_callback);
cv2.createTrackbar("LowS", "Control", iLowS, 255, s_lower_callback);
cv2.createTrackbar("HighS", "Control", iHighS, 255, s_upper_callback);
cv2.createTrackbar("LowV", "Control", iLowV, 255, v_lower_callback);
cv2.createTrackbar("HighV", "Control", iHighV, 255, v_upper_callback);
h_callbacks_ready["value"] = True
s_callbacks_ready["value"] = True
v_callbacks_ready["value"] = True

# Initialize the webcam The 0 argument is the device index. If you have multiple cameras, you can change this number to select a different camera.
cam = cv2.VideoCapture(0)

while True:
    ret_val, img = cam.read()

    lh = cv2.getTrackbarPos('LowH', 'Control')
    ls = cv2.getTrackbarPos('LowS', 'Control')
    lv = cv2.getTrackbarPos('LowV', 'Control')
    hh = cv2.getTrackbarPos('HighH', 'Control')
    hs = cv2.getTrackbarPos('HighS', 'Control')
    hv = cv2.getTrackbarPos('HighV', 'Control')

    lower = np.array([lh, ls, lv], dtype = "uint8")
    higher = np.array([hh, hs, hv], dtype = "uint8")
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create a mask based on the HSV range
    h, w = img.shape[:2]
    #print (img.shape)
    flt = cv2.inRange(hsv, lower, higher);
    #breakpoint()

    contours0, hierarchy = cv2.findContours(flt, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # HAd im2 infront of this line
    
    # Only draw the biggest one 
    bc = biggestContourI(contours0)
    if contourOn==True:
        if bc != None:
            cv2.drawContours(img,contours0, bc, (0,255,0), 3)
    
    cv2.imshow('Color setup - Press q to exit | Press c to toggle countour tracing | Press s to save values', img)
    cv2.imshow('hsv', hsv)
    cv2.imshow('flt', flt)
    
    key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    # if the 'c' key is pressed, toogle the countour highlighting    
    elif key == ord("c"):
        contourOn= not contourOn
    # if the 's' key is pressed, save the current HSV values to a file    
    elif key == ord("s"):
        with HSV_VALUES_PATH.open("w", encoding="utf-8") as values_file:
            values_file.write(f"hsvLower = ({lh}, {ls}, {lv})\n")
            values_file.write(f"hsvUpper = ({hh}, {hs}, {hv})\n")

cv2.destroyAllWindows()
