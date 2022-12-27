import pygame
from random import randint
from class_Network import Network

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
	network = Network(net_map, WIDTH, HEIGHT)

	mouse_down = False
	start_end = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and network.is_editing:
				mouse_down = True
			if event.type == pygame.MOUSEBUTTONUP:
				if network.is_editing:
					network.mobility_reset()
				elif network.is_selecting:
					start_end = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					network.is_selecting = network.is_editing
					network.is_editing = not network.is_editing
					network.start, network.end, network.path = None, None, None

		screen.blit(bg, (0, 0))

		# Displaying the connections between the nodes.
		for key in network.nodes.keys():
			for node in network.nodes[key].connections:
				pygame.draw.aaline(screen, (150,150,150), network.nodes[key].pos, network.nodes[node].pos)

		if network.path:
			for i in range(0, len(network.path)-1):
				posA = network.nodes[network.path[i]].pos
				posB = network.nodes[network.path[i+1]].pos
				pygame.draw.line(screen, (255,255,0), posA, posB, 5)

		# Displaying the nodes and their labels.
		for key in network.nodes.keys():
			pygame.draw.circle(screen, (255,255,255), network.nodes[key].pos, network.nodes[key].radius)
			text = font.render(network.nodes[key].label, True, (0,0,0))
			textRect = text.get_rect()
			textRect.center = network.nodes[key].pos
			screen.blit(text, textRect)

		mouse_position = pygame.mouse.get_pos()
		network.update(mouse_position, mouse_down, start_end)
		mouse_down, start_end = False, False

		pygame.display.update()
		clock.tick(30)


if __name__ == "__main__":
	main()
