import math
import numpy as np

from .const import srb_cap


class Kmean:
	def __init__(self,points,origin,base=0,cap=srb_cap):
		self.origin = origin
		self.points = [Point(point[0],point[1],self.origin,i+base) for i,point in enumerate(points)] # one based indexing, coz 0 is origin
		self.points.sort(key=lambda x: x.theta)
		self.cap = cap
		self.partition = None # partition is set of clusters
		self.compute()


	def compute(self):
		partitions_list = []
		for _ in range(self.cap):
			partition = Partition()
			point_sets = self._radially_sorted_point_sets(_)

			for pset in point_sets:
				cluster = Cluster()
				cluster.mean_point = Point(np.mean([a.x for a in pset]), np.mean([a.y for a in pset]), self.origin)
				partition.clusters.append(cluster)

			#cheap way
			for i,cluster in enumerate(partition.clusters):
				cluster.points = point_sets[i]
			partitions_list.append(partition)
		self.partition = partitions_list[0]


	def _radially_sorted_point_sets(self,offset=0):
		points = self.points[offset:] + self.points[:offset]
		point_sets = []
		cnt = 0
		loc_set = []
		for point in points:
			loc_set.append(point)
			cnt+=1
			if(cnt == self.cap):
				point_sets.append([] + loc_set)
				loc_set = []
				cnt = 0
		if(cnt !=0):
			point_sets.append([] + loc_set)
		return point_sets


class Point:
	def __init__(self,x,y,origin,index=-1):
		self.ox = origin[0]
		self.oy = origin[1]
		self.x = x
		self.y = y
		self.r, self.theta = Point.polar(self.x-self.ox,self.y-self.oy)
		self.index = index
	
	def __str__(self):
		return "(" + str(self.index) + ":" + str(self.x) + "," + str(self.y) + ")"

	def __repr__(self):
		return str(self)


	@staticmethod
	def polar(x,y):
		r = (x ** 2 + y ** 2) ** .5
		theta = math.degrees(math.atan2(y,x))
		return r, theta



class Partition:
	def __init__(self):
		self.clusters = []
		self.variance = 0
		pass



class Cluster:
	def __init__(self):
		self.points = []
		self.mean_point = Point(0,0,[0,0])
		self.variance = 0
	
	def __str__(self):
		return "(" + str(self.mean_point) + ":" + str(len(self.points)) + "::"+ str(self.points) + ")"

	def __repr__(self):
		return str(self)