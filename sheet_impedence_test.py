# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
from numpy import sin, radians, tan, meshgrid, arange, flip, savez
from os import path, mkdir, chdir, remove
from subprocess import call
from glob import glob
from datetime import datetime
#from pandas import DataFrame
from sys import argv
from matplotlib.pyplot import figure
from time import time

start_time = time()

if not path.exists("./fdtd_output"):  # Output folder declaration
	mkdir("fdtd_output")
simTitle = str(datetime.now().year) + "-" + str(
	datetime.now().month) + "-" + str(datetime.now().day) + "-" + str(
		datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second)
if len(argv) > 1:  # Simulation name (optional)
	simTitle = simTitle + " (" + argv[1] + ")"
folder = "fdtd_output_" + simTitle
if path.exists(path.join("./fdtd_output", folder)):  # Overwrite protocol
	yn = input("File", folder, "exists. Overwrite? [Y/N]: ")
	if yn.capitalize() == "N":
		exit()
else:
	mkdir(path.join("./fdtd_output", folder))


# Save detector readings
def save_data(detectors):
	dic = {}
	for detector in detectors:
		dic[detector.name + " (E)"] = [x for x in detector.detector_values()["E"]]
		dic[detector.name + " (H)"] = [x for x in detector.detector_values()["H"]]
	#df = DataFrame(dic)
	#df.to_csv(path.join("./fdtd_output", folder, "detector_readings.csv"), index=None)
	savez(path.join("./fdtd_output", folder, "detector_readings"), **dic)


# grid
grid = fdtd.Grid(shape=(310, 400, 1), grid_spacing=77.5e-9)

# objects

# source
grid[15, 30:370, 0] = fdtd.LineSource(period = 15500e-9 / (3e8), name="source")

# detectors
grid[20:300, 200, 0] = fdtd.LineDetector(name="detector")

# x boundaries
grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

# Saving grid geometry
f = open(path.join("./fdtd_output", folder, "grid.txt"), "w")
f.write(str(grid))
f.close()

grid.run(total_time=500)
#grid.visualize(z=0, show=True)
grid.visualize(z=0, show=True, index=0, save=True, folder=folder)
save_data(grid.detectors)

end_time = time()
print("Runtime:", end_time-start_time)
