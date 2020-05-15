import matplotlib.pyplot as plt
import time

class DynamicPlot():
	def __init__(self):
		plt.ion() # plot interactive mode ON
		self.figure, self.ax = plt.subplots()
		self.cyan_line, = self.ax.plot([],[], 'co-') # intermediate path
		self.green_line, = self.ax.plot([],[], 'go-') # final path
		self.red_line, = self.ax.plot([],[], 'ro') # depot


	def plot(self, cities, path: list):
		x = []
		y = []

		path.append(path[0])
		for index in range(0, len(path)):
			city = cities[path[index]]
			x.append(city.x)
			y.append(city.y)
		
		self.cyan_line.set_data(x, y)
		self.red_line.set_data([cities[0].x],[cities[0].y])

		self.ax.set_xlim(0, (max(x)+2) * 1.1)
		self.ax.set_ylim(0, (max(y)+2)* 1.1)
		self._flush()


	def plot_final(self,cities,path:list):
		x = []
		y = []

		path.append(path[0])
		for index in range(0, len(path)):
			city = cities[path[index]]
			x.append(city.x)
			y.append(city.y)
		
		self.cyan_line.set_data([], [])
		self.green_line.set_data(x,y)
		self.red_line.set_data([cities[0].x],[cities[0].y])

		self.ax.set_xlim(0, (max(x)+2) * 1.1)
		self.ax.set_ylim(0, (max(y)+2)* 1.1)
		self._flush()
		plt.ioff()
		plt.show()


	def show(self,cities,history):
		for path in history[:-1]:
			self.plot(cities,path)
			time.sleep(1)
		self.plot_final(cities,history[-1])


	def _flush(self):
		#We need to draw *and* flush0
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()