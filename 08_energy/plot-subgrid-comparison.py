import numpy as np
from matplotlib import pyplot as plt

import ats_xdmf
import colors

def load(dirname):
    star = 'star' in dirname
    if star:
        v_surf = ats_xdmf.VisFile(f'./energy-{dirname}.regression', domain='surface_column_0')
        v_snow = ats_xdmf.VisFile(f'./energy-{dirname}.regression', domain='snow_column_0')
    else:
        v_surf = ats_xdmf.VisFile(f'./energy-{dirname}.regression', domain='surface')
        v_snow = ats_xdmf.VisFile(f'./energy-{dirname}.regression', domain='snow')
    return v_surf, v_snow

def plot(axs1, v_surf, v_snow, color, label):
    axs1[0].plot(v_surf.times, v_surf.getArray('evaporative_flux'), '-', color=color, label=f'evap flux ({label})')
    axs1[0].plot(v_snow.times, v_snow.getArray('source_sink'), '--', color=color, label=f'snow source ({label})')

    axs1[1].plot(v_surf.times, v_surf.getArray('temperature'), '-', color=color, label=f'surface temperature ({label})')
    axs1[1].plot(v_snow.times, v_snow.getArray('temperature'), '--', color=color, label=f'snow temperature ({label})')

    subgrid = 'subgrid' in label
    if subgrid:
        axs1[2].plot(v_surf.times, v_surf.getArray('volumetric_ponded_depth'), '-', color=color, label=f'ponded (vol) depth ({label})')
    else:
        axs1[2].plot(v_surf.times, v_surf.getArray('ponded_depth'), '-', color=color, label=f'ponded depth ({label})')

    axs1[2].plot(v_snow.times, v_snow.getArray('water_equivalent'), '--', color=color, label=f'SWE ({label})') # NOTE: this relies on surface area = 1 as SWE in m^3

    if subgrid:
        axs1[3].plot(v_surf.times, v_surf.getArray('fractional_areas.cell.2'), '-', color=color, label=f'frac area snow ({label})')
    else:
        axs1[3].plot(v_surf.times, v_surf.getArray('fractional_areas.cell.1'), '-', color=color, label=f'frac area snow ({label})')

def plot_snow_precip(axs1, v_surf, v_snow):
    axs1[0].plot(v_snow.times, v_snow.getArray('precipitation'), '-', color='gray', label=f'snow precip')

def decorate(axs1):
    axs1[3].set_xlabel('time [d]')
    axs1[0].set_ylabel('flux [m/s]')
    axs1[1].set_ylabel('temperature [K]')
    axs1[2].set_ylabel('depth [m]')
    axs1[3].set_ylabel('fractional area [-]')
    for ax in axs1:
        ax.legend()

if __name__ == '__main__':
    dnames = ['permafrost', 'permafrost_subgrid', 'permafrost_subgrid_star']
    labels = ['control', 'subgrid=0', 'subgrid=0,star']
    cols = colors.enumerated_colors(len(dnames))

    fig = plt.figure()
    axs = fig.subplots(4,1)
    
    for dname, color, label in zip(dnames, cols, labels):
        v_surf, v_snow = load(dname)
        plot(axs, v_surf, v_snow, color, label)

    plot_snow_precip(axs, v_surf, v_snow)
    decorate(axs)
    plt.show()
