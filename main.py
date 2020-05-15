from aco import ACO, Graph
from dynamic_plot import DynamicPlot
from city import City

if __name__ == '__main__':
	cities = City.load_cities('./data/data1.txt')
	graph = Graph(cities)
	history,cost = ACO(20, 200, 10, [1.0,3.0], [4.0,2.0], [0.4,0.8]).solve(graph)
	print(cost,history[-1])
	plt = DynamicPlot()
	plt.show(cities,history)