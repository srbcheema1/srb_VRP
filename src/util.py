from .graph import Graph
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