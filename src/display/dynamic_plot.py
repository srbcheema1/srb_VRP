import matplotlib.pyplot as plt
import time

from .subplots.outcomeDisplay import OutcomeDisplay
from .subplots.historyDisplay import HistoryDisplay
from .subplots.partitionDisplay import PartitionDisplay


class DynamicPlot():
	def __init__(self,animate=False):
		self.animate = animate
		plt.ion() # plot interactive mode ON
		self.figure, self.ax = plt.subplots(2,3)
		self.ax[0,0].set_title("SA")
		self.ax[0,1].set_title("ACO")
		self.ax[0,2].set_title("ACO - SA")
		self.ax[1,0].set_title("Kmean")
		self.ax[1,1].set_title("KMean - SA")
		self.ax[1,2].set_title("Outcome")


	def displayClusters(self,clusters,cities):
		PartitionDisplay(self.ax[1,0]).plot_partitions(clusters,cities[0])
		self._flush()


	def show(self,cities,sa_history,aco_history,saco_history,kmean_clusters,skmean_history,graph):
		self.displayClusters(kmean_clusters,cities)
		OutcomeDisplay(self.ax[1,2]).plot_learning(sa_history,aco_history,saco_history,skmean_history,graph)
		saDisplay = HistoryDisplay(self.ax[0,0],cities,sa_history,self._flush)
		acoDisplay = HistoryDisplay(self.ax[0,1],cities,aco_history,self._flush)
		sacoDisplay = HistoryDisplay(self.ax[0,2],cities,saco_history,self._flush)
		skmeanDisplay = HistoryDisplay(self.ax[1,1],cities,skmean_history,self._flush)
		
		def _get_time(i):
			if(i < 5): return 1
			if(i < 10): return 0.5
			if(i < 20): return 0.3
			return 0.2

		sa_history,aco_history,saco_history,skmean_history = self._compress_histories([sa_history,aco_history,saco_history,skmean_history])
		for i in range(max(len(sa_history),len(aco_history),len(saco_history),len(skmean_history))):
			if(i == len(sa_history)-1):
				saDisplay.plot_final(sa_history[i])
			if(i<len(sa_history)-1):
				saDisplay.plot(sa_history[i])

			if(i == len(aco_history)-1):
				acoDisplay.plot_final(aco_history[i])
			if(i<len(aco_history)-1):
				acoDisplay.plot(aco_history[i])

			if(i == len(saco_history)-1):
				sacoDisplay.plot_final(saco_history[i])
			if(i<len(saco_history)-1):
				sacoDisplay.plot(saco_history[i])

			if(i == len(skmean_history)-1):
				skmeanDisplay.plot_final(skmean_history[i])
			if(i<len(skmean_history)-1):
				skmeanDisplay.plot(skmean_history[i])
			if(self.animate): time.sleep(_get_time(i))

		self.end()


	def _compress_histories(self,histories):
		n = 10
		for i,history in enumerate(histories):
			l = len(history)
			if(l > 10):
				histories[i] = [history[int((i/(n-1))*(l-1))] for i in range(n)]
		return tuple(histories)


	def end(self):
		plt.ioff()
		plt.show()


	def _flush(self):
		#We need to draw *and* flush0
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()