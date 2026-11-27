""" *****************************************************
      Billeder der skal manipuleres, bør ligge
      i folderen 'python_images' i samme folder som py-filerne
    *****************************************************
"""
import os
import pathlib
import cv2

myfile = "En_firkant.png"

"""
myfile = "En_firkant_en_cirkel.png"
myfile = "En_firkant_en_stor_cirkel.png"
"""

mydir = os.path.expanduser("python_images")
path = pathlib.Path(mydir, myfile)

image = cv2.imread(str(path))
print(image)
