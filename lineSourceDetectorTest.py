from fdtd_venv import fdtd_mod as fdtd
import numpy as np
import matplotlib.pyplot as plt


grid = fdtd.Grid(shape=(7.75e-6, 15.5e-6, 1), grid_spacing=77.5e-9)

# objects
#grid[-40:-20, 0:15.5e-6, 0] = fdtd.Object(permittivity=10**2)

# source
grid[22, 4e-6:12e-6, 0] = fdtd.LineSource(period=1550e-9 / (3e8), name="source")

# detector
#for i in range(60):
	#grid[(4/3 - np.sin(np.radians(3*i)))*4.65e-6:(4/3 - np.sin(np.radians(3*i+3)))*4.65e-6, (5/3 - np.cos(np.radians(3*i)))*4.65e-6:(5/3 - np.cos(np.radians(3*i+3)))*4.65e-6, 0] = fdtd.LineDetector(name = "detector" + str(i))
for i in range(100):
	grid[22, (4 + 0.08*i)*1e-6:(4 + 0.08*(i+1))*1e-6, 0] = fdtd.LineDetector(name="detector"+str(i))

# x boundaries
grid[0:20, :, :] = fdtd.PML(name="pml_xlow")
grid[-20:, :, :] = fdtd.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:20, :] = fdtd.PML(name="pml_ylow")
grid[:, -20:, :] = fdtd.PML(name="pml_yhigh")

print(grid)

grid.run(total_time=100)
#for i in range(len(grid.detectors)):
	#print(grid.detectors[i].detector_values()['H'][-1])
detector_array = [x.detector_values()['E'][-1] for x in grid.detectors]
#print(detector_array)
grid.visualize(z=0, show=True)

arr = [x[0][2] for x in detector_array]
#for i in detector_array:
	#for j in i:
		#arr.append(j[2])
print(arr)
plt.plot([3*x for x in range(len(arr))], arr)
plt.scatter([3*x for x in range(len(arr))], arr)
plt.show()
 
