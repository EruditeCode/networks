# A Network class to support the network visualisation program. 

from class_Node import Node
from random import randint
from collections import deque

class Network:
	def __init__(self, network_map, width, height):
		self.is_editing = True
		self.is_selecting = False
		self.start, self.end = None, None
		self.path = None
		self.nodes = {}
		for key in network_map.keys():
			self.nodes[key] = Node(key, randint(0, width), randint(0, height), 15, network_map[key])

	def update(self, mouse_position, mouse_down, start_end):
		if self.is_editing and mouse_down:
			for key in self.nodes.keys():
				self.nodes[key].update_mobility(mouse_position)
		elif self.is_editing and not mouse_down:
			for key in self.nodes.keys():
				self.nodes[key].update_position(mouse_position)
		elif self.is_selecting and start_end:
			for key in self.nodes.keys():
				if self.nodes[key].is_selected(mouse_position):
					if self.start == None:
						self.start = key
					else:
						self.end = key
					break

		if self.start and self.end:
			self.path = self.find_path(self.start, self.end)
			self.start, self.end = None, None

	def mobility_reset(self):
		for key in self.nodes.keys():
			self.nodes[key].is_mobile = False

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
