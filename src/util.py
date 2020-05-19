from .graph import Graph
from .simulated_annealing import SimulatedAnnealing
from .kmean import Kmean, Cluster, Point
from src.const import srb_cap

def free_path(cities,cap=srb_cap):
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

def _clusters_to_list(clusters):
	path = []
	for cluster in clusters:
		path.append(0)
		path.extend([pt.index for pt in cluster.points])
	return path

def srb_kmeans(cities,cap=srb_cap):
	# equal sized clusters, good results
	k = Kmean(points=[[city.x,city.y] for city in cities[1:]],origin=[cities[0].x,cities[0].y],base=1,cap=cap)
	return _clusters_to_list(k.partition.clusters),k.partition.clusters


def sklearn_kmeans(cities):
	# unequal sized clusters, so useless
	# history,cost = anneal_sklearn_kmeans(cities,plt)
	from sklearn.cluster import KMeans
	data = [[city.x,city.y] for city in cities[1:]]
	N = (len(cities)+9)//10
	k = KMeans(n_clusters=N)
	label = k.fit(data).predict(data)
	clusters = [Cluster([cities[0].x,cities[0].y]) for _ in range(N)]
	origin = [cities[0].x,cities[0].y]

	for i,pt in enumerate(data):
		clusters[label[i]].points.append(Point(pt[0],pt[1],origin,i+1))
		clusters[label[i]].mean_point = Point(k.cluster_centers_[label[i]][0],k.cluster_centers_[label[i]][1],origin)

	return _clusters_to_list(clusters),clusters

'''
these are useless now, instead use SimulatedAnnealing from .simulated_clusters
'''
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
	# takes k.partition.clusters as param
	cost = 0
	clusters_history = [] # ith history represents history of ith cluster
	for i,cluster in enumerate(clusters):
		graph = Graph([cities[0]] + [cities[pt.index] for pt in cluster.points])
		cluster_history,cost_temp = SimulatedAnnealing(graph, graph.nearestNeighbourSolution(), 0.9998 , 10, 0.0000001, 1000000).anneal()
		cost += cost_temp
		clusters_history.append([graph.get_indices(path) for path in cluster_history])

	return combine_histories(clusters_history), cost