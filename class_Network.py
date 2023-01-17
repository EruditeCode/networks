# A Network class to support the network visualisation program. 

from class_Node import Node
from random import randint
from collections import deque

class Network:
	def __init__(self, width, height, height_min=0, network_map={}):
		# 0 = node, 1 = edge, 2 = edit, 3 = path.
		self.state = 0
		self.height_min = height_min

		self.start = None
		self.path = None
		self.nodes = {}
		for key in network_map.keys():
			self.nodes[key] = Node(key, randint(15, width), randint(height_min+15, height), 15, network_map[key])

	def update(self, mouse_position, mouse_down, mouse_click):
		if self.state == 2 and mouse_down:
			for key in self.nodes.keys():
				self.nodes[key].update_mobility(mouse_position)
		elif self.state == 2 and not mouse_down:
			for key in self.nodes.keys():
				self.nodes[key].update_position(mouse_position)
		elif self.state == 3 and mouse_click:
			for key in self.nodes.keys():
				if self.nodes[key].is_selected(mouse_position):
					if self.start == None:
						self.start = key
					else:
						self.path = self.find_path(self.start, key)
						self.start = None
					break
		elif self.state == 0 and mouse_click and mouse_position[1] > self.height_min:
			# Need to add the right click to remove...
			if self.nodes == {}:
				num = 0
				self.nodes[num] = Node(str(num), mouse_position[0], mouse_position[1], 15, [])
			else:
				num = max(self.nodes) + 1
				self.nodes[num] = Node(str(num), mouse_position[0], mouse_position[1], 15, [])
		elif self.state == 1 and mouse_click and mouse_position[1] > self.height_min:
			for key in self.nodes.keys():
				if self.nodes[key].is_selected(mouse_position):
					if self.start == None:
						self.start = key
					else:
						if self.start != key and key not in self.nodes[self.start].connections:
							self.nodes[self.start].connections.append(key)
						if self.start not in self.nodes[key].connections:
							self.nodes[key].connections.append(self.start)
						self.start = None
					break

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
