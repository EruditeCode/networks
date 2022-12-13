# A program script to explore pathfinding with the depth first search algorithm.

# Walkthrough Video Link: https://www.youtube.com/watch?v=ips-y8ekRnM

net_map = {
	"a":["b", "c", "f"],
	"b":["a", "d", "f"],
	"c":["a", "h"],
	"d":["b", "g"],
	"e":["b", "f"],
	"f":["a", "e"],
	"g":["d"],
	"h":["c"]
}

def search(start, end, network):
	stack, visited = [start], []
	while stack:
		present = stack.pop()
		visited.append(present)
		for node in network[present]:
			if node == end:
				return visited
			if node not in visited and node not in stack:
				stack.append(node)
	return []

def is_path(start, end, network):
	if search(start, end, network):
		return True
	return False

def find_path(start, end, network):
	visited = search(start, end, network)
	if visited:
		path = [end]
		while start not in path:
			path, visited = build_path(path, visited, network)
		return path
	else:
		return f"No path found between {start} and {end}."

def build_path(path, visited, network):
	for index, node in enumerate(visited):
		if node in network[path[-1]]:
			path.append(node)
			visited = visited[0:index]
			break
	return path, visited


test = find_path("a", "g", net_map)
print(test)
