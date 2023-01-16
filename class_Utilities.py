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
