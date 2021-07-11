import numpy as np
import matplotlib.pyplot as plt

def reflRatioS(ei, et, thi, tht = None):
	if (tht == None):
		tht = np.arcsin((ei/et)**0.5 * np.sin(np.radians(thi)))
	return (ei**0.5 * np.cos(np.radians(thi)) - et**0.5 * np.cos(tht)) / (ei**0.5 * np.cos(np.radians(thi)) + et**0.5 * np.cos(tht))

def reflRatioP(ei, et, thi, tht = None):
	if (tht == None):
		tht = np.arcsin((ei/et)**0.5 * np.sin(np.radians(thi)))
	return (et**0.5 * np.cos(np.radians(thi)) - ei**0.5 * np.cos(tht)) / (et**0.5 * np.cos(np.radians(thi)) + ei**0.5 * np.cos(tht))

def transRatioS(ei, et, thi, tht = None):
	if (tht == None):
		tht = np.arcsin((ei/et)**0.5 * np.sin(np.radians(thi)))
	return (2 * ei**0.5 * np.cos(np.radians(thi))) / (ei**0.5 * np.cos(np.radians(thi)) + et**0.5 * np.cos(tht))

def transRatioP(ei, et, thi, tht = None):
	if (tht == None):
		tht = np.arcsin((ei/et)**0.5 * np.sin(np.radians(thi)))
	return (2 * ei**0.5 * np.cos(tht)) / (ei**0.5 * np.cos(np.radians(thi)) + et**0.5 * np.cos(tht))

def printAll(arrays, labels = ['1', '2', '3', '4']):
	i = 0
	while (i < arrays.shape[0]):
		plt.plot(arrays[i], label = labels[i])
		i += 1
	plt.legend()
	plt.show()

