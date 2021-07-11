# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
from numpy import meshgrid, arange, flip, array, load
from os import path
#from sys import argv
from time import time

def lens_simulation(lens_width):
	start_time = time()

	# grid
	grid = fdtd.Grid(shape=(3000, 1400, 1), grid_spacing=77.5e-9)
	grid.save_simulation("R_5737_d_140_metasurface_lensWidth_"+str(lens_width))

	# objects
	#lens_width = 140
	lens_order = 5
	lens_radius = 5737
	x, y = arange(-600, 600, 1), arange(lens_radius - lens_order*lens_width//2, lens_radius, 1)
	X, Y = meshgrid(x, y)
	lens_mask = X**2 + Y**2 <= lens_radius**2
	for j, col in enumerate(lens_mask.T):
		for i, val in enumerate(flip(col)):
			if val:
				grid[130+i%(lens_width//2):130+lens_width-i%(lens_width//2), j+100:j+101, 0] = fdtd.Object(permittivity=1.5**2, name=str(i)+","+str(j))
				break

	# source
	grid[105, 200:1200, 0] = fdtd.LineSource(period = 10 * 1550e-9 / (3e8), name="source")

	# detectors
	#grid[100:750, 80:120, 0] = fdtd.BlockDetector(name="BlockDetector")
	#grid[100:750, 100, 0] = fdtd.LineDetector(name="LineDetectorVert")
	#if peakVal is not None:
		#grid[100+int(peakVal), 60:140, 0] = fdtd.LineDetector(name="LineDetectorHor")

	# x boundaries
	grid[0:100, :, :] = fdtd.PML(name="pml_xlow")
	grid[-100:, :, :] = fdtd.PML(name="pml_xhigh")

	# y boundaries
	grid[:, 0:100, :] = fdtd.PML(name="pml_ylow")
	grid[:, -100:, :] = fdtd.PML(name="pml_yhigh")

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

	for i in range(4000):
		grid.run(total_time=1)
		#grid.visualize(z=0, animate=True)
		grid.visualize(z=0, animate=True, index=i, save=True, folder=grid.folder)
	grid.generate_video(delete_frames=True)
	#grid.save_data()

	#grid.run(total_time=400)
	#grid.visualize(z=0, show=True, index=0, save=True, folder=grid.folder)
	#grid.save_data()
	#grid.visualize(z=0, show=True)

	#df = load(path.join("./fdtd_output", grid.folder, "detector_readings.npz"))
	#fdtd.dB_map_2D(df["BlockDetector (E)"], save_peak="/home/jibin/DDP_Python/peakVal.txt" if peakVal is None else None)

	end_time = time()
	print("Runtime:", end_time-start_time)


if __name__ == "__main__":
	"""
	1. define `save_peak` in `dB_map_2d()` to write peakVal (row number) to '/home/jibin/DDP_Python/peakVal.txt'
	2. escalate permission for this file
	"""
	lens_simulation(lens_width=10)
	lens_simulation(lens_width=20)
	lens_simulation(lens_width=40)
	#with open("/home/jibin/DDP_Python/peakVal.txt", "r") as f:
		#peakVal = f.readline()
	#lens_simulation(peakVal=peakVal)
