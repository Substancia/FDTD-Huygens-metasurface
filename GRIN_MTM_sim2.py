# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
from numpy import sin, radians, tan, array, arange, load
from os import path
#from os import path, mkdir, chdir, remove
#from subprocess import call
#from glob import glob
#from datetime import datetime
#from pandas import DataFrame
#from sys import argv
#from matplotlib.pyplot import figure
from time import time

start_time = time()

# grid
grid = fdtd.Grid(shape=(9.3e-6, 15.5e-6, 1), grid_spacing=77.5e-9)
grid.save_simulation("Example2")

# objects
n0, theta, t = 1, 30, 0.5
for i in range(50):
	x = i*0.08
	epsilon = n0 + x*sin(radians(theta))/t
	epsilon = epsilon**0.5
	grid[5.1e-6:5.6e-6, (5 + i*0.08)*1e-6:(5.08 + i*0.08)*1e-6, 0] = fdtd.Object(permittivity=epsilon, name="object"+str(i))
grid[5.1e-6:5.6e-6, 0.775e-6:5e-6, 0] = fdtd.Object(permittivity=n0**2, name="objectLeft")
grid[5.1e-6:5.6e-6, 9e-6:(15.5 - 0.775)*1e-6, 0] = fdtd.Object(permittivity=epsilon, name="objectRight")

# source
grid[3.1e-6, 1.5e-6:14e-6, 0] = fdtd.LineSource(period = 1550e-9 / (3e8), name="source", pulse=True, cycle=3, hanning_dt=4e-15)

# detectors
for i in range(-4, 8):
	grid[5.8e-6, 84+4*i:86+4*i, 0] = fdtd.LineDetector(name="detector"+str(i))

# x boundaries
grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

# Saving grid geometry
with open(path.join("./fdtd_output", grid.folder, "grid.txt"), "w") as f:
	f.write(str(grid))
	wavelength = 3e8/grid.source.frequency
	wavelengthUnits = wavelength/grid.grid_spacing
	GD = array([grid.x, grid.y, grid.z])
	gridRange = [arange(x/grid.grid_spacing) for x in GD]
	objectRange = array([[gridRange[0][x.x], gridRange[1][x.y], gridRange[2][x.z]] for x in grid.objects]).T
	f.write("\n\nGrid details (in wavelength scale):")
	f.write("\n\tGrid dimensions: ")
	f.write(str(GD/wavelength))
	f.write("\n\tSource dimensions: ")
	f.write(str(array([grid.source.x[-1] - grid.source.x[0] + 1, grid.source.y[-1] - grid.source.y[0] + 1, grid.source.z[-1] - grid.source.z[0] + 1])/wavelengthUnits))
	f.write("\n\tObject dimensions: ")
	f.write(str([(max(map(max, x)) - min(map(min, x)) + 1)/wavelengthUnits for x in objectRange]))

for i in range(100):
	grid.run(total_time=1)
	#grid.visualize(z=0, animate=True)
	grid.visualize(z=0, animate=True, index=i, save=True, folder=grid.folder)
grid.generate_video(delete_frames=True)
grid.save_data()

#grid.run(total_time=120)
#grid.visualize(z=0, show=True, index=0, save=True, folder=folder)
#grid.save_data()
#grid.visualize(z=0, show=True)

df = load(path.join("./fdtd_output", grid.folder, "detector_readings.npz"))
fdtd.plot_detection(df)

end_time = time()
print("Runtime:", end_time-start_time)
