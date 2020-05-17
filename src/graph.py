import math

class Graph(object):
	def __init__(self, cities: list):
		self.cities = cities
		self.cost = Graph.cost_matrix(cities)
		self.size = len(self.cities)
		self.pheromone = [[1 for j in range(self.size)] for i in range(self.size)]


	@staticmethod
	def distance(a, b):
		return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


	@staticmethod
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


	def minimumSpanningTree(self):
		parent = [-1 for i in range(self.size)]
		included = [False for i in range(self.size)]
		dist_from_tree = [10**9 for i in range(self.size)]
		dist_from_tree[0] = 0

		def _nearest_city():
			min_dist = 10**9
			min_index = -1
			for i in range(len(dist_from_tree)):
				if(included[i] == False and dist_from_tree[i] < min_dist):
					min_dist = dist_from_tree[i]
					min_index = i
			return min_index

		for _ in range(self.size):
			u = _nearest_city()
			included[u] = True
			for v in range(self.size):
				if(included[v] == False and dist_from_tree[v] > self.cost[u][v]):
					dist_from_tree[v] = self.cost[u][v]
					parent[v] = u
		
		cost = 0
		lines = []
		for _ in range(1,self.size):
			cost += self.cost[_][parent[_]]
			lines.append([(self.cities[_].x,self.cities[_].y), (self.cities[parent[_]].x,self.cities[parent[_]].y)])
		return cost,lines,parent


	def path_cost(self,path):
		cost = 0
		for index in range(1, len(path)):
			i = path[index-1]
			j = path[index]
			cost += self.cost[i][j]
		cost += self.cost[path[0]][path[-1]] #round trip
		return cost

	def get_indices(self,path):
		return [self.cities[i].index for i in path]
