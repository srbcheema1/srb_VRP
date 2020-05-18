import matplotlib.pyplot as plt
import time

from .subplots.outcomeDisplay import OutcomeDisplay
from .subplots.historyDisplay import HistoryDisplay
from .subplots.partitionDisplay import PartitionDisplay

class DynamicPlot():
	def __init__(self):
		plt.ion() # plot interactive mode ON
		self.figure, self.ax = plt.subplots(2,3)
		self.ax[0,0].set_title("free")
		self.ax[0,1].set_title("Pure ACO")
		self.ax[0,2].set_title("SA with ACO")
		self.ax[1,0].set_title("Kmean")
		self.ax[1,1].set_title("SA with Kmean")
		self.ax[1,2].set_title("Optmimization")

	def displayClusters(self,clusters,cities):
		PartitionDisplay(self.ax[1,0]).plot_partitions(clusters,cities[0])
		self._flush()

	def show(self,cities,s_history,aco_history,saco_history,graph):
		acoDisplay = HistoryDisplay(self.ax[0,1],cities,aco_history,self._flush)
		sacoDisplay = HistoryDisplay(self.ax[0,2],cities,aco_history,self._flush)
		sDisplay = HistoryDisplay(self.ax[1,1],cities,s_history,self._flush)

		for i in range(max(len(s_history),len(aco_history),len(saco_history))):
			if(i == len(aco_history)-1):
				acoDisplay.plot_final(aco_history[i])
			if(i<len(aco_history)-1):
				acoDisplay.plot(aco_history[i])
			if(i == len(saco_history)-1):
				sacoDisplay.plot_final(saco_history[i])
			if(i<len(saco_history)-1):
				sacoDisplay.plot(saco_history[i])
			if(i == len(s_history)-1):
				sDisplay.plot_final(s_history[i])
			if(i<len(s_history)-1):
				sDisplay.plot(s_history[i])
			time.sleep(1)

		OutcomeDisplay(self.ax[1,2]).plot_learning(s_history,aco_history,saco_history,graph)
		self.end()


	def end(self):
		plt.ioff()
		plt.show()


	def _flush(self):
		#We need to draw *and* flush0
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()