from src.graph import Graph
from src.aco import ACO
from src.display.dynamic_plot import DynamicPlot
from src.city import City
from src.kmean import Kmean
from src.simulated_annealing import SimulatedAnnealing

def combine_histories(clusters_history):
	combined_history = [] # combined of all clusters
	for frame_no in range(max([len(history) for history in clusters_history])): # frames as longest history
		frame = []
		for cluster_history in clusters_history:
			if(frame_no < len(cluster_history)):
				frame.extend(cluster_history[frame_no])
			else:
				frame.extend(cluster_history[-1])
		combined_history.append(frame)
	return combined_history

def anneal_clusters(clusters,cities):
	cost = 0
	clusters_history = [] # ith history represents history of ith cluster
	for i,cluster in enumerate(clusters):
		graph = Graph([cities[0]] + [cities[pt.index] for pt in cluster.points])
		cluster_history,cost_temp = SimulatedAnnealing(graph, graph.nearestNeighbourSolution(), 0.9998 , 10, 0.0000001, 1000000).anneal()
		cost += cost_temp
		clusters_history.append([graph.get_indices(path) for path in cluster_history])

	return combine_histories(clusters_history), cost

def anneal_kmeans(cities,plt):
	k = Kmean(points=[[city.x,city.y] for city in cities[1:]],origin=[cities[0].x,cities[0].y],base=1)
	plt.displayClusters(k.partition.clusters,cities)
	return anneal_clusters(k.partition.clusters,cities)

if __name__ == '__main__':
	cities = City.load_cities('./data/data60.txt')
	graph = Graph(cities)
	a_history,_ = ACO(20, 100, 10, [1.0,2.0], [2.0,1.0], [0.4,0.8]).solve(graph)
	plt = DynamicPlot()
	history,_ = anneal_kmeans(cities,plt)
	plt.show(cities,history,a_history,graph)