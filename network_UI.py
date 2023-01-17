import pygame
from random import randint
from class_Network import Network
from class_Utilities import Button

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
	network = Network(WIDTH, HEIGHT, 100)

	# Creating the buttons.
	buttons = []
	buttons.append(Button("NODE", 25, 25, 50, 50, True))
	buttons.append(Button("EDGE", 90, 25, 50, 50))
	buttons.append(Button("MOVE", 155, 25, 50, 50))
	buttons.append(Button("PATH", 220, 25, 50, 50))
	btn_surface = pygame.Surface((50,50))

	mouse_down = False
	mouse_click = False
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and network.state == 2:
				mouse_down = True
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_click = True
				mouse_position = pygame.mouse.get_pos()
				for index, button in enumerate(buttons):
					if button.check_click(mouse_position):
						network.state = index
						network.start, network.path = None, None
				if network.state == 2:
					network.mobility_reset()

		# Update buttons.
		for button in buttons:
			button.status = False
		buttons[network.state].status = True

		screen.blit(bg, (0, 0))
		screen.blit(menu, (0, 0))

		# Displaying buttons.
		for button in buttons:
			if button.status:
				color = (255, 110, 40)
			else:
				color = (0, 86, 62)
			btn_surface.fill(color)
			screen.blit(btn_surface, button.pos)
			text = font.render(button.text, True, (255,255,255))
			textRect = text.get_rect()
			textRect.center = (button.pos[0]+25, button.pos[1]+25)
			screen.blit(text, textRect)

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
		network.update(mouse_position, mouse_down, mouse_click)
		mouse_down, mouse_click = False, False

		pygame.display.update()
		clock.tick(30)


if __name__ == "__main__":
	main()
