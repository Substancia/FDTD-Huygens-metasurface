# import only necessary functions from modules to reduce load
from fdtd_venv import fdtd_mod as fdtd
from numpy import arange, array, where
from matplotlib.pyplot import subplot, plot, xlabel, ylabel, legend, title, suptitle, show, ylim, figure
from scipy.optimize import curve_fit
from os import path
from sys import argv
from time import time


def fit_func(x, a, b, c):
	return a*x**2 + b*x + c


start_time = time()

animate = False
run_time = 400
saveStuff = False
results = True
transmit_detectors = 32

# grid
grid = fdtd.Grid(shape=(200, 15.5e-6, 1), grid_spacing=77.5e-9)
if saveStuff:
	grid.save_simulation(argv[1] if len(argv) > 1 else None)

# objects

# source
#grid[15, 99, 0] = fdtd.PointSource(period = 1550e-9 / (3e8), name="source1")
grid[15, 100, 0] = fdtd.PointSource(period = 1550e-9 / (3e8), name="source2")

# detectors
#grid[80:200, 80:120, 0] = fdtd.BlockDetector(name="BlockDetector")
#grid[80:200, 100, 0] = fdtd.LineDetector(name="LineDetectorVert")
grid[19, 75:125, 0] = fdtd.LineDetector(name="LineDetectorHorIncident")
for i in range(transmit_detectors):
	grid[30+5*i, 75:125, 0] = fdtd.LineDetector(name="LineDetectorHorEmergent_"+str(30+5*i))

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
else:
	if run_time > 0:
		grid.run(total_time=run_time)
	if saveStuff:
		grid.visualize(z=0, show=True, index=0, save=True, folder=grid.folder)
		grid.save_data()
	else:
		grid.visualize(z=0, show=True)

if results:
	phase_profile_incident = []
	phase_profile_emergent = [[] for j in range(transmit_detectors)]		# number of trasmit side detectors
	det_vals_incident = array(grid.detectors[0].detector_values()['E'][-grid.sources[0].period:])
	det_vals_emergent = [array(grid.detectors[i].detector_values()['E'][-grid.sources[0].period:]) for i in range(1, len(phase_profile_emergent)+1)]
	for i in range(len(grid.detectors[0].x)):
		period_phase = grid.sources[0].period - where(det_vals_incident[:, i, 2] == max(det_vals_incident[:, i, 2]))[-1][-1]
		phase_profile_incident.append(((grid.sources[0].period/4 + period_phase)/grid.sources[0].period)%1)
		for j in range(len(phase_profile_emergent)):
			period_phase = grid.sources[0].period - where(det_vals_emergent[j][:, i, 2] == max(det_vals_emergent[j][:, i, 2]))[-1][-1]
			phase_profile_emergent[j].append(((grid.sources[0].period/4 + period_phase)/grid.sources[0].period)%1)
	xdata = array([x for x in range(-25, 25)])
	#phase_difference = (-array(phase_profile_emergent) + array(phase_profile_incident) + 2*pi)%(2*pi)
	#popt, _ = curve_fit(fit_func, xdata, phase_difference)
	figure(num="phase_profile")
	plot(xdata/grid.sources[0].period, phase_profile_incident, label="Incident phase")
	for j in range(len(phase_profile_emergent)):
		plot(xdata/grid.sources[0].period, phase_profile_emergent[j], label="Emergent phase"+str(j))
	#plot(xdata/grid.sources[0].period, phase_difference, label="Phase difference")
	#plot(xdata/grid.sources[0].period, fit_func(xdata, *popt), label="Curve-fit for Phase difference")
	for j in range(len(phase_profile_emergent)):
		popt, _ = curve_fit(fit_func, xdata, phase_profile_emergent[j])
		plot(xdata/grid.sources[0].period, fit_func(xdata, *popt), label="Curve-fit for Phase in detector"+str(j))
		#print(popt)
	xlabel("x/lambda")
	ylabel("phase/2pi")
	legend()
	#title("Curve-fit Phase difference: %5.6f*x**2 + %5.6f*x + %5.6f" % tuple(popt))
	show()

	figure(num="phase_profile_curve_fit")
	for j in range(len(phase_profile_emergent)):
		if j%4 == 0:
			subplot(2, 4, j/4+1)
			title("Detectors %1i to %2i" % tuple([j, j+3]))
			xlabel("x/lambda")
			ylabel("phase/2pi")
			ylim(0, 1)
		popt, _ = curve_fit(fit_func, xdata, phase_profile_emergent[j])
		plot(xdata/grid.sources[0].period, fit_func(xdata, *popt), label="Curve-fit for Phase in detector"+str(j))
		print(popt)
	#legend()
	suptitle("Curve-fiting (Consecutive order of detectors in each plot, blue: 1, orange: 2, green: 3, red: 4)")
	show()
	
	figure(num="phase_bent")
	plot([x for x in range(30, 30+5*len(phase_profile_emergent), 5)], [detector[len(detector)//2] - detector[0] for detector in phase_profile_emergent], label="Phase profile 'bent'")
	plot([x for x in range(30, 30+5*len(phase_profile_emergent), 5)], [0 for x in range(len(phase_profile_emergent))], label="Zero line")
	xlabel("detector position")
	title("Measure of 'bent' of different phase profiles as difference of phases at mid and at end of each detector")
	legend()
	show()

end_time = time()
print("Runtime:", end_time-start_time) 
 
