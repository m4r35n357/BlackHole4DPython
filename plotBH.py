#!/usr/bin/env python

from sys import argv, stderr, exit, stdin
from math import sqrt, sin, cos, fabs
from visual import scene, sphere, curve, points, rate, ellipsoid, ring, color
from json import loads
from array import array
from scipy.interpolate import interp1d, InterpolatedUnivariateSpline
import numpy as np

def isco (a):
    z1 = 1.0 + pow(1.0 - a * a, 1.0 / 3.0) * (pow(1.0 + a, 1.0 / 3.0) + pow(1.0 - a, 1.0 / 3.0))
    z2 = sqrt(3.0 * a * a + z1 * z1)
    if a >= 0.0:
        return 3.0 + z2 - sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))
    else:
        return 3.0 + z2 + sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))

def main():
    if len(argv) < 3:
        raise Exception('>>> ERROR! Please supply values for black hole mass [>= 1.0] and spin [0.0 - 1.0] <<<')
    m = float(argv[1])
    a = float(argv[2])
    horizon = m * (1.0 + sqrt(1.0 - a * a))
    cauchy = m * (1.0 - sqrt(1.0 - a * a))
    #  set up the scene
    scene.center = (0.0, 0.0, 0.0)
    scene.width = scene.height = 1024
    scene.range = (20.0, 20.0, 20.0)
    inner = 2.0 * sqrt(cauchy**2 + a**2)
    ellipsoid(pos = scene.center, length = inner, height = inner, width = 2.0 * cauchy, color = color.blue, opacity = 0.4)  # Inner Horizon
    outer = 2.0 * sqrt(horizon**2 + a**2)
    ellipsoid(pos = scene.center, length = outer, height = outer, width = 2.0 * horizon, color = color.blue, opacity = 0.3)  # Outer Horizon
    ergo = 2.0 * sqrt(4.0 + a**2)
    ellipsoid(pos = scene.center, length = ergo, height = ergo, width = 2.0 * horizon, color = color.gray(0.7), opacity = 0.2)  # Ergosphere
    if fabs(a) > 0.0:
        ring(pos=scene.center, axis=(0, 0, 1), radius = a, color = color.white, thickness=0.01)  # Singularity
    else:
        sphere(pos=scene.center, radius = 0.05, color = color.white)  # Singularity
    ring(pos=scene.center, axis=(0, 0, 1), radius = sqrt(isco(a)**2 + a**2), color = color.magenta, thickness=0.01)  # ISCO
    curve(pos=[(0.0, 0.0, -15.0), (0.0, 0.0, 15.0)], color = color.gray(0.7))
    # animate!
    ball = sphere()  # Particle
    counter = 0
    dataLine = stdin.readline()
    while dataLine:  # build raw data arrays
        rate(60)
        if counter % 1000 == 0:
            ball.visible = False
            ball = sphere(radius = 0.2)  # Particle
            ball.trail = curve(size = 1)  #  trail
        data = loads(dataLine)
        e = float(data['v4e'])
        if e < -120.0:
            ball.color = color.green
        elif e < -90.0:
            ball.color = color.cyan
        elif e < -60.0:
            ball.color = color.yellow
        elif e < -30.0:
            ball.color = color.orange
        else:
            ball.color = color.red
        r = float(data['r'])
        th = float(data['th'])
        ph = float(data['ph'])
        ra = sqrt(r**2 + a**2)
        sth = sin(th)
        ball.pos = (ra * sth * cos(ph), ra * sth * sin(ph), r * cos(th))
        ball.trail.append(pos = ball.pos, color = ball.color)
        counter += 1
        dataLine = stdin.readline()

if __name__ == "__main__":
    main()
else:
    print >> stderr, __name__ + " module loaded"