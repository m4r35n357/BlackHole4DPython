#!/usr/bin/env python
'''
Copyright (c) 2014, 2015, 2016, Ian Smith (m4r35n357)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
from sys import argv, stderr, exit, stdin
from math import sqrt, sin, cos, tan, fabs, pi
from visual import scene, sphere, curve, points, rate, ellipsoid, ring, color, cone
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
    #cone(pos=(0,0,12), axis=(0,0,-12), radius=12.0 * tan(0.15 * pi), opacity=0.2)
    #cone(pos=(0,0,-12), axis=(0,0,12), radius=12.0 * tan(0.15 * pi), opacity=0.2)
    #sphere(pos=(0,0,0), radius=3.0, opacity=0.2)
    #sphere(pos=(0,0,0), radius=12.0, opacity=0.1)
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
