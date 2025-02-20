import numpy as np
from matplotlib import pyplot as plt
import ats_xdmf
import colors

import sys,os

def plot(dname, domain, interval=10):
    f = ats_xdmf.VisFile(dname, domain)
    f.loadMesh(columnar=True)

    comps = f.search("total_component_concentration")
    x = f.centroids[:,0,0]
    fig, ax = plt.subplots(1,1)

    if len(comps) <= 2:
        cmaps = ['jet', 'viridis_r']
    else:
        cmaps = ['Blues', 'Reds', 'Purples', 'Oranges', 'Greens', 'Greys']

    for i, comp in enumerate(comps):
        print(comp)
        tcc = f.getArray(comp)
        cm = colors.cm_mapper(0, tcc.shape[0]-1, cmaps[i])

        print(f'plotting {tcc.shape[0]} solutions')
        for i in range(0, tcc.shape[0], interval):
            ax.plot(x, tcc[i,:,0], color=cm(i))

    plt.show()


if __name__ == '__main__':
    if sys.argv[-2] == "-s":
        # this is also useful for dilution_test, which is 1D
        # subsurface in x
        domain = None
        interval = 1
    else:
        domain = 'surface'
        interval = 10
    plot(sys.argv[-1], domain, interval)
