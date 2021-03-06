import math
import numpy as np
from random import shuffle

from .const import srb_cap, inf


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
				cluster = Cluster(self.origin)
				cluster.mean_point = Point(np.mean([a.x for a in pset]), np.mean([a.y for a in pset]), self.origin)
				partition.clusters.append(cluster)

			#cheap way
			# for i,cluster in enumerate(partition.clusters):
			# 	cluster.points = point_sets[i]
			# 	cluster.calc_variance()

			self.fill_partition(partition,point_sets)
			partition.calc_variance()
			partitions_list.append(partition)

		partitions_list.sort()
		self.partition = partitions_list[0]
	
	def fill_partition(self,partition,point_sets):
		for _ in range(6):
			for cluster in partition.clusters:
				cluster.points = []
			self.fill_clusters(partition,point_sets)
			point_sets = []
			for cluster in partition.clusters:
				point_sets.append(cluster.points[:])
		
		for cluster in partition.clusters:
			cluster.calc_variance()

	def fill_clusters(self,partition,point_sets):
		for point_set in point_sets:
			shuffle(point_set)
		pt_list = []
		for i in range(max([len(x) for x in point_sets])):
			for point_set in point_sets:
				if(i < len(point_set)):
					pt_list.append(point_set[i])
		
		for pt in pt_list:
			dist = [(inf+1,0) for _ in range(len(partition.clusters))]
			for i,cluster in enumerate(partition.clusters):
				if(len(cluster.points) == self.cap):
					dist[i] = (inf,i)
					continue
				dist[i] = (pt.distance(cluster.mean_point),i)
			dist.sort()
			partition.clusters[dist[0][1]].points.append(pt)
			partition.clusters[dist[0][1]].calc_mean()


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

	def distance(self,other):
		return ((self.x - other.x)**2 + (self.y - other.y)**2)**2 * (abs(self.theta - other.theta)**0.4+1)

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
	
	def calc_variance(self):
		for cluster in self.clusters:
			self.variance += cluster.variance
	
	def __lt__(self,other):
		return self.variance < other.variance


class Cluster:
	def __init__(self,origin):
		self.origin = origin
		self.points = []
		self.mean_point = Point(0,0,self.origin)
		self.variance = 0
	
	def calc_mean(self):
		self.mean_point = Point(np.mean([a.x for a in self.points]), np.mean([a.y for a in self.points]), self.origin)
	
	def calc_variance(self):
		for pt in self.points:
			self.variance += pt.distance(self.mean_point)

	def __str__(self):
		return "(" + str(self.mean_point) + ":" + str(len(self.points)) + "::"+ str(self.points) + ")"

	def __repr__(self):
		return str(self)