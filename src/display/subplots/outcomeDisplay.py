class OutcomeDisplay:
	def __init__(self,ax):
		self.ax = ax

	def plot_learning(self,history,a_history,graph):
		self.ax.plot([i for i in range(len(history))], [graph.path_cost(i) for i in history])
		line_init = self.ax.axhline(y=graph.path_cost(history[0]), color='y', linestyle='--')
		line_min = self.ax.axhline(y=graph.path_cost(history[-1]), color='g', linestyle='--')
		line_aco = self.ax.axhline(y=graph.path_cost(a_history[-1]), color='c', linestyle='--')
		self.ax.legend([line_init, line_min,line_aco], 
					['NNA cost', 'SA cost','aco cost'])
		self.ax.set(xlabel='iteration', ylabel='cost')