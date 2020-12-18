# Python program to explain cv2.rectangle() method

# importing cv2
import cv2

# path
path = r"BLOCKS\blocks_ext.png"

# Reading an image in default mode
image = cv2.imread(path)

# Window name in which image is displayed
window_name = 'Image'

# Start coordinate, here (5, 5)
# represents the top left corner of rectangle
# 322 2310 323 2295

# 465 634 690 481

start_point = (465, 634)

# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangle
end_point = (690, 481)

# Blue color in BGR
color = (0, 0, 255)

# Line thickness of 2 px
thickness = 9

# Using cv2.rectangle() method
# Draw a rectangle with blue line borders of thickness of 2 px
image = cv2.rectangle(image, start_point, end_point, color, thickness)

# Displaying the image
cv2.imshow(window_name, image)
cv2.waitKey(0)
cv2.imwrite("Bloceufu.jpg", image)
