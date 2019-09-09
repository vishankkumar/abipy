#!/usr/bin/env python

import os
from matplotlib import pyplot as plt
from abipy.core.abinit_units import *
from abipy.abilab import abiopen
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import UnivariateSpline as Spline


# f = '/Users/vishankkumar/Documents/phonons/silicon/1000k/neb_flow/w0/t0/outdata/out_HIST.nc'
f = os.sys.argv[1]
time_step = -1
smoothing = 4

file = abiopen(f)

neb_profile = [(etotal - min(file.reader.read_value('etotal')[time_step])) * Ha_to_eV
               for etotal in file.reader.read_value('etotal')[time_step]]
images = np.arange(len(neb_profile))

fig, ax = plt.subplots()
plt.scatter(images, neb_profile, label='Data points')

# Smoothing the NEB profile
smooth_profile = Spline(x=images[:len(images)-1], y=neb_profile[:len(images)-1], k=smoothing)
smooth_x = np.linspace(0, len(images), 100)

# Plotting the smooth spline
ax.plot(smooth_x, smooth_profile(smooth_x), label='Smoothing spline')
ax.set_xlabel('NEB Images')
ax.set_ylabel('Energy barrier [eV]')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.tight_layout()
plt.legend(frameon='False')
plt.savefig(os.path.dirname(f))
