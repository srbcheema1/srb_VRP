import math

class Graph(object):
	def __init__(self, cities: list):
		self.cities = cities
		self.cost = Graph.cost_matrix(cities)
		self.size = len(self.cities)
		self.pheromone = [[1 for j in range(self.size)] for i in range(self.size)]


	def distance(a, b):
		return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


	def cost_matrix(cities):
		cost_matrix = []
		rank = len(cities)
		for i in range(rank):
			row = []
			for j in range(rank):
				row.append(Graph.distance(cities[i], cities[j]))
			cost_matrix.append(row)
		return cost_matrix


	def nearestNeighbourSolution(self):
		node = 0
		result = [node]
		nodes_to_visit = set(range(len(self.cost)))
		nodes_to_visit.remove(node)

		while nodes_to_visit:
			nearest_node = min([(self.cost[node][j], j) for j in nodes_to_visit], key=lambda x: x[0])
			node = nearest_node[1]
			nodes_to_visit.remove(node)
			result.append(node)

		return result


	def path_cost(self,path):
		cost = 0
		for index in range(1, len(path)):
			i = path[index-1]
			j = path[index]
			cost += self.cost[i][j]
		cost += self.cost[path[0]][path[-1]] #round trip
		return cost
