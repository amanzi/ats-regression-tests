import numpy as np
from matplotlib import pyplot as plt
import ats_xdmf
import colors

import sys,os

def plot(dname, domain):
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
    
        for i in range(0, tcc.shape[0]+1, 10):
            ax.plot(x, tcc[i,:,0], color=cm(i))

    plt.show()


if __name__ == '__main__':
    if sys.argv[-2] == "-s":
        domain = None
    else:
        domain = 'surface'
    plot(sys.argv[-1], domain)
