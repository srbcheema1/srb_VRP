from aco import ACO, Graph
from dynamic_plot import DynamicPlot
from city import City
from kmean import Kmean
from simulated_annealing import SimulatedAnnealing

def _get_indices(path,graph):
	return [graph.cities[i].index for i in path]

def get_histories(partitions,cities):
	cost = 0
	histories = dict()
	max_history_len = 0
	for i,part in enumerate(partitions):
		city_list = [cities[0]] + part.cities
		graph = Graph(city_list)
		history,cost_temp = SimulatedAnnealing(graph, graph.nearestNeighbourSolution(), 0.9998 , 10, 0.0000001, 1000000).anneal()
		cost += cost_temp
		new_history = [_get_indices(path,graph) for path in history]
		histories[i] = new_history
		max_history_len = max(max_history_len,len(new_history))

	final_hist = []
	for i in range(max_history_len):
		history = []
		for j in range(len(partitions)):
			if(i < len(histories[j])):
				history.extend(histories[j][i])
			else:
				history.extend(histories[j][-1])
		final_hist.append(history)
	return final_hist, cost


if __name__ == '__main__':
	cities = City.load_cities('./data/data60.txt')
	graph = Graph(cities)
	k = Kmean(cities)
	history,cost = get_histories(k.partitions,cities)
	a_history,a_cost = ACO(20, 100, 10, [1.0,2.0], [2.0,1.0], [0.4,0.8]).solve(graph)
	plt = DynamicPlot()
	plt.show(cities,history,a_history,graph,k.partitions)