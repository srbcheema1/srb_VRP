from src.graph import Graph
from src.aco import ACO
from src.display.dynamic_plot import DynamicPlot
from src.city import City
from src.kmean import Kmean
from src.simulated_annealing import SimulatedAnnealing

def anneal_clusters(clusters,cities):
	cost = 0
	histories = dict()
	max_history_len = 0
	for i,cluster in enumerate(clusters):
		city_list = [cities[0]] + [cities[pt.index] for pt in cluster.points]
		graph = Graph(city_list)
		history,cost_temp = SimulatedAnnealing(graph, graph.nearestNeighbourSolution(), 0.9998 , 10, 0.0000001, 1000000).anneal()
		max_history_len = max(max_history_len,len(history))
		cost += cost_temp
		histories[i] = [graph.get_indices(path) for path in history]

	combined_hist = [] # combined of all clusters
	for i in range(max_history_len):
		history = []
		for j in range(len(clusters)):
			if(i < len(histories[j])):
				history.extend(histories[j][i])
			else:
				history.extend(histories[j][-1])
		combined_hist.append(history)
	return combined_hist, cost


if __name__ == '__main__':
	cities = City.load_cities('./data/data60.txt')
	graph = Graph(cities)
	k = Kmean(points=[[city.x,city.y] for city in cities[1:]],origin=[cities[0].x,cities[0].y],base=1)
	history,cost = anneal_clusters(k.partition.clusters,cities)
	a_history,a_cost = ACO(20, 100, 10, [1.0,2.0], [2.0,1.0], [0.4,0.8]).solve(graph)
	plt = DynamicPlot()
	plt.show(cities,history,a_history,graph,k.partition.clusters)