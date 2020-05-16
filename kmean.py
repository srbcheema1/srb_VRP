import math
import numpy as np



class Kmean:
	def __init__(self,cities,cap=10):
		self.cities = cities
		self.origin = [cities[0].x,cities[0].y]
		self.points = [Point(city.x,city.y,self.origin,city.index) for city in cities[1:]]
		self.cap = cap
		self.partitions = []
		self.compute()


	def compute(self):
		point_sets = self._radially_sorted_point_sets()

		for pset in point_sets:
			partition = Partition()
			partition.mean_point = Point(np.mean([a.x for a in pset]), np.mean([a.y for a in pset]), self.origin)
			self.partitions.append(partition)

		#cheap way
		for i,part in enumerate(self.partitions):
			part.points = point_sets[i]
			part.cities = [self.cities[a.index] for a in part.points]


	def _radially_sorted_point_sets(self):
		point_sets = []
		self.points.sort(key=lambda x: x.r)
		cnt = 0
		loc_set = []
		for point in self.points:
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
		self.points = []
		self.cities = []
		self.mean_point = Point(0,0,[0,0])
	
	def __str__(self):
		return "(" + str(self.mean_point) + ":" + str(len(self.points)) + "::"+ str(self.cities) + ")"

	def __repr__(self):
		return str(self)