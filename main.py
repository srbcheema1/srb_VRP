import time
from srblib import Tabular

from src.city import City
from src.graph import Graph
from src.aco import ACO
from src.simulated_clusters import SimulatedAnnealing
from src.display.dynamic_plot import DynamicPlot
from src.util import srb_kmeans, free_path, sklearn_kmeans

def run(cities,cap=10,disp=True):
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
	if(disp): print("algo: ","SA","ACO","aco-SA","Kmean","SA")
	if(disp): print("times: ",*times)
	if(disp): print(sa_cost,aco_cost,saco_cost,skmean_cost)
	if(disp): DynamicPlot().show(cities,sa_history,aco_history,saco_history,kmean_clusters,skmean_history,graph)
	return [sa_cost,aco_cost,saco_cost,skmean_cost]

def extract_output():
	data = [["N","Cap","SA","ACO","ACO-SA","Kmean-SA"]]
	for i in range(100):
		cities = City.generate_cities()
		n = len(cities)
		cap = 10 if n <=60 else 20
		ret = run(cities,cap,disp=False)
		data.append([n,cap] + ret)
		print(Tabular([[i,n,cap] + ret]))
	tabular = Tabular(data)
	tabular.write_json('output/out.json')
	tabular.write_xls('output/data.xls')

if __name__ == '__main__':
	run(City.load_cities('data/data60.txt'),cap=10)
	# extract_output() # only to extract data