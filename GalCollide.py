#!/usr/bin/env python

"""GalCollide.py: Description."""

__author__ = "Michael Lindner"

import matplotlib.pylab as plt
import astropy.units as u
import pynbody
import Parameters as p
from Combine import GalCombine
import ObservationFrame

Gal1 = p.Gal1
Gal2 = p.Gal2
dDelta = p.dDelta
d_perigalactic = p.d_perigalactic
initial_separation = p.initial_separation
eccentricity = p.eccentricity
time = p.time
mDyn = p.mDyn
writename = p.writename
W1 = p.W1
w1 = p.w1
i1 = p.i1
W2 = p.W2
w2 = p.w2
i2 = p.i2
transform = p.transform
observation_frame = p.observation_frame

if (initial_separation < d_perigalactic):
    print("""Error: Initial separation must
           be greater than the perigalactic distance""")
    exit()
else:
    pass

two_bodys = GalCombine(Gal1, Gal2, dDelta,
                       d_perigalactic, initial_separation, eccentricity,
                       time, mDyn, writename, W1, w1, i1, W2, w2, i2,
                       transform)

two_bodys.make_param_file()
two_bodys.make_director_file()
combined = two_bodys.combine()
two_bodys.make_info_file()

test1 = two_bodys.solve_ivp(Gal1)
test2 = two_bodys.solve_ivp(Gal2)

Mass1 = float(Gal1['mass'].sum().in_units('kg')) * u.kg
Mass2 = float(Gal2['mass'].sum().in_units('kg')) * u.kg
MassTot = Mass1 + Mass2

x1 = (test1['y'][0] * u.m).to(u.kpc).value * Mass1 / MassTot
x2 = (test2['y'][0] * u.m).to(u.kpc).value * Mass2 / MassTot
y1 = (test1['y'][1] * u.m).to(u.kpc).value * Mass1 / MassTot
y2 = (test2['y'][1] * u.m).to(u.kpc).value * Mass2 / MassTot

fig, ax = plt.subplots(2)
ax[0].plot(test1['t'], y1)
ax[1].plot(test2['t'], y2)
ax[0].set_ylabel('y')
ax[0].set_xlabel('t')
plt.savefig("./Images/TwoBodyYt_img")

fig, ax = plt.subplots(figsize=(15, 15))

ax.set_ylim(-50, 50)
ax.set_xlim(-50, 50)

ax.scatter(x1[0], y1[0], c='g')
ax.scatter(x2[0], y2[0], c='g')
ax.scatter(x1[1:50], y1[1:50], c='b')
ax.scatter(x2[1:50], y2[1:50], c='r')
plt.savefig("./Images/TwoBodyXY_img")

if observation_frame is True:
    write_file = ObservationFrame.obsTransform(combined)
else:
    write_file = combined

write_file.write(filename=p.writename,
                 fmt=pynbody.tipsy.TipsySnap,
                 cosmological=False)

plt.show()
