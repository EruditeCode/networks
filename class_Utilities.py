# A file to store many small but useful classes.

class Button:
	def __init__(self, text, x, y, width, height, status:bool=False):
		self.text = text
		self.pos = (x, y)
		self.width = width
		self.height = height
		self.status = status

	def check_click(self, click_position):
		if (self.pos[0] + self.width >= click_position[0] >= self.pos[0] and
			self.pos[1] + self.height >= click_position[1] >= self.pos[1]):
			return True
		return False

class EdgeLabel:
	def __init__(self, width, height, nodes, nodes_dict):
		self.width = width
		self.height = height
		self.nodes = nodes
		self.weight = None
		self.pos = None
		self.editable = False

		self.update(nodes_dict)

	def update(self, nodes_dict):
		# Update position.
		posA = nodes_dict[self.nodes[0]].pos
		posB = nodes_dict[self.nodes[1]].pos
		self.pos = ((posA[0] + posB[0])//2, ((posA[1] + posB[1])//2)-15)

		# Update weight.
		self.weight = nodes_dict[self.nodes[0]].weights[self.nodes[1]]

	def check_click(self, click_position):
		if (self.pos[0] + self.width//2 >= click_position[0] >= self.pos[0] - self.width//2 and
			self.pos[1] + self.height//2 >= click_position[1] >= self.pos[1] - self.height//2):
			return True
		return False
