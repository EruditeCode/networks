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

	# Creating the background surface for the interface.
	bg = pygame.Surface((WIDTH, HEIGHT))
	bg.fill((20, 20, 20))
	menu = pygame.Surface((WIDTH, 100))
	menu.fill((100,100,100))

	# Function to assist with displaying text.
	def draw_text(text, size, x, y, color):
		font = pygame.font.Font(None, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.center = (x, y)
		screen.blit(text_surface, text_rect)

	# Initialising the network.
	network = Network(WIDTH, HEIGHT, 100)

	# Creating the buttons.
	buttons = []
	buttons.append(Button("NODE", 25, 25, 50, 50, True))
	buttons.append(Button("EDGE", 90, 25, 50, 50))
	buttons.append(Button("MOVE", 155, 25, 50, 50))
	buttons.append(Button("PATH", 220, 25, 50, 50))
	btn_surface = pygame.Surface((50,50))

	show_weights = True
	weight_edit = False
	store_weight = ""

	mouse_down, mouse_click = False, False
	click_type = 0
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN and network.state == 2:
				mouse_down = True
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					click_type = 0
				elif event.button == 3:
					click_type = 1
				mouse_click = True
				weight_edit = False
				if store_weight:
					network.update_edge_weight(store_weight)
				store_weight = ""
			if event.type == pygame.KEYDOWN:
				if not weight_edit:
					for label in network.edge_labels:
						if label.editable == True:
							weight_edit = True
				if weight_edit and event.unicode.isdigit():
					store_weight += str(event.unicode)

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
			draw_text(button.text, 20, button.pos[0]+25, button.pos[1]+25, (255,255,255))

		# Displaying the connections between the nodes.
		for key in network.nodes.keys():
			for node in network.nodes[key].connections:
				pygame.draw.aaline(screen, (255,255,255), network.nodes[key].pos, network.nodes[node].pos)

		if network.path:
			for i in range(0, len(network.path)-1):
				posA = network.nodes[network.path[i]].pos
				posB = network.nodes[network.path[i+1]].pos
				pygame.draw.line(screen, (255,255,0), posA, posB, 5)

		if show_weights:
			for label in network.edge_labels:
				if label.editable == True: # Should move the label positions here, not in the class.
					draw_text(store_weight, 25, label.pos[0], label.pos[1], (240,0,0))
				else:
					draw_text(str(label.weight), 25, label.pos[0], label.pos[1], (0,240,0))

		# Displaying the nodes and their labels.
		for key in network.nodes.keys():
			pygame.draw.circle(screen, (255,255,255), network.nodes[key].pos, network.nodes[key].radius)
			draw_text(network.nodes[key].label, 21, network.nodes[key].pos[0], network.nodes[key].pos[1], (0,0,0))

		mouse_position = pygame.mouse.get_pos()
		if mouse_click:
			for index, button in enumerate(buttons):
				if button.check_click(mouse_position):
					network.state = index
					network.start, network.path = None, None
					mouse_click = False
		network.update(mouse_position, mouse_down, mouse_click, click_type)
		mouse_down, mouse_click = False, False

		pygame.display.update()
		clock.tick(30)


if __name__ == "__main__":
	main()
