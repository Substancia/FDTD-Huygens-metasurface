from fdtd_venv import fdtd_mod as fdtd
from numpy import sin, cos, radians
from createGeometry import createTriangle

grid = fdtd.Grid(shape=(9.3e-6, 15.5e-6, 1), grid_spacing=77.5e-9)

grid[60, 50, 0] = fdtd.PointSource(period=1550e-9 / (3e8), name="source")

#theta = 30
#grid[3.9e-6:(3.9 - 2*sin(radians(theta/2)))*1e-6, 5.8e-6:(5.8 + 2*cos(radians(theta/2)))*1e-6, 0] = fdtd.Object(permittivity=100, name="objectLeft")
#grid[4.3e-6:(4.3 + 2*sin(radians(theta/2)))*1e-6, 5.8e-6:(5.8 + 2*cos(radians(theta/2)))*1e-6, 0] = fdtd.Object(permittivity=100, name="objectRight")

hornLeft = createTriangle([[53, 48], [58, 48], [53, 58]])
hornRight = createTriangle([[67, 48], [62, 48], [67, 58]])
for i in range(len(hornLeft)):
	grid[hornLeft[i][0][0]:hornLeft[i][1][0], hornLeft[i][0][1]:hornLeft[i][1][1], 0] = fdtd.Object(permittivity=100, name="objectLeft"+str(i))
	grid[hornRight[i][0][0]:hornRight[i][1][0], hornRight[i][0][1]:hornRight[i][1][1], 0] = fdtd.Object(permittivity=100, name="objectRight"+str(i))

#grid.run(total_time=50)
#grid.visualize(z=0, show=True)
for i in range(100):
	grid.run(total_time=1)
	grid.visualize(z=0, animate=True)
