import ptspy.plot.plotter as pl
import ptspy.simulator.simulator as sm
import ptspy.utilities.parse as pr
import ptspy.utilities.dataHandler as dh


def main(args):
	allData = dh.getAllData(args.configFile)
	particleList = sm.startSimulation(allData)
	pl.plotData(allData,particleList)

if __name__ == "__main__":
	args = pr.parseArgs()
	main(args)