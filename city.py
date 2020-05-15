class City:
	def __init__(self,index,x,y):
		self.index = int(index)
		self.x = int(x)
		self.y = int(y)


	def __repr__(self):
		return str(self)


	def __str__(self):
		return "{" + str(self.index) + ": " + str(self.x) + "," + str(self.y) + "}"

	
	@staticmethod
	def load_cities(file_name):
		cities = []
		with open(file_name) as f:
			index = 1
			for line in f.readlines():
				city = line.split(' ')
				cities.append(City(index,city[0],city[1]))
				index+=1
		return cities