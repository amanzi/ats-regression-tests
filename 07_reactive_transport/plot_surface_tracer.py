import numpy as np
from matplotlib import pyplot as plt
import plot_lines
import ats_xdmf
import sys,os


def plot(dname):
    f = ats_xdmf.VisFile(dname, 'surface', time_unit='s')
    f.loadMesh(order=['x',])

    varnames = f.search("total_component_concentration")
    comps = [v.split('.')[1] for v in varnames]
    cmaps = ['Reds', 'Blues']

    ax = None
    for i, (comp, cmap) in enumerate(zip(comps, cmaps)):
        ax, _ = f.plotLinesInTime(f"total_component_concentration.{comp}", ax=ax, time_slice=10,
                                  colorbar_label=f"{comp} in time [s]", colorbar_ticks=(i == 0), cmap=cmap)

    ax.set_ylabel("concentration [mol / mol H2O]")

    plt.show()


if __name__ == '__main__':
    dname = sys.argv[-1]
    if not os.path.isdir(dname):
        raise RuntimeError("USAGE: python plot_surface_tracer.py DIRNAME")
    plot(dname)
