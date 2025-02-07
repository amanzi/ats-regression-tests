import numpy as np
from matplotlib import pyplot as plt
import ats_xdmf
import colors

import sys,os

def plot(dname):
    f = ats_xdmf.VisFile(dname, 'surface')
    f.loadMesh(columnar=True)

    tcc1 = f.getArray('surface-total_component_concentration.Tracer1')
    tcc2 = f.getArray('surface-total_component_concentration.Tracer2')

    cm1 = colors.cm_mapper(0, tcc1.shape[0]-1, 'Reds')
    cm2 = colors.cm_mapper(0, tcc2.shape[0]-1, 'Blues')

    x = f.centroids[:,0,0]
    
    fig, ax = plt.subplots(1,1)
    for i in range(0, tcc1.shape[0]+1, 10):
        ax.plot(x, tcc1[i,:,0], color=cm1(i))
        ax.plot(x, tcc2[i,:,0], color=cm2(i))

    plt.show()


if __name__ == '__main__':
    plot(sys.argv[-1])
