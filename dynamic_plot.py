import matplotlib.pyplot as plt
import time

class DynamicPlot():
	def __init__(self):
		plt.ion() # plot interactive mode ON
		self.figure, self.ax = plt.subplots()
		self.cyan_line, = self.ax.plot([],[], 'co-') # intermediate path
		self.green_line, = self.ax.plot([],[], 'go-') # final path
		self.red_line, = self.ax.plot([],[], 'ro') # depot

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

	def plot(self, cities, path: list):
		x, y = self.get_xy(cities,path)
		
		self.cyan_line.set_data(x, y)
		self.red_line.set_data([cities[0].x],[cities[0].y])

		self.set_lim(0, (max(x)+2) * 1.1, 0, (max(y)+2)* 1.1, self.ax)
		self._flush()


	def plot_final(self,cities,path:list):
		x, y = self.get_xy(cities,path)
		
		self.cyan_line.set_data([], [])
		self.green_line.set_data(x,y)
		self.red_line.set_data([cities[0].x],[cities[0].y])

		self.set_lim(0, (max(x)+2) * 1.1, 0, (max(y)+2)* 1.1, self.ax)
		self._flush()
	
	def plot_partitions(self,partitions,origin):
		x,y,c = [],[],[]
		colmap = {0:'r', 1: 'g', 2: 'b', 3: 'y'}
		self.ax.scatter(origin.x,origin.y,color='k',edgecolor='k')
		for i,part in enumerate(partitions):
			self.ax.scatter(part.mean_point.x,part.mean_point.y,color=colmap[i],edgecolor='k')
			for city in part.cities:
				x.append(city.x)
				y.append(city.y)
				c.append(colmap[i])
		self.ax.scatter(x, y, color=c, alpha=0.5)
		self.end()


	def show(self,cities,history):
		for path in history[:-1]:
			self.plot(cities,path)
			time.sleep(1)
		self.plot_final(cities,history[-1])
		self.end()


	def end(self):
		plt.ioff()
		plt.show()


	def _flush(self):
		#We need to draw *and* flush0
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()