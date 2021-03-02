#from matplotlib.pyplot import plot, show

def create2D(vertices, resolution = 1):
	
	"""
	Divides given 2D geometry and returns an array of smaller shapes. (Incomplete!)
	Geometry needs at least one horizontal/vertical edge, ends being marked at beginning and end of vertices list.
	
	Arguments:-
	vertices (list): List of cartesian coordinates of vertices of geometry
	resolution (int): Smallest unit used for smaller shapes (multiples of Yee cells)
	"""

	horizontal, vertical = [], []
	
	# Check for horizontal edges
	if vertices[0][1] == vertices[-1][1]:
		horizontal = [vertices[0], vertices[-1]]
	
	# Check for vertical edges
	if vertices[0][0] == vertices[-1][0]:
		vertical = [vertices[0], vertices[-1]]
	
	# Check for obtuse angles
	if len(horizontal) > 0:
		for x in vertices[1:-1]:
			if not horizontal[0][0] <= x[0] <= horizontal[1][0]:
				print("Obtuse")
	elif len(vertical) > 0:
		for x in vertices[1:-1]:
			if not vertical[0][1] <= x[1] <= vertical[1][1]:
				print("Obtuse")

def createTriangle(vertices, resolution = 1):
	
	"""
	Creates a staircase triangle with an array of small pillars.
	coordinates given should form a right angled triangle with two sides parallel to grid axes.
	
	Arguments:-
	vertices (list): List of cartesian coordinates of vertices of triangle
	resolution (int): Smallest unit used for smaller shapes (multiples of Yee cells)
	"""
	
	if vertices[1][1] == vertices[2][1]:
		height, ratio = vertices[0][0] - vertices[1][0], (vertices[1][0] - vertices[0][0]) / (vertices[2][1] - vertices[0][1])
	elif vertices[1][1] == vertices[0][1]:
		height, ratio = 0, (vertices[0][0] - vertices[1][0]) / (vertices[2][1] - vertices[0][1])
	else:
		raise Exception("Please specify a RIGHT ANGLED TRIANGLE")
	grid = [[[vertices[1][0] + round(height + (x - vertices[0][1])*ratio), x], [vertices[0][0], x + resolution]] for x in range(vertices[0][1], vertices[2][1], resolution)]
	
	return standardizeList(grid)

def standardizeList(List):		# Converts grid array into format easily usable with FDTD module
	for x in List:
		if x[0][0] == x[1][0] or x[0][1] == x[1][1]:
			List.remove(x)
	for n, x in enumerate(List):
		if x[0][0] > x[1][0]:
			List[n][0][0], List[n][1][0] = List[n][1][0], List[n][0][0]
		if x[0][1] > x[1][1]:
			List[n][0][1], List[n][1][1] = List[n][1][1], List[n][0][1]
	
	return List

if __name__ == "__main__":
	grid = createTriangle([[0, 0], [10, 5], [0, 5]], 1)
	print(grid)
	#plot([x[0][1] for x in grid], [-x[0][0] for x in grid])
	#show()
