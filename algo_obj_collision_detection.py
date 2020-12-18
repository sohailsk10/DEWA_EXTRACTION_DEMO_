# rect = [minX, maxX, minY, maxY] # rect.left = minX, rect.right =maxX, rect.top=minY, rect.bottom =maxY
# rect = [minX, maxX, minY, maxY] # rect.left = minX, rect.right =maxX, rect.top=minY, rect.bottom =maxY
# coordinates of the rhombus
# point1 = line_left_x1, line_left_y1,
# point2 = line_left_x2, line_left_y2,
# point3 = line_right_x1, line_right_y1,
# point4 = line_right_x2, line_right_y2

class Object_in_ROI:
	def __init__(self,minX, maxX, minY, maxY, line_left_x1, line_left_y1, line_left_x2, line_left_y2,
	line_right_x1, line_right_y1, line_right_x2, line_right_y2):

		self.P_right = [line_right_x1, line_right_y1]
		self.Q_right = [line_right_x2, line_right_y2]
	#line_right = [P_right, Q_right]  # line_right = [[minX, minY], [maxX, maxY]] for lanes
		self.P_left = [line_left_x1, line_left_y1]
		self.Q_left = [line_left_x2, line_left_y2]
	#line_left = [P_left, Q_left]  # line_left = [[minX, minY], [maxX, maxY]] for lanes
		self.rect = [minX, maxX, minY, maxY] # box for person or object

	def lineFromPoints(self, P, Q):
		a = (Q[1] - (P[1]))
		b = P[0] - Q[0]
		c = a * (P[0]) + b * (P[1])

		if (a/b < 0):
			print("The line passing through points P and Q is:",
			      a, "x ", b, "y = ", c, "\n")
		else:
			print("The line passing through points P and Q is: ",
			      a, "x + ", b, "y = ", c, "\n")

	def getX(self, y, P, Q):
		a = (Q[1] - P[1])
		b = P[0] - Q[0]
		c = a * (P[0]) + b * -1 *  (P[1])
		x = (c - (b * y)) / a
		return x

	def getleftlineX(self, y):
		a = (self.Q_left[1] - self.P_left[1])
		b = self.P_left[0] - self.Q_left[0]
		c = a * (self.P_left[0]) + b * -1 * (self.P_left[1])
		x = (c - (b * y)) / a
		return x

	def getrightlineX(self, y):
		a = (self.Q_right[1] - self.P_right[1])
		b = self.P_right[0] - self.Q_right[0]
		c = a * self.P_right[0] + b * -1 * self.P_right[1]
		x = (c - (b * y)) / a
		return x


	def getSlope(self, P, Q):
		a = (Q[1] - P[1])
		b = P[0] - Q[0]
		slope = a / b
		return slope

	def getrightlineSlope(self):
		a = (self.Q_right[1] - self.P_right[1])
		b = self.P_right[0] - self.Q_right[0]
		slope = a / b
		return slope

	def getleftlineSlope(self):
		a = (self.Q_left[1] - self.P_left[1])
		b = self.P_left[0] - self.Q_left[0]
		slope = a / b
		return slope

	def getY(self, x, P, Q):
		a = (Q[1] - P[1])
		b = P[0] - Q[0]
		c = a * (P[0]) + b * -1 * (P[1])
		y = (c - (a * x)) / b
		return y

	def getrightlineY(self, x):
		a = (self.Q_right[1] - self.P_right[1])
		b = self.P_right[0] - self.Q_right[0]
		c = a * (self.P_right[0]) + b * -1 * self.P_right[1]
		y = (c - (a * x)) / b
		return y

	def getleftlineY(self, x):
		a = (self.Q_left[1] - self.P_left[1])
		b = self.P_left[0] - self.Q_left[0]
		c = a * (self.P_left[0]) + b * -1 * self.P_left[1]
		y = (c - (a * x)) / b
		return y

	def isvoilation(self):
		if self.getSlope(self.P_left, self.Q_left) == 0:
			print("Error slope cannot be zero")
			raise Exception("Error : slope cannot be zero")
		else:
			if self.getX(self.rect[3], self.P_left, self.Q_left) < self.rect[0] \
					< self.getX(self.rect[3], self.P_right, self.Q_right)\
					or \
					self.getX(self.rect[3], self.P_left, self.Q_left) < self.rect[1] \
				< self.getX(self.rect[3], self.P_right, self.Q_right):  # rect = [minX, maxX, minY, maxY] # rect.left = minX, rect.right =maxX, rect.top=minY, rect.bottom =maxY
				return True
			else:
				return False
