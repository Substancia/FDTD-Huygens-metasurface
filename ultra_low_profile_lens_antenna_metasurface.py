# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
from numpy import sin, radians, tan, meshgrid, arange, flip, array
from os import path
from sys import argv
from time import time

start_time = time()

animate = False
run = False
saveStuff = False

# grid
grid = fdtd.Grid(shape=(260, 15.5e-6, 1), grid_spacing=77.5e-9)
if saveStuff:
	grid.save_simulation(argv[1] if len(argv) > 1 else None)

# objects
grid[36:40, 96:104, 0] = fdtd.Object(permittivity=1.5**2, name="h1")
grid[37:40, 104:108, 0] = fdtd.Object(permittivity=1.5**2, name="h2")
grid[38:40, 108:112, 0] = fdtd.Object(permittivity=1.5**2, name="h3")
grid[33:40, 112:116, 0] = fdtd.Object(permittivity=1.5**2, name="h4")
grid[34:40, 116:120, 0] = fdtd.Object(permittivity=1.5**2, name="h5")
grid[35:40, 120:124, 0] = fdtd.Object(permittivity=1.5**2, name="h6")
grid[34:40, 124:128, 0] = fdtd.Object(permittivity=1.5**2, name="h7")
grid[37:40, 128:132, 0] = fdtd.Object(permittivity=1.5**2, name="h8")
grid[39:40, 132:136, 0] = fdtd.Object(permittivity=1.5**2, name="h9")
grid[34:40, 136:140, 0] = fdtd.Object(permittivity=1.5**2, name="h10")
grid[35:40, 140:144, 0] = fdtd.Object(permittivity=1.5**2, name="h11")
grid[36:40, 144:148, 0] = fdtd.Object(permittivity=1.5**2, name="h12")
grid[37:40, 148:152, 0] = fdtd.Object(permittivity=1.5**2, name="h13")
	#left
grid[37:40, 92:96, 0] = fdtd.Object(permittivity=1.5**2, name="h-2")
grid[38:40, 88:92, 0] = fdtd.Object(permittivity=1.5**2, name="h-3")
grid[33:40, 84:88, 0] = fdtd.Object(permittivity=1.5**2, name="h-4")
grid[34:40, 80:84, 0] = fdtd.Object(permittivity=1.5**2, name="h-5")
grid[35:40, 76:80, 0] = fdtd.Object(permittivity=1.5**2, name="h-6")
grid[34:40, 72:76, 0] = fdtd.Object(permittivity=1.5**2, name="h-7")
grid[37:40, 68:72, 0] = fdtd.Object(permittivity=1.5**2, name="h-8")
grid[39:40, 64:68, 0] = fdtd.Object(permittivity=1.5**2, name="h-9")
grid[34:40, 60:64, 0] = fdtd.Object(permittivity=1.5**2, name="h-10")
grid[35:40, 56:60, 0] = fdtd.Object(permittivity=1.5**2, name="h-11")
grid[36:40, 52:56, 0] = fdtd.Object(permittivity=1.5**2, name="h-12")
grid[37:40, 48:52, 0] = fdtd.Object(permittivity=1.5**2, name="h-13")
#lens_width = 5
#lens_orders = 5
#x, y = arange(-90, 90, 1), arange(200-lens_orders*lens_width, 200, 1)
#X, Y = meshgrid(x, y)
#lens_mask = X**2 + Y**2 <= 40000
#for j, col in enumerate(lens_mask.T):
	#for i, val in enumerate(flip(col)):
		#if val:
			#grid[30+lens_width+i%lens_width:40, j+10:j+11, 0] = fdtd.Object(permittivity=1.5**2, name=str(i)+","+str(j))
			#grid[30+i%lens_width:32+lens_width-i%lens_width, j+10:j+11, 0] = fdtd.Object(permittivity=1.5**2, name=str(i)+","+str(j))
			#break


# source
grid[15, 20:180, 0] = fdtd.LineSource(period = 1550e-9 / (3e8), name="source")

# detectors
grid[50:250, 80:120, 0] = fdtd.BlockDetector(name="BlockDetector")
grid[50:250, 100, 0] = fdtd.LineDetector(name="LineDetectorVert")
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
		#f.write("\n\tObject dimensions: ")
		#f.write(str([(max(map(max, x)) - min(map(min, x)) + 1)/wavelengthUnits for x in objectRange]))

if animate:
	if run:
		for i in range(400):
			grid.run(total_time=1)
			if saveStuff:
				grid.visualize(z=0, animate=True, index=i, save=True, folder=grid.folder)
			else:
				grid.visualize(z=0, animate=True)
	if saveStuff:
		grid.generate_video(delete_frames=True)
		grid.save_data()
else:
	if run:
		grid.run(total_time=400)
	if saveStuff:
		grid.visualize(z=0, show=True, index=0, save=True, folder=grid.folder)
		grid.save_data()
	else:
		grid.visualize(z=0, show=True)

end_time = time()
print("Runtime:", end_time-start_time)
 
