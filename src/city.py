from random import randint
class City:
	def __init__(self,index,x,y):
		self.index = int(index)
		self.x = float(x)
		self.y = float(y)


	def __repr__(self):
		return str(self)


	def __str__(self):
		return "{" + str(self.index) + ": " + str(self.x) + "," + str(self.y) + "}"


	@staticmethod
	def load_cities(file_name):
		cities = []
		with open(file_name) as f:
			index = 0
			for line in f.readlines():
				city = line.split(' ')
				cities.append(City(index,city[0],city[1]))
				index+=1
		return cities


	@staticmethod
	def generate_cities():
		n = randint(30,100)
		pt_set = set()
		cities = []
		for i in range(n):
			a = randint(1,50)
			b = randint(1,50)
			while((a,b) in pt_set):
				a = randint(1,50)
				b = randint(1,50)
			pt_set.add((a,b))
			cities.append(City(i,a,b))
		return cities
