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


	def show(self,cities,history,a_history,graph,partitions):
		PartitionDisplay(self.ax[1,0]).plot_partitions(partitions,cities[0])
		acoDisplay = HistoryDisplay(self.ax[0,1],cities,a_history,self._flush)
		srbDisplay = HistoryDisplay(self.ax[1,1],cities,history,self._flush)

		for i in range(max(len(a_history),len(history))):
			if(i == len(a_history)-1):
				acoDisplay.plot_final(a_history[i])
			if(i<len(a_history)-1):
				acoDisplay.plot(a_history[i])
			if(i == len(history)-1):
				srbDisplay.plot_final(history[i])
			if(i<len(history)-1):
				srbDisplay.plot(history[i])
			time.sleep(1)

		OutcomeDisplay(self.ax[1,2]).plot_learning(history,a_history,graph)
		self.end()


	def end(self):
		plt.ioff()
		plt.show()


	def _flush(self):
		#We need to draw *and* flush0
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()