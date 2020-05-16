import math
import random

from graph import Graph


class SimulatedAnnealing:
	def __init__(self, graph:Graph, init_soln, alpha, temp, stopping_temp, stopping_iter):
		self.graph = graph #array_like,list of coordinates
		self.sample_size = len(graph.cities)
		self.temp = temp #initial temperature
		self.alpha = alpha #rate at which temp decreases
		self.stopping_temp = stopping_temp
		self.stopping_iter = stopping_iter
		self.iteration = 1

		self.curr_solution = init_soln
		self.history = [self.curr_solution]
		self.curr_weight = self.graph.path_cost(self.curr_solution)
		self.min_weight = self.curr_weight


	def acceptance_probability(self, candidate_weight):
		return math.exp(-abs(candidate_weight - self.curr_weight) / self.temp)


	def accept(self, candidate):
		candidate_weight = self.graph.path_cost(candidate)
		if candidate_weight < self.curr_weight:
			self.curr_weight = candidate_weight
			self.curr_solution = candidate
			if candidate_weight < self.min_weight:
				self.min_weight = candidate_weight
				self.history.append(candidate)
		elif random.random() < self.acceptance_probability(candidate_weight):
			self.curr_weight = candidate_weight
			self.curr_solution = candidate


	def anneal(self):
		while self.temp >= self.stopping_temp and self.iteration < self.stopping_iter:
			candidate = list(self.curr_solution)
			l = random.randint(2, self.sample_size - 1)
			i = random.randint(0, self.sample_size - l)
			candidate[i: (i + l)] = reversed(candidate[i: (i + l)])

			self.accept(candidate)
			self.temp *= self.alpha
			self.iteration += 1

		self.print_summary()
		return self.history


	def print_summary(self):
		initial_weight = self.graph.path_cost(self.history[0])
		print('Intial weight: ', initial_weight)
		print('Minimum weight: ', self.min_weight)
		print('Improvement: ', round((initial_weight - self.min_weight) / (initial_weight), 4) * 100, '%')