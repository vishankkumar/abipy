#!/usr/bin/env python

import os
from matplotlib import pyplot as plt
from abipy.core.abinit_units import *
from abipy.abilab import abiopen
from matplotlib.ticker import MaxNLocator
from scipy.interpolate import UnivariateSpline as Spline
from pymatgen.plot_set import set_mpl


set_mpl(scale=2)
# f = '/Users/vishankkumar/Documents/phonons/silicon/1000k/neb_flow/w0/t0/outdata/out_HIST.nc'
f = os.sys.argv[1]
param = os.sys.argv
file = []
for p in param[1:]:
    print(p)
    file.append(p)
print('Files passed for plotting: {}'.format(file))
time_step = -1
smoothing = 4
fig, ax = plt.subplots()

for f in file:
    if f.endswith('.nc'):
        file = abiopen(f)

        neb_profile = [(etotal - min(file.reader.read_value('etotal')[time_step])) * Ha_to_eV
                       for etotal in file.reader.read_value('etotal')[time_step]]
        images = np.arange(len(neb_profile))
    elif f.endswith('.csv'):
        x, neb_profile = np.loadtxt(f,delimiter=',',skiprows=1, usecols=(0,4), unpack=True)
        images = np.arange(len(x))

    plt.scatter(images, neb_profile, label=r'$\Delta E$ = ' + str(np.round(max(neb_profile) - min(neb_profile), 4)))

    # Smoothing the NEB profile
    smooth_profile = Spline(x=images, y=neb_profile, k=smoothing)
    smooth_x = np.linspace(0, len(images)-1, 100)

    # Plotting the smooth spline
    ax.plot(smooth_x, smooth_profile(smooth_x))
    ax.set_xlabel('NEB Images')
    ax.set_ylabel('Energy barrier [eV]')
    # ax.text(max(smooth_x)/2.0 - 0.5, min(neb_profile) + 0.5 * max(neb_profile),
    #         r'$\Delta E$ = ' + str(np.round(max(neb_profile) - min(neb_profile), 4)))
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.tight_layout()
plt.legend(frameon='False')
# plt.savefig(os.path.dirname(f))
plt.show()