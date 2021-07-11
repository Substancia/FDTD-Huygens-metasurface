# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
from numpy import sin, radians, tan, meshgrid, arange, flip, array, load
from os import path
#from sys import argv
from time import time

def lens_simulation(source_x_val):
	start_time = time()

	# grid
	grid = fdtd.Grid(shape=(520, 15.5e-6, 1), grid_spacing=77.5e-9)
	grid.save_simulation("R_400_d_40_inverse")

	# objects
	lens_width = 40
	lens_radius = 400
	x, y = arange(-90, 90, 1), arange(lens_radius - lens_width/2, lens_radius, 1)
	X, Y = meshgrid(x, y)
	lens_mask = X**2 + Y**2 <= lens_radius**2
	for j, col in enumerate(lens_mask.T):
		for i, val in enumerate(flip(col)):
			if val:
				grid[30+i:30+lens_width-i, j+10:j+11, 0] = fdtd.Object(permittivity=1.5**2, name=str(i)+","+str(j))
				break

	# source
	grid[source_x_val, 100, 0] = fdtd.PointSource(period=1550e-9/3e8, name="source", pulse=True, cycle=3, hanning_dt=4e-15)

	# detectors
	for i in range(11):
		grid[15, 50+10*i:52+10*i, 0] = fdtd.LineDetector(name="LineDetector"+str(i))

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
		#f.write("\n\tSource dimensions: ")
		#f.write(str(array([grid.source.x[-1] - grid.source.x[0] + 1, grid.source.y[-1] - grid.source.y[0] + 1, grid.source.z[-1] - grid.source.z[0] + 1])/wavelengthUnits))
		f.write("\n\tObject dimensions: ")
		f.write(str([(max(map(max, x)) - min(map(min, x)) + 1)/wavelengthUnits for x in objectRange]))

	for i in range(800):
		grid.run(total_time=1)
		#grid.visualize(z=0, animate=True)
		grid.visualize(z=0, animate=True, index=i, save=True, folder=grid.folder)
	grid.generate_video(delete_frames=True)
	grid.save_data()

	end_time = time()
	print("Runtime:", end_time-start_time)


if __name__ == "__main__":
	lens_simulation(source_x_val=214)
	lens_simulation(source_x_val=127)
