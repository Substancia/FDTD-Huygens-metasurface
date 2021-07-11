from fdtd_venv import fdtd_mod as fdtd
from numpy import meshgrid, arange, flip, array
from scipy.optimize import curve_fit
from os import path
from time import time


def main(wl=40):
	start_time = time()

	animate = False
	run_time = 800
	saveStuff = True

	# grid
	grid = fdtd.Grid(shape=(400, 400, 1), grid_spacing=0.5*77.5e-9)
	if saveStuff:
		grid.save_simulation("lambda_%2i_vs_f" % wl)

	# objects
	lens_width = 40		# in terms of biconvex
	lens_order = 1
	lens_radius = 400
	x, y = arange(-180, 180, 1), arange(lens_radius-lens_order*lens_width/2, lens_radius, 1)
	X, Y = meshgrid(x, y)
	lens_mask = X**2 + Y**2 <= lens_radius**2
	for j, col in enumerate(lens_mask.T):
		for i, val in enumerate(flip(col)):
			if val:
				# biconvex
				grid[60-(lens_width//2)+i%(lens_width//2):60+(lens_width//2)-i%(lens_width//2), j+20:j+21, 0] = fdtd.Object(permittivity=1.5**2, name=str(i)+","+str(j))
				# planoconvex
				#grid[60-(lens_width//2)+i%(lens_width//2):60, j+20:j+21, 0] = fdtd.Object(permittivity=1.5**2, name=str(i)+","+str(j))
				break

	# source
	grid[30, 100:300, 0] = fdtd.LineSource(period = wl/40 * 1550e-9 / (3e8), name="source")

	# detectors
	grid[100:380, 160:240, 0] = fdtd.BlockDetector(name="BlockDetector")

	# x boundaries
	grid[0:20, :, :] = fdtd.PML(name="pml_xlow")
	grid[-20:, :, :] = fdtd.PML(name="pml_xhigh")

	# y boundaries
	grid[:, 0:20, :] = fdtd.PML(name="pml_ylow")
	grid[:, -20:, :] = fdtd.PML(name="pml_yhigh")

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
			fdtd.dB_map_2D(array(grid.detectors[0].detector_values()['E']), file_name="lambda_%2i_vs_f.png" % wl)
	else:
		if run_time > 0:
			grid.run(total_time=run_time)
		if saveStuff:
			grid.visualize(z=0, show=True, index=0, save=True, folder=grid.folder)
			grid.save_data()
			fdtd.dB_map_2D(array(grid.detectors[0].detector_values()['E']), file_name="lambda_%2i_vs_f.png" % wl)
		else:
			grid.visualize(z=0, show=True)

	end_time = time()
	print("Runtime:", end_time-start_time) 


if __name__ == "__main__":
	main(10)	# spatial period of wave set to 10 unit cells
