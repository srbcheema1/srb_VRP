import matplotlib.pyplot as plt
import time

class DynamicPlot():
	def __init__(self):
		plt.ion() # plot interactive mode ON
		self.figure, self.ax = plt.subplots(2,2)
		self.cyan_line, = self.ax[1,0].plot([],[], 'co-') # intermediate path
		self.green_line, = self.ax[1,0].plot([],[], 'go-') # final path
		self.red_line, = self.ax[1,0].plot([],[], 'ro') # depot
		self.a_cyan_line, = self.ax[0,1].plot([],[], 'co-') # intermediate path
		self.a_green_line, = self.ax[0,1].plot([],[], 'go-') # final path
		self.a_red_line, = self.ax[0,1].plot([],[], 'ro') # depot
		self.ax[0,0].set_title("partitions")
		self.ax[0,1].set_title("Ant Colony Optimmization")
		self.ax[1,0].set_title("Simulated Annealing")
		self.ax[1,1].set_title("Optmimization")

	def get_xy(self,cities,p_path:list):
		x, y = [], []
		path = p_path[:]
		path.append(path[0])
		for index in range(0, len(path)):
			city = cities[path[index]]
			x.append(city.x)
			y.append(city.y)
		return x,y

	def set_lim(self,x0,x1,y0,y1,ax):
		ax.set_xlim(x0, x1)
		ax.set_ylim(y0, y1)

	def a_plot(self, cities, path: list):
		x, y = self.get_xy(cities,path)
		self.a_cyan_line.set_data(x, y)
		self.a_red_line.set_data([cities[0].x],[cities[0].y])
		self._flush()

	def a_plot_final(self,cities,path:list):
		x, y = self.get_xy(cities,path)
		self.a_cyan_line.set_data([], [])
		self.a_green_line.set_data(x,y)
		self.a_red_line.set_data([cities[0].x],[cities[0].y])
		self._flush()

	def plot(self, cities, path: list):
		x, y = self.get_xy(cities,path)
		self.cyan_line.set_data(x, y)
		self.red_line.set_data([cities[0].x],[cities[0].y])
		self._flush()

	def plot_final(self,cities,path:list):
		x, y = self.get_xy(cities,path)
		self.cyan_line.set_data([], [])
		self.green_line.set_data(x,y)
		self.red_line.set_data([cities[0].x],[cities[0].y])
		self._flush()
	
	def plot_partitions(self,partitions,origin):
		x,y,c = [],[],[]
		colmap = {0:'r', 1: 'g', 2: 'b', 3: 'y',4:'c',5:'m'}
		self.ax[0,0].scatter(origin.x,origin.y,color='k',edgecolor='k')
		for i,part in enumerate(partitions):
			self.ax[0,0].scatter(part.mean_point.x,part.mean_point.y,color=colmap[i],edgecolor='k')
			for city in part.cities:
				x.append(city.x)
				y.append(city.y)
				c.append(colmap[i])
		self.ax[0,0].scatter(x, y, color=c, alpha=0.5)


	def show(self,cities,history,a_history,graph,partitions):
		self.plot_partitions(partitions,cities[0])
		x, y = self.get_xy(cities,history[0])
		self.set_lim(0, (max(x)+2) * 1.1, 0, (max(y)+2)* 1.1, self.ax[0,0])
		self.set_lim(0, (max(x)+2) * 1.1, 0, (max(y)+2)* 1.1, self.ax[0,1])
		self.set_lim(0, (max(x)+2) * 1.1, 0, (max(y)+2)* 1.1, self.ax[1,0])

		for i in range(max(len(a_history),len(history))):
			if(i == len(a_history)-1):
				self.a_plot_final(cities,a_history[i])
			if(i<len(a_history)-1):
				self.a_plot(cities,a_history[i])
			if(i == len(history)-1):
				self.plot_final(cities,history[i])
			if(i<len(history)-1):
				self.plot(cities,history[i])
			time.sleep(1)

		self.plot_learning(history,a_history,graph)
		self.end()

	def plot_learning(self,history,a_history,graph):
		self.ax[1,1].plot([i for i in range(len(history))], [graph.path_cost(i) for i in history])
		line_init = self.ax[1,1].axhline(y=graph.path_cost(history[0]), color='y', linestyle='--')
		line_min = self.ax[1,1].axhline(y=graph.path_cost(history[-1]), color='g', linestyle='--')
		line_aco = self.ax[1,1].axhline(y=graph.path_cost(a_history[-1]), color='c', linestyle='--')
		self.ax[1,1].legend([line_init, line_min,line_aco], 
					['NNA cost', 'SA cost','aco cost'])
		self.ax[1,1].set(xlabel='iteration', ylabel='cost')

	def end(self):
		plt.ioff()
		plt.show()

	def _flush(self):
		#We need to draw *and* flush0
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()