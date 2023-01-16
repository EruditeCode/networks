import pygame
from random import randint
from class_Network import Network
from class_Utilities import Button

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
	WIDTH, HEIGHT = 1280, 650
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Visual Networks")
	clock = pygame.time.Clock()
	font = pygame.font.Font(None, 20)

	# Creating the background surface for the interface.
	bg = pygame.Surface((WIDTH, HEIGHT))
	bg.fill((20, 20, 20))
	menu = pygame.Surface((WIDTH, 100))
	menu.fill((100,100,100))

	# Initialising the network.
	network = Network(net_map, WIDTH, HEIGHT, 100)

	# Creating the buttons. # Make this into a list!
	state_to_buttons = {0:"Node",1:"Edge",2:"Move",3:"Path"}
	buttons = {}
	buttons["Node"] = Button("Node", 25, 25, 50, 50, True)
	buttons["Edge"] = Button("Edge", 90, 25, 50, 50)
	buttons["Move"] = Button("Move", 155, 25, 50, 50)
	buttons["Path"] = Button("Path", 220, 25, 50, 50)
	btn_surface = pygame.Surface((50,50))


	mouse_down = False
	start_end = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and network.state == 2:
				mouse_down = True
			if event.type == pygame.MOUSEBUTTONUP:
				# Check a series of buttons in the header...
				if network.state == 2:
					network.mobility_reset()
				elif network.state == 3:
					start_end = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if network.state == 2:
						network.state = 3
					elif network.state == 3:
						network.state = 2
					network.start, network.end, network.path = None, None, None

		# Update buttons.
		for key in buttons.keys():
			if key == state_to_buttons[network.state]:
				buttons[key].status = True
			else:
				buttons[key].status = False

		screen.blit(bg, (0, 0))
		screen.blit(menu, (0, 0))

		# Displaying buttons.
		for key in buttons.keys():
			if buttons[key].status:
				color = (255, 110, 40)
			else:
				color = (0, 86, 62)
			btn_surface.fill(color)
			screen.blit(btn_surface, buttons[key].pos)

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
