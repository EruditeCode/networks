
class Node:
	def __init__(self, label, x, y, radius, connections):
		self.label = label
		self.pos = (x, y)
		self.radius = radius
		self.connections = connections
		self.is_mobile = False

	def update_position(self, point):
		if self.is_mobile:
			self.pos = point

	def update_mobility(self, point):
		if self.is_selected(point):
			self.is_mobile = True

	def is_selected(self, point):
		if self.euclidean_distance(self.pos, point) <= self.radius:
			return True
		return False

	def euclidean_distance(self, point_1, point_2):
		s = 0.0
		for i in range(len(point_1)):
			s += ((point_1[i] - point_2[i]) ** 2)
		return s ** 0.5
