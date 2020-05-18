import math
import random

from .graph import Graph


class SimulatedAnnealing:
	def __init__(self, graph:Graph, init_soln, alpha, temp, stopping_temp, stopping_iter):
		self.temp = temp #initial temperature
		self.alpha = alpha #rate at which temp decreases
		self.stopping_temp = stopping_temp
		self.stopping_iter = stopping_iter
		self.iteration = 1

		self.graph = graph
		self.curr_solution = self.create_clusters(init_soln)
		self.history = [self.combined_path(self.curr_solution)]
		self.curr_weight = self.graph.path_cost(self.combined_path(self.curr_solution))
		self.min_weight = self.curr_weight


	def create_clusters(self,path):
		clusters = []
		path = path[1:] + [0]
		loc_path = [0]
		for val in path:
			if(val == 0):
				clusters.append(loc_path)
				loc_path = [0]
			else:
				loc_path.append(val)
		return clusters


	def combined_path(self,paths):
		full_path = []
		for path in paths:
			full_path.extend(path)
		return full_path


	def acceptance_probability(self, candidate_weight):
		return math.exp(-abs(candidate_weight - self.curr_weight) / self.temp)


	def accept(self, candidate):
		candidate_weight = self.graph.path_cost(self.combined_path(candidate))
		if candidate_weight < self.curr_weight:
			self.curr_weight = candidate_weight
			self.curr_solution = candidate
			if candidate_weight < self.min_weight:
				self.min_weight = candidate_weight
				self.history.append(self.combined_path(candidate))
		elif random.random() < self.acceptance_probability(candidate_weight):
			self.curr_weight = candidate_weight
			self.curr_solution = candidate


	def get_candidate(self):
		candidate = []
		for path in self.curr_solution:
			candidate.append(path[:])
		way = random.randint(0,1)
		if(way == 0):
			i = random.randint(0,len(candidate)-1)
			j = random.randint(0,len(candidate)-1)
			ia = random.randint(1,len(candidate[i])-1)
			jb = random.randint(1,len(candidate[j])-1)
			candidate[i][ia], candidate[j][jb] = candidate[j][jb],candidate[i][ia]
		else:
			i = random.randint(0,len(candidate)-1)
			if(len(candidate[i]) < 3):
				return candidate
			b = random.randint(2, len(candidate[i])- 1)
			a = random.randint(1, len(candidate[i]) - b)
			candidate[i][a: (a + b)] = reversed(candidate[i][a: (a + b)])
		return candidate


	def anneal(self):
		while self.temp >= self.stopping_temp and self.iteration < self.stopping_iter:
			candidate = self.get_candidate()
			self.accept(candidate)
			self.temp *= self.alpha
			self.iteration += 1
		return self.history,self.min_weight