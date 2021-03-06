class PartitionDisplay():
	def __init__(self,ax):
		self.ax = ax

	def plot_partitions(self,clusters,origin):
		x,y,c = [],[],[]
		colmap = {0:'r', 1: 'g', 2: 'b', 3: 'y',4:'c',5:'m'}
		self.ax.scatter(origin.x,origin.y,color='k',edgecolor='k')
		for i,cluster in enumerate(clusters):
			self.ax.scatter(cluster.mean_point.x,cluster.mean_point.y,color=colmap[i],edgecolor='k')
			for point in cluster.points:
				x.append(point.x)
				y.append(point.y)
				c.append(colmap[i])
		self.ax.set_xlim(0, (max(x)+2) * 1.1)
		self.ax.set_ylim(0, (max(y)+2)* 1.1)
		self.ax.scatter(x, y, color=c, alpha=0.5)