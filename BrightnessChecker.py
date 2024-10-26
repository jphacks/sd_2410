import cv2
import numpy as np
from matplotlib import pyplot as plt


def  homeChecker():
    file = 'photo.jpg'

    #read image file and convert to HSV
    img = cv2.imread(str(file))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)


    #when Value Brightness over exceed 82, decide awake
    if np.mean(v) > 82:
        print('gohome')
        return True
    else:
        print('goout')
        return False
