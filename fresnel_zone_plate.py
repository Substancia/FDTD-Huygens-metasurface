# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
from numpy import sin, radians, tan, meshgrid, arange, flip, array
from os import path
from sys import argv
from time import time

start_time = time()

def radius_function(n, lam, f):
	return int((n*lam*f + (n*lam/2)**2)**0.5)

run = True
saveStuff = False

# grid
grid = fdtd.Grid(shape=(260, 15.5e-6, 1), grid_spacing=77.5e-9)
if saveStuff:
	grid.save_simulation(argv[1] if len(argv) > 1 else None)

# objects
f = 100
lam = 1550e-4
col_center =  100
for i in range(20):
	grid[30:40, col_center+radius_function(2*i+1, lam, f):col_center+radius_function(2*i+2, lam, f), 0] = fdtd.Object(permittivity=100, name="r"+str(i))
	grid[30:40, col_center-radius_function(2*i+2, lam, f):col_center-radius_function(2*i+1, lam, f), 0] = fdtd.Object(permittivity=100, name="l"+str(i))

# source
grid[15, 50:150, 0] = fdtd.LineSource(period = 1550e-9 / (3e8), name="source")

# detectors
grid[50:150, 80:120, 0] = fdtd.BlockDetector(name="BlockDetector")
grid[50:150, 100, 0] = fdtd.LineDetector(name="LineDetectorVert")
#grid[450, 60:140, 0] = fdtd.LineDetector(name="LineDetectorHor")

# x boundaries
grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

# Saving grid geometry
if saveStuff:
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

#if run:
	#for i in range(400):
		#grid.run(total_time=1)
		#grid.visualize(z=0, animate=True)
		#grid.visualize(z=0, animate=True, index=i, save=True, folder=grid.folder)
#if saveStuff:
	#grid.generate_video(delete_frames=True)
	#grid.save_data()

if run:
	grid.run(total_time=400)
if saveStuff:
	grid.visualize(z=0, show=True, index=0, save=True, folder=grid.folder)
	grid.save_data()
else:
	grid.visualize(z=0, show=True)

end_time = time()
print("Runtime:", end_time-start_time)
