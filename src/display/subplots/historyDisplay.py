class HistoryDisplay:
	def __init__(self,ax,cities,history,flush):
		self.cities = cities
		self.history = history
		self.ax = ax
		self.flush = flush
		self.cyan_line, = self.ax.plot([],[], 'co-') # intermediate path
		self.green_line, = self.ax.plot([],[], 'go-') # final path
		self.red_line, = self.ax.plot([],[], 'ro') # depot
		self.set_lim()


	def get_xy(self,p_path:list):
		x, y = [], []
		path = p_path[:]
		path.append(path[0])
		for index in range(0, len(path)):
			city = self.cities[path[index]]
			x.append(city.x)
			y.append(city.y)
		return x,y


	def set_lim(self):
		x, y = self.get_xy(self.history[0])
		self.ax.set_xlim(0, (max(x)+2) * 1.1)
		self.ax.set_ylim(0, (max(y)+2)* 1.1)


	def plot(self, path: list):
		x, y = self.get_xy(path)
		self.cyan_line.set_data(x, y)
		self.red_line.set_data([self.cities[0].x],[self.cities[0].y])
		self.flush()


	def plot_final(self,path:list):
		x, y = self.get_xy(path)
		self.cyan_line.set_data([], [])
		self.green_line.set_data(x,y)
		self.red_line.set_data([self.cities[0].x],[self.cities[0].y])
		self.flush()
