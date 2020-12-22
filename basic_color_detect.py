import cv2
import numpy as np

path = "TrialTrench_Sample2_6500.png"
img = cv2.imread(path)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_range = np.array([169, 100, 100])                     # Red color
upper_range = np.array([189,255,255])
# lower_range = np.array([110,50,50])                        # Blue color
# upper_range = np.array([130,255,255])

mask = cv2.inRange(hsv, lower_range, upper_range)

cv2.imshow('image', img)
cv2.imshow('mask', mask)


cv2.waitKey(0)
cv2.destroyAllWindows()