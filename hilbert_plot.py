from matplotlib.pyplot import subplot, plot, show, title, suptitle, figure, legend
from scipy.signal import hilbert
from pandas import read_csv
from sys import argv
 
def plotDetection(File):
	df = read_csv(File)
	#dic = df.to_string()

	for detector in df:
		if detector[-2] == "E":
			figure(0, figsize=(15, 15))
		elif detector[-2] == "H":
			figure(1, figsize=(15, 15))
		for dimension in range(len(df[detector][0][2:-2].split())):
			subplot(2, 2, dimension + 1)
			plot(abs(hilbert([float(x[2:-2].split()[dimension]) for x in df[detector]])), label=detector)
			title(detector[-2] + "(" + ["x", "y", "z"][dimension] + ")")
		#suptitle(detector)
		#show()
	legend()
	show()


if __name__ == "__main__":
	plotDetection(argv[1])
