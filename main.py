from aco import ACO, Graph
from dynamic_plot import DynamicPlot
from city import City
from kmean import Kmean

if __name__ == '__main__':
	plt = DynamicPlot()
	cities = City.load_cities('./data/data40.txt')
	graph = Graph(cities)
	# k = Kmean(cities)
	# plt.plot_partitions(k.partitions,cities[0])
	history,cost = ACO(20, 100, 10, [1.0,2.0], [2.0,1.0], [0.4,0.8]).solve(graph)
	print(cost,history[-1])
	plt.show(cities,history)