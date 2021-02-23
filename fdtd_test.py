import fdtd
import numpy as np

grid = fdtd.Grid(shape=(15e-6, 15e-6, 1), )

# objects
grid[7e-6:10e-6, 0:15e-6, 0] = fdtd.Object(permittivity=2.42**2)

# source
grid[1.5e-6:np.tan(np.radians(30))*9.0e-6, 6.0e-6:13.5e-6, 0] = fdtd.LineSource(period = 1550e-9 / (3e8), name="source")

# detector
grid[12e-6, :, 0] = fdtd.LineDetector(name="detector")

# x boundaries
grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

print(grid)

#for i in range(0, 100):
    #grid.run(total_time=1)

grid.run(total_time=100)
grid.visualize(z=0)
