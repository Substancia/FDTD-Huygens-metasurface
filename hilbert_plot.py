from matplotlib.pyplot import subplot, plot, show, title, suptitle, figure, legend, xlabel, ylabel
from scipy.signal import hilbert
from pandas import read_csv
from sys import argv

"""
Hilbert plot for detector responses.
Warning: ALL detectors should be *1 CELL* in size.

Arguments:-
filename (string)
"""
 
def plotDetection(File, detectorElement, specificPlot):
	df = read_csv(File)
	#dic = df.to_string()

	for detector in df:
		if specificPlot is not None:
			if detector[-2] != specificPlot[0]:
				continue
		if detector[-2] == "E":
			figure(0, figsize=(15, 15))
		elif detector[-2] == "H":
			figure(1, figsize=(15, 15))
		for dimension in range(len(df[detector][0][1:-1].split("\n")[0][1:-1].split())):
			if specificPlot is not None:
				if ["x", "y", "z"].index(specificPlot[1]) != dimension:
					continue
			# if specificPlot, plot on 1x1, else plot on 2x2
			subplot(2 - int(specificPlot is not None), 2 - int(specificPlot is not None), dimension + 1 if specificPlot is None else 1)
			#plot(abs(hilbert([float(x[2:-2].split()[dimension]) for x in df[detector]])), label=detector)
			plot(abs(hilbert([float(x[1:-1].split("\n ")[0][1:-1].split()[dimension]) for x in df[detector]])), label=detector)
			title(detector[-2] + "(" + ["x", "y", "z"][dimension] + ")")
		#suptitle(detector)
		#show()

# Loop same as above, only to add axes labels
	for i in range(2):
		if specificPlot is not None:
			if ["E", "H"][i] != specificPlot[0]:
				continue
		figure(i)
		for dimension in range(len(df[detector][0][1:-1].split("\n")[0][1:-1].split())):
			if specificPlot is not None:
				if ["x", "y", "z"].index(specificPlot[1]) != dimension:
					continue
			subplot(2 - int(specificPlot is not None), 2 - int(specificPlot is not None), dimension + 1 if specificPlot is None else 1)
			xlabel("Time steps")
			ylabel("Magnitude")
	legend()
	show()


if __name__ == "__main__":
	if len(argv) < 3:
		argv.append("0")
	if len(argv) < 4:
		argv.append(None)
	plotDetection(argv[1], argv[2], argv[3])
