import algo_obj_collision_detection
import cv2 as cv
import numpy as np
cv.destroyAllWindows()
# rect = [minX, maxX, minY, maxY] # rect.left = minX, rect.right =maxX, rect.top=minY, rect.bottom =maxY
# coordinates of the rhombus
# point1 = line_left_x1, line_left_y1,
# point2 = line_left_x2, line_left_y2,
# point3 = line_right_x1, line_right_y1,
# point4 = line_right_x2, line_right_y2
minX = 174
minY = 15
maxX = 200
maxY = 100  # to test change the value to 200
line_left_x1 = 40
line_left_y1 = 10
line_left_x2 = 240
line_left_y2 = 300
line_right_x1 = 100
line_right_y1 = 10
line_right_x2 = 300
line_right_y2 = 300

obj_in_roi = algo_obj_collision_detection.Object_in_ROI(minX, maxX, minY, maxY, line_left_x1, line_left_y1, line_left_x2, line_left_y2, line_right_x1, line_right_y1, line_right_x2, line_right_y2)
print("------", obj_in_roi)
print(obj_in_roi.lineFromPoints(obj_in_roi.P_right, obj_in_roi.Q_right))
print(obj_in_roi.lineFromPoints(obj_in_roi.P_left, obj_in_roi.Q_left))
print(obj_in_roi.getSlope(obj_in_roi.P_left, obj_in_roi.Q_left))
print(obj_in_roi.getSlope(obj_in_roi.P_right, obj_in_roi.Q_right))


img = np.zeros((500, 500, 3), np.uint8)


print(obj_in_roi.getX(obj_in_roi.rect[3], obj_in_roi.P_left, obj_in_roi.Q_left))
print(obj_in_roi.rect[0])
print(obj_in_roi.rect[1])
print(obj_in_roi.getX(obj_in_roi.rect[3], obj_in_roi.P_right, obj_in_roi.Q_right))

cv.rectangle(img, (obj_in_roi.rect[0], obj_in_roi.rect[2]), (obj_in_roi.rect[1], obj_in_roi.rect[3]), (0, 255, 0), 1)
if obj_in_roi.isvoilation():
	cv.line(img, (line_left_x1, line_left_y1), (line_left_x2, line_left_y2), (0, 0, 255), 1)
	cv.line(img, (line_right_x1, line_right_y1), (line_right_x2, line_right_y2), (0, 0, 255), 1)
	cv.line(img, (line_left_x1, line_left_y1), (line_right_x1, line_right_y1), (0, 0, 255), 1)
	cv.line(img, (line_left_x2, line_left_y2), (line_right_x2, line_right_y2), (0, 0, 255), 1)
	print(True)
else:
	cv.line(img, (line_left_x1, line_left_y1), (line_left_x2, line_left_y2), (255, 0, 255), 1)
	cv.line(img, (line_right_x1, line_right_y1), (line_right_x2, line_right_y2), (255, 0, 255), 1)
	cv.line(img, (line_left_x1, line_left_y1), (line_right_x1, line_right_y1), (255, 0, 255), 1)
	cv.line(img, (line_left_x2, line_left_y2), (line_right_x2, line_right_y2), (255, 0, 255), 1)

	print(False)
cv.imshow("display", img)
cv.waitKey(0)
cv.destroyAllWindows()
