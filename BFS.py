# A program script to explore the breadth first search algorithm.

# Walkthrough Video Link: https://www.youtube.com/watch?v=E3DFkn8p3N8

from collections import deque

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

def bfs(start_pos, network):
	visited = []
	queue = deque([start_pos])

	while queue:
		present = queue.popleft()
		visited.append(present)
		for node in network[present]:
			if node not in visited and node not in queue:
				queue.append(node)

	return visited

test = bfs("a", net_map)
print(test)
