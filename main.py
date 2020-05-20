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

	times = [round(times[i]-times[i-1],2) for i in range(1,len(times))]
	if(disp): print("algo: ","SA","ACO","aco-SA","Kmean","SA")
	if(disp): print("times: ",*times)
	if(disp): print(sa_cost,aco_cost,saco_cost,skmean_cost)
	if(disp): DynamicPlot().show(cities,sa_history,aco_history,saco_history,kmean_clusters,skmean_history,graph)
	c_ret = [round(x,2) for x in [sa_cost,aco_cost,saco_cost,skmean_cost]]
	t_ret = [round(x,2) for x in [times[0],times[1],times[1] + times[2],times[3] + times[4]]]
	h_ret = [sa_history,aco_history,saco_history,skmean_history]
	return c_ret, t_ret, h_ret

def extract_output():
	data = [["Sno","N","Cap","SA","SA-time","ACO","ACO-time","ACO-SA","ACO-SA-time","Kmean-SA","Kmean-SA-time"]]
	for i in range(100):
		cities = City.generate_cities()
		n = len(cities)
		cap = 10 if n <=60 else 20
		c_ret, t_ret, h_ret = run(cities,cap,disp=False)
		tabular_ret = [i+1,n,cap]
		for a,b in zip(c_ret,t_ret):
			tabular_ret.append(a)
			tabular_ret.append(b)
		data.append(tabular_ret)
		print(Tabular([tabular_ret]))
	tabular = Tabular(data)
	tabular.write_json('output/out.json')
	tabular.write_xls('output/data.xls')

if __name__ == '__main__':
	run(City.load_cities('data/data60.txt'),cap=10)
	# extract_output() # only to extract data