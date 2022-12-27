import pygame
from random import randint

net_map = {
	"a":["b", "c", "f"],
	"b":["a", "d", "e"],
	"c":["a", "h"],
	"d":["b", "g"],
	"e":["b", "f"],
	"f":["a", "e"],
	"g":["d"],
	"h":["c"],
}

class Node:
	def __init__(self, label, x, y, radius):
		self.label = label
		self.pos = (x, y)
		self.radius = radius
		self.connections = []

def main():
	# Initialise pygame settings
	pygame.init()
	WIDTH, HEIGHT = 800, 400
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Visual Sorts")
	clock = pygame.time.Clock()
	font = pygame.font.Font(None, 20)

	# Creating the background surfaces for the interface.
	bg = pygame.Surface((WIDTH, HEIGHT))
	bg.fill((20, 20, 20))

	# Initialising the nodes.
	nodes = []
	for key in net_map.keys():
		nodes.append(Node(key, randint(0, WIDTH), randint(0, HEIGHT), 15))

	for node in nodes:
		connections = []
		for value in net_map[node.label]:
			for nodecheck in nodes:
				if nodecheck.label == value:
					connections.append(nodecheck)
		node.connections = connections


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		screen.blit(bg, (0, 0))

		for node in nodes:
			for connection in node.connections:
				pygame.draw.aaline(screen, (150,150,150), node.pos, connection.pos)

		for node in nodes:
			pygame.draw.circle(screen, (255,255,255), node.pos, node.radius)
			text = font.render(node.label, True, (0,0,0))
			textRect = text.get_rect()
			textRect.center = node.pos
			screen.blit(text, textRect)

		pygame.display.update()
		clock.tick(30)


if __name__ == "__main__":
	main()
