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
    cmaps = ['Reds', 'Blues', 'Greens', 'Purples', 'Oranges', 'Greys']

    ax = None
    for i, (comp, cmap) in enumerate(zip(comps, cmaps)):
        ax, _ = f.plotLinesInTime(f"total_component_concentration.{comp}", ax=ax, time_slice=10,
                                  colorbar_label=f"{comp} in time [s]", colorbar_ticks=(i == 0), cmap=cmap)

    ax.set_ylabel("concentration [mol / mol H2O]")

    # # add some guidelines
    # # advection lines
    # if dname != 'surface_tracer_diffusion.regression':
    #     x = np.arange(0., 1000.01, 100.)
    #     X = np.outer(np.array([1,1]), x).transpose()
    #     y = np.array([0., 2.])
    #     Y = np.tile(y, (len(x), 1))
    #     plot_lines.plotLines(X, Y, np.arange(0, len(x), 1), ax=ax, cmap='Greys', linestyle='--', colorbar_label='advected front', colorbar_ticks=False)

    # xs = np.arange(0, 1001, 50)
    # ax.plot(xs, np.ones_like(xs), 'rx', label='expected asymptote Tracer1')
    # ax.plot(xs, 2*np.ones_like(xs), 'bx', label='expected asymptote Tracer2')
    # ax.legend()

    # if dname == 'surface_tracer_advection_dispersion.regression':
    #     ax.set_title('NOTE: Tracer1 and Tracer2 should be identical solutions and plot on top of each other.')

    plt.show()


if __name__ == '__main__':
    dname = sys.argv[-1]
    if not os.path.isdir(dname):
        raise RuntimeError("USAGE: python plot_surface_tracer.py DIRNAME")
    plot(dname)
