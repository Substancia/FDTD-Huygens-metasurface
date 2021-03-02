from fdtd_venv import fdtd_mod as fdtd
from os import path, mkdir, chdir, remove
from subprocess import call
from glob import glob
from datetime import datetime
from matplotlib.pyplot import plot, scatter, show


if not path.exists("./fdtd_output"):
	mkdir("fdtd_output")
folder = "fdtd_output_" + str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day) + "-" + str(datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second)
mkdir(path.join("./fdtd_output", folder))

def generate_video():
	chdir(path.join("./fdtd_output", folder))
	call([
		'ffmpeg', '-framerate', '8', '-i', 'file%02d.png', '-r', '30', '-pix_fmt', 'yuv420p',
		'fdtd_sim_video.mp4'
	])
	for file_name in glob("*.png"):
		remove(file_name)


grid = fdtd.Grid(shape=(7.75e-6, 15.5e-6, 1), grid_spacing=38.75e-9)

# objects
#grid[-40:-20, 0:15.5e-6, 0] = fdtd.Object(permittivity=10**2)
for i in range(80):
	grid[80+i:81+i, 250-i:300, 0] = fdtd.Object(permittivity=100**2, name="slice"+str(i))

# source
#grid[22, 7.75e-6, 0] = fdtd.PointSource(period=1550e-9 / (3e8), name="source")
grid[44, 4e-6:12e-6, 0] = fdtd.LineSource(period=1550e-9 / (3e8), name="source")

# detector
for i in range(6):
	grid[(2+i)*20:(3+i)*20, 80, 0] = fdtd.LineDetector(name="detector"+str(i))
	#grid[20+i:21+i, 50, 0] = fdtd.LineDetector(name="detector"+str(i))
#grid[20:80, 50, 0] = fdtd.LineDetector(name="detector")

# x boundaries
grid[0:40, :, :] = fdtd.PML(name="pml_xlow")
grid[-40:, :, :] = fdtd.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:40, :] = fdtd.PML(name="pml_ylow")
grid[:, -40:, :] = fdtd.PML(name="pml_yhigh")

for i in range(200):
	grid.run(total_time=1)
	grid.visualize(z=0, animate=True, index = i, save = True, folder = folder)
generate_video()

#grid.run(total_time=200)
detector_array = [x.detector_values()['E'][-1] for x in grid.detectors]
#print(detector_array)
#grid.visualize(z=0, show=True)

arr = [x[0][2] for x in detector_array]
#for i in detector_array:
	#for j in i:
		#arr.append(j[2])
print(arr)
plot([x for x in range(len(arr))], arr)
scatter([x for x in range(len(arr))], arr)
show()
