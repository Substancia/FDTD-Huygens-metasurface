from fdtd_venv import fdtd_mod as fdtd
from numpy import radians, tan, array, arange
from os import path
from sys import argv

animate = False
run_time = 300
saveStuff = True
results = True

# grid
grid = fdtd.Grid(shape=(200, 200, 1), grid_spacing=77.5e-9)
if saveStuff:
	grid.save_simulation(argv[1] if len(argv) > 1 else None)

# boundaries
grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

# objects
#grid[80:120, 10:-10, 0] = fdtd.Object(permittivity=1.5**2, name="glass_slab")

# source
th = 30
grid[75:25, 25:round(25+50/tan(radians(th))), 0] = fdtd.LineSource(period=(1550e-9)/(3e8), name="source", pulse=True, cycle=3, hanning_dt=4e-15)

# detectors
for i in range(25, 175, 2):
	#grid[100, i:i+2, 0] = fdtd.LineDetector(name="detector1,"+str(i))
	grid[120, i:i+2, 0] = fdtd.LineDetector(name="detector2,"+str(i))

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

if animate:
	if run_time > 0:
		for i in range(run_time):
			grid.run(total_time=1)
			if saveStuff:
				grid.visualize(z=0, animate=True, index=i, save=True, folder=grid.folder)
			else:
				grid.visualize(z=0, animate=True)
	if saveStuff:
		grid.generate_video(delete_frames=True)
		grid.save_data()
else:
	if run_time > 0:
		grid.run(total_time=run_time)
	if saveStuff:
		grid.visualize(z=0, show=True, index=0, save=True, folder=grid.folder)
		grid.save_data()
	else:
		grid.visualize(z=0, show=True)
