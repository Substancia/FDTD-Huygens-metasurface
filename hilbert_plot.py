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
 
def plotDetection(File, detectorElement):
	df = read_csv(File)
	#dic = df.to_string()

	for detector in df:
		if detector[-2] == "E":
			figure(0, figsize=(15, 15))
		elif detector[-2] == "H":
			figure(1, figsize=(15, 15))
		for dimension in range(len(df[detector][0][1:-1].split("\n")[0][1:-1].split())):
			subplot(2, 2, dimension + 1)
			#plot(abs(hilbert([float(x[2:-2].split()[dimension]) for x in df[detector]])), label=detector)
			plot(abs(hilbert([float(x[1:-1].split("\n ")[0][1:-1].split()[dimension]) for x in df[detector]])), label=detector)
			title(detector[-2] + "(" + ["x", "y", "z"][dimension] + ")")
		#suptitle(detector)
		#show()
	for i in range(2):
		figure(i)
		for dimension in range(len(df[detector][0][1:-1].split("\n")[0][1:-1].split())):
			subplot(2, 2, dimension + 1)
			xlabel("Time steps")
			ylabel("Magnitude")
	legend()
	show()


if __name__ == "__main__":
	if len(argv) < 3:
		argv.append("0")
	plotDetection(argv[1], argv[2])
