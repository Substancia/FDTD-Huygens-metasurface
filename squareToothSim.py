import numpy as np
import matplotlib.pyplot as plt

def sqtooth(th, src = [], W = 30, w = 20, h = 20, n = 10, steps = 1500, stepSize = 0.1):
	"""
	Inputs:-
		th (angle with normal)
		src (x, y coords of source mid; default = 100 away from center in th direction)
		W (width of beam; default = 30)
		w (width of tooth; default = 20)
		h (height of tooth; default = 20)
		n (number of waves in beam; default = 10)
		steps (number of steps taken by wave; default = 1500)
		stepSize (size of each step; default = 0.1)
	Output:-
		Array of wave paths as array of position of each wave at each timestep (dimensions: 2)
	"""
	th = np.radians(th)
	if len(src) == 0: src = [-100 * np.sin(th), max(100 * np.cos(th), W/2)]
	beam = [(pos*np.cos(th) + src[0], pos*np.sin(th) + src[1]) for pos in np.linspace(-W/2, W/2, n)]
	print('\nsrc:', src, '\nW', W, '\nth', th, '\nh', h, '\nw', w, '\nn', n, '\nsteps', steps, '\nstepSize', stepSize)
	print('\nBeam starts from', beam, '\n')
	beamEnd = []
	beamPaths = []
	beamEndDirections = []
	for wave in beam:
		print('Considering wave', wave, '...')
		beamPath = []
		x, y = wave
		dx, dy = stepSize * np.sin(th), stepSize * np.cos(th)
		i = 0
		while (i < steps):
			if ((y >= 0 and y < stepSize) and (x < -w/2 or x > w/2)) or ((y >= h and y < h + stepSize) and (x > -w/2 and x < w/2)): dy = stepSize * np.cos(np.pi - th)
			if (x <= -w/2 and x >= -w/2 - stepSize) and y < h: dx = stepSize * np.sin(-th)
			x, y = x + dx, y - dy
			i += 1
			beamPath.append((x, y))
			#print('Position:', (x, y))
		beamEnd.append((x, y))
		beamPaths.append(beamPath)
		beamEndDirections.append(dx)
		print('End point:', x, ',', y, '\n')
	print('All waves terminated; End points:-\n', beamEnd)
	forward = len([x for x in beamEndDirections if x >= 0])
	reverse = len([x for x in beamEndDirections if x < 0])
	print('Forward reflection:', forward, '/', n, ' = ', forward/n)
	print('Reverse reflection:', reverse, '/', n, ' = ', reverse/n)
	return beamPaths

def printArray(arr, w = 20, h = 20):
	"""
	Prints multiple arrays on same plot (with square tooth add-on)
	
	Input:-
		arr (list of arrays)
		w (width of tooth; default = 20)
		h (height of tooth; default = 20)
	"""
	i = 0
	for wave in arr:
		arrT = [[x[0] for x in wave], [x[1] for x in wave]]
		plt.plot(arrT[0], arrT[1], label = i)
		i += 1
	plt.plot([-100, -w/2, -w/2, w/2, w/2, 100], [0, 0, h, h, 0, 0], label = 'tooth')
	plt.xlim(-100, 100)
	plt.ylim(-2, 100)
	#plt.legend()
	plt.show()

if __name__ == "__main__":
	th = np.radians(60)
	printArray(sqtooth(60, [-100 * np.sin(th), 100 * np.cos(th) + 18]))
