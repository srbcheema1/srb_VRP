import random

from graph import Graph

class ACO(object):
	def __init__(self, ant_count: int, generations: int, quantity: int, alpha: list, beta: list, decay: list):
		self.quantity = quantity #pheromone intensity
		self.ant_count = ant_count
		self.generations = generations
		#these will vary with generations
		self.decay = decay[0] #evaporation or decay of phermone
		self.beta = beta[0] #relative importance of heuristic information
		self.alpha = alpha[0] #relative importance of pheromone
		self.decay_p = decay
		self.alpha_p = alpha
		self.beta_p = beta


	def _update_parameters(self,gen):
		self.decay = self.decay_p[0] + (self.decay_p[1]-self.decay_p[0])*gen/self.generations
		self.alpha = self.alpha_p[0] + (self.alpha_p[1]-self.alpha_p[0])*gen/self.generations
		self.beta = self.beta_p[0] + (self.beta_p[1]-self.beta_p[0])*gen/self.generations


	def _update_pheromone(self, graph: Graph, ants: list):
		for i, row in enumerate(graph.pheromone):
			for j, col in enumerate(row):
				graph.pheromone[i][j] *= self.decay
				ants.sort()
				best_ants = ants[:len(ants)//3]
				for ant in best_ants:
					graph.pheromone[i][j] += ant.pheromone_delta[i][j]


	def solve(self, graph: Graph):
		history = []
		best_cost = float('inf')
		for gen in range(self.generations):
			self._update_parameters(gen)
			ants = [_Ant(self, graph) for i in range(self.ant_count)]
			for ant in ants:
				cost = ant.travel()
				if cost < best_cost:
					best_cost = cost
					history.append([] + ant.path)
			self._update_pheromone(graph, ants)
		return history, best_cost



class _Ant(object):
	def __init__(self, aco: ACO, graph: Graph):
		self.aco = aco
		self.graph = graph

		self.pheromone_delta = []  # the local increase of pheromone
		self.allowed = {i for i in range(graph.size)}  # nodes which are allowed for the next selection
		self.ease = [[0 if i == j else 1 + (10 / graph.cost[i][j]) for j in range(graph.size)] for i in range(graph.size)]  # heuristic information
		self.capacity = 0
		self.max_capacity = 10

		self.path = []  # path list
		self.cost = 0 # path cost by ant

		self.curr = 0
		self.path.append(self.curr)
		self.allowed.remove(self.curr)


	def travel(self):
		while self.allowed:
			self._select_next()
		self._update_pheromone_delta()
		self.cost = self.graph.path_cost(self.path)
		return self.cost


	def _unload(self):
		self.path.append(0)
		self.capacity = 0
		self.curr = 0


	def _select_next(self):
		if(self.capacity > self.max_capacity):
			self._unload()

		denominator = 0
		for i in self.allowed:
			denominator += (1+self.graph.pheromone[self.curr][i])**self.aco.alpha \
											* self.ease[self.curr][i]**self.aco.beta \
											* self._clustoring_factor(i)


		probabilities = [0 for i in range(self.graph.size)]  # probabilities for moving to a node in the next step
		for i in self.allowed:
			probabilities[i] = (1+self.graph.pheromone[self.curr][i])**self.aco.alpha * self.ease[self.curr][i]**self.aco.beta \
													* self._clustoring_factor(i) / denominator

		self.curr = self._select_according_to_probability(probabilities)
		self.allowed.remove(self.curr)
		self.path.append(self.curr)
		self.capacity = self.capacity + 1
 
	def _clustoring_factor(self,i):
		if(self.curr == 0):
			return 1
		filled = self.capacity/self.max_capacity
		far_fact = (abs(filled-1/2)*4 - 1) * (-1)
		return (1+self.graph.cost[self.curr][0])**(far_fact/4)

	def _select_according_to_probability(self,probabilities):
		rand = random.random()
		for i, probability in enumerate(probabilities):
			rand -= probability
			if rand <= 0:
				return i


	def _update_pheromone_delta(self):
		self.pheromone_delta = [[0 for j in range(self.graph.size)] for i in range(self.graph.size)]
		for _ in range(1, len(self.path)):
			i = self.path[_ - 1]
			j = self.path[_]
			self.pheromone_delta[i][j] = self.aco.quantity

	def __lt__(self, other):
		return self.cost < other.cost