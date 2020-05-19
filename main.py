import time
from src.city import City
from src.graph import Graph
from src.aco import ACO
from src.simulated_clusters import SimulatedAnnealing
from src.display.dynamic_plot import DynamicPlot
from src.util import srb_kmeans, free_path, sklearn_kmeans

def run(file_name,cap=10):
	cities = City.load_cities(file_name)
	graph = Graph(cities)
	params = [0.99998 , 1, 0.000001, 100000] # at this iterations end, at 0.9998 temp will
	times = [time.time()]

	sa_history,sa_cost = SimulatedAnnealing(graph,free_path(cities,cap=cap),*params).anneal()
	times.append(time.time())

	aco_history,aco_cost = ACO(10, 50, 10, [1.0,2.0], [2.0,1.0], [0.4,0.8],cap=cap).solve(graph)
	times.append(time.time())

	saco_history,saco_cost = SimulatedAnnealing(graph,aco_history[-1],*params).anneal()
	times.append(time.time())

	kmean_path,kmean_clusters = srb_kmeans(cities,cap=cap)
	times.append(time.time())

	skmean_history, skmean_cost = SimulatedAnnealing(graph,kmean_path,*params).anneal()
	times.append(time.time())

	times = [times[i]-times[i-1] for i in range(1,len(times))]
	print("algo: ","SA","ACO","aco-SA","Kmean","SA")
	print("times: ",*times)
	print(sa_cost,aco_cost,saco_cost,skmean_cost)
	DynamicPlot().show(cities,sa_history,aco_history,saco_history,kmean_clusters,skmean_history,graph)

if __name__ == '__main__':
	run('./data/data60.txt',cap=10)