from fdtd_venv import fdtd_mod as fdtd
from numpy import arange, flip, meshgrid, array
from matplotlib.pyplot import plot, show

def main():
	grid = fdtd.Grid(shape=(200, 200, 1), grid_spacing=155e-9)

	lens_width = 10
	lens_order = 3
	lens_radius = 25
	x, y = arange(-90, 90, 1), arange(lens_radius-lens_order*lens_width/2, lens_radius, 1)
	X, Y = meshgrid(x, y)
	lens_mask = X**2 + Y**2 <= lens_radius**2
	for j, col in enumerate(lens_mask.T):
		for i, val in enumerate(flip(col)):
			if val:
				grid[50+i%(lens_width//2):50+lens_width-i%(lens_width//2), j+10:j+11, 0] = fdtd.Object(permittivity=1.5**2, name=str(i)+","+str(j))
				break

	grid[25, 80:120, 0] = fdtd.LineSource(period=1550e-9/3e8, name="source")

	grid[30:130, 100, 0] = fdtd.LineDetector(name="LineDetector")
	grid[30:130, 75:125, 0] = fdtd.BlockDetector(name="BlockDetector")

	grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
	grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")
	grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
	grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

	grid.run(total_time=300)
	grid.visualize(z=0, show=True)
	#E_val = array(grid.detector.detector_values()['E'])
	#arr = []
	#for i in range(100):
		#temp = E_val[:, i, 2]
		#arr.append(max(temp) - min(temp))
	#print("Max index:", 30+arr.index(max(arr)))
	#plot(arange(30, 130, 1), arr)
	#show()
	fdtd.dB_map_2D(array(grid.detectors[1].detector_values()['E'][200:]))

if __name__ == "__main__":
	main()
