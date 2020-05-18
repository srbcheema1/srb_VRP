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
		self.ax[0,0].set_title("free SA")
		self.ax[0,1].set_title("Pure ACO")
		self.ax[0,2].set_title("SA with ACO")
		self.ax[1,0].set_title("Kmean")
		self.ax[1,1].set_title("SA with Kmean")
		self.ax[1,2].set_title("Optmimization")

	def displayClusters(self,clusters,cities):
		PartitionDisplay(self.ax[1,0]).plot_partitions(clusters,cities[0])
		self._flush()

	def show(self,cities,skmean_history,aco_history,saco_history,free_history,graph):
		freeDisplay = HistoryDisplay(self.ax[0,0],cities,free_history,self._flush)
		acoDisplay = HistoryDisplay(self.ax[0,1],cities,aco_history,self._flush)
		sacoDisplay = HistoryDisplay(self.ax[0,2],cities,saco_history,self._flush)
		skmeanDisplay = HistoryDisplay(self.ax[1,1],cities,skmean_history,self._flush)
		
		def _get_time(i):
			if(i < 5): return 1
			if(i < 10): return 0.5
			if(i < 20): return 0.3
			return 0.2

		for i in range(max(len(skmean_history),len(aco_history),len(saco_history),len(free_history))):
			if(i == len(free_history)-1):
				freeDisplay.plot_final(free_history[i])
			if(i<len(free_history)-1):
				freeDisplay.plot(free_history[i])

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

		OutcomeDisplay(self.ax[1,2]).plot_learning(skmean_history,aco_history,saco_history,free_history,graph)
		self.end()


	def end(self):
		plt.ioff()
		plt.show()


	def _flush(self):
		#We need to draw *and* flush0
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()