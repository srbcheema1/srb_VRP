class OutcomeDisplay:
	def __init__(self,ax):
		self.ax = ax

	def plot_learning(self,skmean_history,aco_history,saco_history,free_history,graph):
		self.ax.plot([i for i in range(len(saco_history))], [graph.path_cost(i) for i in saco_history],'m-')
		line_free = self.ax.axhline(y=graph.path_cost(free_history[-1]), color='r', linestyle='--')
		line_skmean = self.ax.axhline(y=graph.path_cost(skmean_history[-1]), color='g', linestyle='--')
		line_aco = self.ax.axhline(y=graph.path_cost(aco_history[-1]), color='y', linestyle='--')
		line_saco = self.ax.axhline(y=graph.path_cost(saco_history[-1]), color='c', linestyle='--')
		self.ax.legend([line_aco,line_free,line_skmean,line_saco], 
					['ACO','free SA','kmean-SA','ACO-SA'])
		self.ax.set(xlabel='iteration', ylabel='cost')