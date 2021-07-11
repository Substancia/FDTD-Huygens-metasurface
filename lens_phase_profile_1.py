# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
from numpy import meshgrid, arange, flip, array, where, pi
from matplotlib.pyplot import subplot, plot, xlabel, ylabel, legend, title, suptitle, show, ylim, figure, scatter, subplots_adjust
from scipy.optimize import curve_fit
from os import path
from sys import argv
from time import time


def fit_func(x, a, b, c):
	return a*x**2 + b*x + c


def main(wl=40):
	start_time = time()

	animate = False
	run_time = 800
	saveStuff = True
	results = True
	transmit_detectors = 32

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
				#grid[30-(lens_width//2)+i%(lens_width//2):30, j+10:j+11, 0] = fdtd.Object(permittivity=1.5**2, name=str(i)+","+str(j))
				break

	# source
	grid[30, 100:300, 0] = fdtd.LineSource(period = wl/40 * 1550e-9 / (3e8), name="source")

	# detectors
	#grid[100:380, 160:240, 0] = fdtd.BlockDetector(name="BlockDetector")
	#grid[100:380, 200, 0] = fdtd.LineDetector(name="LineDetectorVert")
	grid[39, 150:250, 0] = fdtd.LineDetector(name="LineDetectorHorIncident")
	for i in range(transmit_detectors):
		grid[80+10*i, 150:250, 0] = fdtd.LineDetector(name="LineDetectorHorEmergent_"+str(30+5*i))

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

	#for i in range(400):
		#grid.run(total_time=1)
		#grid.visualize(z=0, animate=True)
		#grid.visualize(z=0, animate=True, index=i, save=True, folder=grid.folder)
	#grid.generate_video(delete_frames=True)
	#grid.save_data()

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
			#fdtd.dB_map_2D(array(grid.detectors[0].detector_values()['E']), file_name="lambda_%2i_vs_f.png" % wl)
	else:
		if run_time > 0:
			grid.run(total_time=run_time)
		if saveStuff:
			grid.visualize(z=0, show=True, index=0, save=True, folder=grid.folder)
			grid.save_data()
			#fdtd.dB_map_2D(array(grid.detectors[0].detector_values()['E']), file_name="lambda_%2i_vs_f.png" % wl)
		else:
			grid.visualize(z=0, show=True)

	if results:
		phase_profile_incident = []
		phase_profile_emergent = [[] for j in range(transmit_detectors)]		# number of trasmit side detectors
		det_vals_incident = array(grid.detectors[0].detector_values()['E'][-grid.source.period:])
		det_vals_emergent = [array(grid.detectors[i].detector_values()['E'][-grid.source.period:]) for i in range(1, len(phase_profile_emergent)+1)]
		for i in range(len(grid.detectors[0].x)):
			period_phase = grid.source.period - where(det_vals_incident[:, i, 2] == max(det_vals_incident[:, i, 2]))[-1][-1]
			phase_profile_incident.append(((grid.source.period/4 + period_phase)/grid.source.period)%1)
			for j in range(len(phase_profile_emergent)):
				period_phase = grid.source.period - where(det_vals_emergent[j][:, i, 2] == max(det_vals_emergent[j][:, i, 2]))[-1][-1]
				phase_profile_emergent[j].append(((grid.source.period/4 + period_phase)/grid.source.period)%1)
		xdata = array([x for x in range(-50, 50)])
		for i, detector in enumerate(phase_profile_emergent):
			prev = detector[0]
			for j, val in enumerate(detector):
				if abs(val-prev) > 0.7:
					phase_profile_emergent[i][j] = val-abs(val-prev)/(val-prev)
				prev = phase_profile_emergent[i][j]
		#phase_difference = (-array(phase_profile_emergent) + array(phase_profile_incident) + 2*pi)%(2*pi)
		#popt, _ = curve_fit(fit_func, xdata, phase_difference)
		figure(num="phase_profile")
		plot(xdata/grid.source.period, phase_profile_incident, label="Incident phase")
		for j in range(len(phase_profile_emergent)):
			plot(xdata/grid.source.period, phase_profile_emergent[j], label="Emergent phase"+str(j))
		#plot(xdata/grid.source.period, phase_difference, label="Phase difference")
		#plot(xdata/grid.source.period, fit_func(xdata, *popt), label="Curve-fit for Phase difference")
		for j in range(len(phase_profile_emergent)):
			popt, _ = curve_fit(fit_func, xdata, phase_profile_emergent[j])
			plot(xdata/grid.source.period, fit_func(xdata, *popt), label="Curve-fit for Phase in detector"+str(j))
			#print(popt)
		xlabel("x/lambda")
		ylabel("phase/2pi")
		legend()
		#title("Curve-fit Phase difference: %5.6f*x**2 + %5.6f*x + %5.6f" % tuple(popt))
		show()
		
		figure(num="phase_profile")
		for j in range(len(phase_profile_emergent)):
			if j%4 == 0:
				subplot(2, 4, j/4+1)
				title("Detectors %1i to %2i" % tuple([j, j+3]))
				xlabel("x/lambda")
				ylabel("phase/2pi")
				ylim(0, 1.5)
			popt, _ = curve_fit(fit_func, xdata, phase_profile_emergent[j])
			plot(xdata/grid.source.period, phase_profile_emergent[j], label="Phase in detector"+str(j))
			#print(popt)
		#legend()
		subplots_adjust(wspace=0.4, hspace=0.4)
		suptitle("Phase at detectors (Consecutive order of detectors in each plot, blue: 1, orange: 2, green: 3, red: 4)")
		show()
		
		figure(num="phase_profile_curve_fit")
		popt = [[] for x in range(len(phase_profile_emergent))]
		for j in range(len(phase_profile_emergent)):
			if j%4 == 0:
				subplot(2, 4, j/4+1)
				title("Detectors %1i to %2i" % tuple([j, j+3]))
				xlabel("x/lambda")
				ylabel("phase/2pi")
				ylim(0, 1.5)
			popt[j], _ = curve_fit(fit_func, xdata, phase_profile_emergent[j])
			plot(xdata/grid.source.period, fit_func(xdata, *popt[j]), label="Curve-fit for Phase in detector"+str(j))
			print(fit_func(array([0, xdata[0]]), *popt[j]))
		#legend()
		subplots_adjust(wspace=0.4, hspace=0.4)
		suptitle("Curve-fiting (Consecutive order of detectors in each plot, blue: 1, orange: 2, green: 3, red: 4)")
		show()
		
		figure(num="phase_bent")
		#plot([x for x in range(30, 30+5*len(phase_profile_emergent), 5)], [detector[len(detector)//2] - detector[0] for detector in phase_profile_emergent], label="Phase profile 'bent'")
		plot([x for x in range(80, 80+10*len(phase_profile_emergent), 10)], [fit_func(0, *detector) - fit_func(xdata[0], *detector) for detector in popt], label="Phase profile curvature inverse")
		#plot([x for x in range(30, 30+5*len(phase_profile_emergent), 5)], [((detector[1]/detector[0])**2-(detector[2]/detector[0]))**0.5 for detector in popt], label="Phase profile curvature")
		#scatter([x for x in range(30, 30+5*len(phase_profile_emergent), 5)], [detector[len(detector)//2] - detector[0] for detector in phase_profile_emergent], c=[["blue", "orange", "green", "red"][x%4] for x in range(len(phase_profile_emergent))])
		scatter([x for x in range(80, 80+10*len(phase_profile_emergent), 10)], [fit_func(0, *detector) - fit_func(xdata[0], *detector) for detector in popt], c=[["blue", "orange", "green", "red"][x%4] for x in range(len(phase_profile_emergent))])
		#scatter([x for x in range(30, 30+5*len(phase_profile_emergent), 5)], [((detector[1]/detector[0])**2-(detector[2]/detector[0]))**0.5 for detector in popt], c=[["blue", "orange", "green", "red"][x%4] for x in range(len(phase_profile_emergent))])
		plot([x for x in range(80, 80+10*len(phase_profile_emergent), 10)], [0 for x in range(len(phase_profile_emergent))], label="Zero line")
		xlabel("Detector position")
		ylabel("1/Curvature")
		title("Curvature of different phase profiles")
		legend()
		show()

	del grid
	end_time = time()
	print("Runtime:", end_time-start_time) 


if __name__ == "__main__":
	main(int(argv[1]))
