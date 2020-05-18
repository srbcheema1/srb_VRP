class OutcomeDisplay:
	def __init__(self,ax):
		self.ax = ax

	def plot_learning(self,s_history,aco_history,saco_history,graph):
		self.ax.plot([i for i in range(len(s_history))], [graph.path_cost(i) for i in s_history],'m-',
								[i for i in range(len(saco_history))], [graph.path_cost(i) for i in saco_history],'b-')
		line_nna = self.ax.axhline(y=graph.path_cost(s_history[0]), color='r', linestyle='--')
		line_min = self.ax.axhline(y=graph.path_cost(s_history[-1]), color='g', linestyle='--')
		line_aco = self.ax.axhline(y=graph.path_cost(aco_history[-1]), color='y', linestyle='-')
		line_saco = self.ax.axhline(y=graph.path_cost(saco_history[-1]), color='c', linestyle='--')
		self.ax.legend([line_nna, line_min,line_aco,line_saco], 
					['NNA', 'SA','ACO','ACO-SA'])
		self.ax.set(xlabel='iteration', ylabel='cost')