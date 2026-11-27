""" *****************************************************
      Billeder der skal manipuleres, bør ligge
      i folderen 'python_images' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2

#myfile = "Patterns.png"
myfile = "test2.jpg"
mydir = os.path.expanduser("python_images")
path = pathlib.Path(mydir, myfile)
image = cv2.imread(str(path))

cv2.imshow("Image - ORG",image)

# We need a grayscale 
# version
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Image - Gray",img_gray)

blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
cv2.imshow("Image - Blur",blur)

# Detect edges
canny = cv2.Canny(blur, 10, 100, 3)
cv2.imshow("Image - Canny",canny)

dilated = cv2.dilate(canny, (1, 1), iterations=0)
cv2.imshow("Image - dilated",dilated)

(cnt, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Denne tegner contours om alle objekter
cv2.drawContours(image, cnt, -1, (0, 255, 0), -2)

# Mens denne laver en kasse om dem.
count=1
for c in cnt:
    rect = cv2.boundingRect(c)
    #if rect[2] < 100 or rect[3] < 100: continue
    #print cv2.contourArea(c)
    x,y,w,h = rect
    cv2.rectangle(image,(x-1,y-1),(x+w+1,y+h+1),(0,0,255),1)
    cv2.putText(image,str(count),(x+w+10,y+h),0,0.3,(50,50,50))
    count+=1
      
cv2.imshow("Image - Objects Counted: "+str(len(cnt)),image)
print("Objects in picture: "+str(len(cnt)))

#print(cnt)
cv2.waitKey(0) # Waits for any key
cv2.destroyAllWindows()
