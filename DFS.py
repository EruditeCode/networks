# A program script to explore the depth first search algorithm.

# Walkthrough Video Link: https://www.youtube.com/watch?v=E3DFkn8p3N8

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

def dfs(start_pos, network):
	visited = []
	stack = [start_pos]

	while stack:
		present = stack.pop()
		visited.append(present)
		for node in network[present]:
			if node not in visited and node not in stack:
				stack.append(node)

	return visited

test = dfs("a", net_map)
print(test)
