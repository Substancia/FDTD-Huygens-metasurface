from fdtd_venv import fdtd_mod as fdtd
import numpy as np
import os
import subprocess
import glob
import datetime
import matplotlib.pyplot as plt


if not os.path.exists("./fdtd_output"):
	os.makedir("fdtd_output")
folder = "fdtd_output_" + str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().hour) + "-" + str(datetime.datetime.now().minute) + "-" + str(datetime.datetime.now().second)
os.mkdir(os.path.join("./fdtd_output", folder))

def generate_video():
	os.chdir(os.path.join("./fdtd_output", folder))
	subprocess.call([
		'ffmpeg', '-framerate', '8', '-i', 'file%02d.png', '-r', '30', '-pix_fmt', 'yuv420p',
		'fdtd_sim_video.mp4'
	])
	for file_name in glob.glob("*.png"):
		os.remove(file_name)


grid = fdtd.Grid(shape=(7.75e-6, 15.5e-6, 1), grid_spacing=77.5e-9)

# objects
#grid[-40:-20, 0:15.5e-6, 0] = fdtd.Object(permittivity=10**2)

# source
grid[22, 7.75e-6, 0] = fdtd.PointSource(period=1550e-9 / (3e8), name="source")

# detector
for i in range(90):
	grid[(4/3 - np.sin(np.radians(2*i)))*4.65e-6:(4/3 - np.sin(np.radians(2*i+2)))*4.65e-6, (5/3 - np.cos(np.radians(2*i)))*4.65e-6:(5/3 - np.cos(np.radians(2*i+2)))*4.65e-6, 0] = fdtd.LineDetector(name = "detector" + str(i))
#grid[4e-6, 50:51, 0] = fdtd.LineDetector(name="detector")

# x boundaries
grid[0:20, :, :] = fdtd.PML(name="pml_xlow")
grid[-20:, :, :] = fdtd.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:20, :] = fdtd.PML(name="pml_ylow")
grid[:, -20:, :] = fdtd.PML(name="pml_yhigh")

#print(grid)

for i in range(100):
	grid.run(total_time=1)
	grid.visualize(z=0, animate=True, index = i, save = True, folder = folder)
generate_video()

#grid.run(total_time=100)
#for i in range(len(grid.detectors)):
	#print(grid.detectors[i].detector_values()['H'][-1])
detector_array = [x.detector_values()['E'][-1] for x in grid.detectors]
#print(detector_array)
#grid.visualize(z=0, show=True)

arr = [x[0][2] for x in detector_array]
#for i in detector_array:
	#for j in i:
		#arr.append(j[2])
print(arr)
plt.plot([2*x for x in range(len(arr))], arr)
plt.scatter([2*x for x in range(len(arr))], arr)
plt.show()
