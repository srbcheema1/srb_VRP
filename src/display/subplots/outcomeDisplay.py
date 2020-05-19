class OutcomeDisplay:
	def __init__(self,ax):
		self.ax = ax

	def plot_learning(self,sa_history,aco_history,saco_history,skmean_history,graph):
		self.ax.plot([i for i in range(len(saco_history))], [graph.path_cost(i) for i in saco_history],'m-')
		line_sa = self.ax.axhline(y=graph.path_cost(sa_history[-1]), color='r', linestyle='--')
		line_aco = self.ax.axhline(y=graph.path_cost(aco_history[-1]), color='y', linestyle='--')
		line_saco = self.ax.axhline(y=graph.path_cost(saco_history[-1]), color='c', linestyle='--')
		line_skmean = self.ax.axhline(y=graph.path_cost(skmean_history[-1]), color='g', linestyle='--')
		self.ax.legend([line_sa,line_aco,line_saco,line_skmean], 
					['SA','ACO','ACO-SA','KMean-SA'])
		self.ax.set(xlabel='iteration', ylabel='cost')