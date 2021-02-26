from matplotlib.pyplot import subplot, plot, show, title, suptitle, figure
from pandas import read_csv
from sys import argv
"""
Detector values plot function.

Arguments:-
simulation name (optional): Saves the simulation folder with this name along with timestamp
"""


def plotDetection(File, timestep):
	df = read_csv(File)
	#dic = df.to_string()
	if int(timestep) == -1:
		timestep = len(df) - 1

	for detector in df:
		figure(figsize=(15, 15))
		for dimension in range(len(df[detector][0][1:-1].split("\n ")[0][1:-1].split())):
			subplot(2, 2, dimension + 1)
			plot([float(x[1:-1].split()[dimension]) for x in df[detector][int(timestep)][1:-1].split("\n ")])
			title(detector[-2] + "(" + ["x", "y", "z"][dimension] + ")")
		suptitle(detector)
		show()

	#for dimension in range(len(df["detector (E)"][0][1:-1].split())):
	#subplot(2, len(df["detector (E)"][0][1:-1].split()), dimension + 1)
	#plot([x[1:-1].split()[dimension] for x in df["detector (E)"]])
	#title("E(" + ["x", "y", "z"][dimension] + ")")

	#subplot(2, len(df["detector (H)"][0][1:-1].split()), dimension + 4)
	#plot([x[1:-1].split()[dimension] for x in df["detector (H)"]])
	#title("H(" + ["x", "y", "z"][dimension] + ")")

	#show()


if __name__ == "__main__":
	if len(argv) < 3:
		argv.append(-1)
	plotDetection(argv[1], argv[2])
