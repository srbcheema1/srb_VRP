class PartitionDisplay():
	def __init__(self,ax):
		self.ax = ax

	def plot_partitions(self,partitions,origin):
		x,y,c = [],[],[]
		colmap = {0:'r', 1: 'g', 2: 'b', 3: 'y',4:'c',5:'m'}
		self.ax.scatter(origin.x,origin.y,color='k',edgecolor='k')
		for i,part in enumerate(partitions):
			self.ax.scatter(part.mean_point.x,part.mean_point.y,color=colmap[i],edgecolor='k')
			for city in part.cities:
				x.append(city.x)
				y.append(city.y)
				c.append(colmap[i])
		self.ax.set_xlim(0, (max(x)+2) * 1.1)
		self.ax.set_ylim(0, (max(y)+2)* 1.1)
		self.ax.scatter(x, y, color=c, alpha=0.5)