# A Network class to support the network visualisation program. 

from class_Node import Node
from random import randint
from collections import deque

class Network:
	def __init__(self, width, height, height_min=0):
		# 0 = node, 1 = edge, 2 = edit, 3 = path.
		self.state = 0
		self.height_min = height_min
		self.start, self.select = None, None
		self.path = None
		self.nodes = {}

	def update(self, mouse_position, mouse_down, mouse_click, click_type):
		# Update start and select based on click.
		if mouse_click and self.state != 2:
			self.check_if_node_selected(mouse_position)
			if self.start == None:
				self.start = self.select

		# Adding Nodes.
		if self.state == 0 and mouse_click and mouse_position[1] > self.height_min:
			self.add_or_remove_node(mouse_position, click_type)
		# Adding Edges.
		elif self.state == 1 and mouse_click and mouse_position[1] > self.height_min:
			self.add_or_remove_edge(mouse_position, click_type)
		# Moving Nodes Around.
		elif self.state == 2 and mouse_down:
			for key in self.nodes.keys():
				self.nodes[key].update_mobility(mouse_position)
		elif self.state == 2 and not mouse_down and not mouse_click:
			for key in self.nodes.keys():
				self.nodes[key].update_position(mouse_position)
		elif self.state == 2 and mouse_click:
			for key in self.nodes.keys():
				self.nodes[key].is_mobile = False
		# Pathfinding.
		elif self.state == 3 and mouse_click and self.start != self.select:
			self.path = self.find_path(self.start, self.select)
			self.start = None

		self.select = None

	def check_if_node_selected(self, mouse_position):
		for key in self.nodes.keys():
			if self.nodes[key].is_selected(mouse_position):
				self.select = key

	def add_or_remove_node(self, mouse_position, click_type):
		if click_type == 0 and self.nodes == {}:
			self.nodes[1] = Node("1", mouse_position[0], mouse_position[1], 15, [])
		elif click_type == 0 and self.nodes:
			num = max(self.nodes) + 1
			self.nodes[num] = Node(str(num), mouse_position[0], mouse_position[1], 15, [])
		elif click_type == 1 and self.nodes and self.select:
			for key in self.nodes.keys():
				self.remove_edge_from_connections(self.select, key)
			del self.nodes[self.select]

	def add_or_remove_edge(self, mouse_position, click_type):
		if click_type == 0 and self.start != self.select:
			self.add_edge_to_connections(self.start, self.select)
			self.add_edge_to_connections(self.select, self.start)
			self.start = None
		elif click_type == 1 and self.start != self.select:
			self.remove_edge_from_connections(self.start, self.select)
			self.remove_edge_from_connections(self.select, self.start)
			self.start = None

	def remove_edge_from_connections(self, node_start, node_end):
		if node_start in self.nodes[node_end].connections:
			self.nodes[node_end].connections.remove(node_start)

	def add_edge_to_connections(self, node_start, node_end):
		if node_end not in self.nodes[node_start].connections:
			self.nodes[node_start].connections.append(node_end)

	def search(self, start, end):
		queue, visited = deque([start]), []
		while queue:
			present = queue.popleft()
			visited.append(present)
			for node in self.nodes[present].connections:
				if node == end:
					return visited
				if node not in visited and node not in queue:
					queue.append(node)
		return []

	def find_path(self, start, end):
		visited = self.search(start, end)
		if visited:
			path = [end]
			while start not in path:
				path, visited = self.build_path(path, visited, self.nodes[path[-1]].connections)
			return path
		return None

	def build_path(self, path, visited, connections):
		for index, node in enumerate(visited):
			if node in connections:
				path.append(node)
				visited = visited[0:index]
				break
		return path, visited
