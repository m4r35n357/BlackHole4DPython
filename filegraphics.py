#!/usr/bin/env python

from sys import argv, stderr, exit
from math import sqrt, sin, fabs
from visual import scene, sphere, curve, points, rate, ellipsoid, ring
from json import loads
from array import array
from scipy.interpolate import interp1d
import numpy as np

def isco (a):
	z1 = 1.0 + pow(1.0 - a * a, 1.0 / 3.0) * (pow(1.0 + a, 1.0 / 3.0) + pow(1.0 - a, 1.0 / 3.0))
	z2 = sqrt(3.0 * a * a + z1 * z1)
	if a >= 0.0:
		return 3.0 + z2 - sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))
	else:
		return 3.0 + z2 + sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))

def main():
	if len(argv) < 4:
		raise Exception('>>> ERROR! Please supply a data file name, a parameter file name, and the number of points to use <<<')
	dataFile = open(argv[1], 'r')
	parameterFile = open(argv[2], 'r')
	nData = int(argv[3])
	# get parameters
        try:
            parameters = loads(parameterFile.read())
        except ValueError as e:
            print('PARAMETER ERROR: ' + str(e))
            exit(-1)		
	a = parameters['a']
	m = parameters['M']
	horizon = m * (1.0 + sqrt(1.0 - a * a));
	cauchy = m * (1.0 - sqrt(1.0 - a * a));
	# get raw data
        line = dataFile.readline()
	tau = array('d')
	x = array('d')
	y = array('d')
	z = array('d')
	e = array('d')
	tauMax = 0.0
	while line:
		p = loads(line)
		tauValue = p['tau']
		tauMax = tauValue if tauValue > tauMax else tauMax
		tau.append(tauValue)
		x.append(p['x'])
		y.append(p['y'])
		z.append(p['z'])
		e.append(p['v4e'])
		line = dataFile.readline()
	# interpolate here
        try:
		xI = interp1d(tau, x, kind='linear')
		yI = interp1d(tau, y, kind='linear')
		zI = interp1d(tau, z, kind='linear')
		eI = interp1d(tau, e, kind='linear')
        except ValueError as e:
            print('DATA ERROR: ' + str(argv[0]) + ': ' + str(e))
            exit(-2)		
	tauI = np.linspace(0, tauMax, num = nData)
	#  set up the scene
	scene.center = (0.0, 0.0, 0.0)
	scene.width = scene.height = 1000.0
	scene.range = (20.0, 20.0, 20.0)
	colours = [ (1.0, 1.0, 1.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.7, 0.7, 0.7), (0.5, 0.5, 0.0), (0.5, 0.0, 0.5), (0.0, 1.0, 1.0), (1.0, 1.0, 0.0), (0.0, 0.0, 0.0) ]
        inner = 2.0 * sqrt(cauchy**2 + a**2)
	ellipsoid(pos = scene.center, length = inner, height = inner, width = 2.0 * cauchy, color = colours[3], opacity = 0.4)  # Inner Horizon
        outer = 2.0 * sqrt(horizon**2 + a**2)
	ellipsoid(pos = scene.center, length = outer, height = outer, width = 2.0 * horizon, color = colours[3], opacity = 0.3)  # Outer Horizon
        ergo = 2.0 * sqrt(4.0 + a**2)
	ellipsoid(pos = scene.center, length = ergo, height = ergo, width = 2.0 * horizon, color = colours[4], opacity = 0.2)  # Ergosphere
        if fabs(a) > 0.0:
	    ring(pos=scene.center, axis=(0, 0, 1), radius = a, color = colours[0], thickness=0.01)  # Singularity
        else:
            sphere(pos=scene.center, radius = 0.05, color = colours[0])  # Singularity
	ring(pos=scene.center, axis=(0, 0, 1), radius = sqrt(isco(a)**2 + a**2), color = colours[6], thickness=0.01)  # ISCO
	ball = sphere(pos = (xI(tauI[0]), yI(tauI[0]), zI(tauI[0])), radius = 0.2)  # Particle
	ball.trail = curve(size = 1)  #  trail
	# animate!
	for i in range(len(tauI)):
		rate(60)
		error = eI(tauI[i])
		if error < -120.0:
			colour = colours[2]
		elif error < -90.0:
			colour = colours[7]
		elif error < -60.0:
			colour = colours[8]
		else:
			colour = colours[1]
		ball.color = colour
		position = (xI(tauI[i]), yI(tauI[i]), zI(tauI[i]))
		ball.pos = position
		ball.trail.append(pos = position, color = colour, retain = 10000)

if __name__ == "__main__":
	main()
else:
	print >> stderr, __name__ + " module loaded"

