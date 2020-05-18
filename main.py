from src.city import City
from src.graph import Graph
from src.aco import ACO
from src.simulated_clusters import SimulatedAnnealing
from src.display.dynamic_plot import DynamicPlot
from src.util import srb_kmeans
from src.const import srb_cap

def free_path(cities):
	path = [0]
	added = 0
	for i in range(1,len(cities)):
		path.append(i)
		added += 1
		if(added >= srb_cap):
			added = 0
			path.append(0)
	if(path[-1]==0):
		path.pop()
	return path

if __name__ == '__main__':
	cities = City.load_cities('./data/data50.txt')
	graph = Graph(cities)
	aco_history,aco_cost = ACO(10, 50, 10, [1.0,2.0], [2.0,1.0], [0.4,0.8]).solve(graph)
	params = [0.99998 , 1, 0.0000001, 1000000]
	saco_history,saco_cost = SimulatedAnnealing(graph,aco_history[-1],*params).anneal()
	plt = DynamicPlot()
	kmean_path = srb_kmeans(cities,plt)
	skmean_history, skmean_cost = SimulatedAnnealing(graph,kmean_path,*params).anneal()
	free_history,free_cost = SimulatedAnnealing(graph,free_path(cities),*params).anneal()
	print(free_cost,aco_cost,saco_cost,skmean_cost)
	plt.show(cities,skmean_history,aco_history,saco_history,free_history,graph)