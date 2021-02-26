# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
#import numpy as np
from os import path, mkdir, chdir, remove
from subprocess import call
from glob import glob
from datetime import datetime
from pandas import DataFrame
from sys import argv
#from matplotlib.pyplot import figure

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


# Generate video
def generate_video(delete_frames=False):
	chdir(path.join("./fdtd_output", folder))
	call([
		'ffmpeg', '-y', '-framerate', '8', '-i', 'file%02d.png', '-r', '30',
		'-pix_fmt', 'yuv420p', 'fdtd_sim_video_' + simTitle + '.mp4'
	])
	if delete_frames:  # delete frames
		for file_name in glob("*.png"):
			remove(file_name)
	chdir("../..")


# Save detector readings
def save_data(detectors):
	dic = {}
	for detector in detectors:
		dic[detector.name + " (E)"] = [x for x in detector.detector_values()["E"]]
		dic[detector.name + " (H)"] = [x for x in detector.detector_values()["H"]]
	df = DataFrame(dic)
	df.to_csv(path.join("./fdtd_output", folder, "detector_readings.csv"), index=None)


grid = fdtd.Grid(shape=(15.5e-6, 15.5e-6, 1), )

#grid[7e-6:8e-6, 0:1e-6, 0] = fdtd.Object(permittivity=100, name="object1")
#grid[6e-6:8e-6, 1e-6:2e-6, 0] = fdtd.Object(permittivity=100, name="object2")
#grid[7e-6:8e-6, 2e-6:3e-6, 0] = fdtd.Object(permittivity=100, name="object3")
#grid[6e-6:8e-6, 3e-6:4e-6, 0] = fdtd.Object(permittivity=100, name="object4")
#grid[7e-6:8e-6, 4e-6:5e-6, 0] = fdtd.Object(permittivity=100, name="object5")
#grid[6e-6:8e-6, 5e-6:6e-6, 0] = fdtd.Object(permittivity=100, name="object6")
#grid[7e-6:8e-6, 6e-6:7e-6, 0] = fdtd.Object(permittivity=100, name="object7")
#grid[6e-6:8e-6, 7e-6:8e-6, 0] = fdtd.Object(permittivity=100, name="object8")
#grid[7e-6:8e-6, 8e-6:9e-6, 0] = fdtd.Object(permittivity=1, name="object9")
#grid[6e-6:8e-6, 9e-6:10e-6, 0] = fdtd.Object(permittivity=1, name="object10")
#grid[7e-6:8e-6, 10e-6:11e-6, 0] = fdtd.Object(permittivity=1, name="object11")
#grid[6e-6:8e-6, 11e-6:12e-6, 0] = fdtd.Object(permittivity=1, name="object12")
#grid[7e-6:8e-6, 12e-6:13e-6, 0] = fdtd.Object(permittivity=1, name="object13")
#grid[6e-6:8e-6, 13e-6:14e-6, 0] = fdtd.Object(permittivity=1, name="object14")
#grid[7e-6:8e-6, 14e-6:15e-6, 0] = fdtd.Object(permittivity=1, name="object15")

#grid[1.0e-6:np.tan(np.radians(30))*8.5e-6, 6.5e-6:14e-6, 0] = fdtd.LineSource(period = 1550e-9 / (3e8), name="source")
#grid[20, 7.5e-6, 0] = fdtd.PointSource(period=1550e-9 / (3e8), name="source", pulse=True)
grid[20, 7.5e-6, 0] = fdtd.PointSource(period=1550e-9 / (3e8), name="source", pulse=True, cycle=3, dt=4e-15)

#grid[12e-6, :, 0] = fdtd.LineDetector(name="detector")
for i in range(9):
	grid[12e-6, 30+5*i:32+5*i, 0] = fdtd.LineDetector(name="detector"+str(i))

# x boundaries
grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

#print(grid)
f = open(path.join("./fdtd_output", folder, "grid.txt"), "w")
f.write(str(grid))
f.close()

#figure(figsize=(15, 15))
for i in range(120):
	grid.run(total_time=1)
	#grid.visualize(z=0, animate=True)
	grid.visualize(z=0, animate=True, index=i, save=True, folder=folder)
generate_video(delete_frames=True)
#grid.run(total_time=120)
#grid.visualize(z=0, index=i, save=True, folder=folder)
save_data(grid.detectors)

#grid.run(total_time=100)
#grid.visualize(z=0, show=True)
#print(grid.detectors[0].name, grid.detectors[0].detector_values()["E"][-1])
