import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as plta
import ats_xdmf
import colors

import sys,os


def plot(dname, vmax=0.1, i=0):
    f = ats_xdmf.VisFile(dname, 'surface', time_unit='s')
    f.loadMesh(order=['x','y'], shape=(100,100))

    tcc1 = f.getArray('surface-total_component_concentration.Tracer1')
    tcc2 = f.getArray('surface-total_component_concentration.Tracer2')
    print(tcc1.shape)

    cm1 = colors.cm_mapper(0, tcc1.shape[0]-1, 'Reds')
    cm2 = colors.cm_mapper(0, tcc2.shape[0]-1, 'Blues')

    if vmax is None:
        vmax1 = tcc1[i,:,:].max()
    else:
        vmax1 = vmax

    fig, ax = plt.subplots(1,2)
    pc1 = ax[0].pcolormesh(f.centroids[:,:,0],
                           f.centroids[:,:,1],
                           tcc1[i,:,:],
                           vmin=0, vmax=vmax1)
    ax[0].set_xlabel('tcc 1')
    fig.colorbar(pc1, ax=ax[0])
    print(tcc1[i,:,:])

    if vmax is None:
        vmax2 = tcc2[i,:,:].max()
    else:
        vmax2 = vmax

    pc2 = ax[1].pcolormesh(f.centroids[:,:,0],
                           f.centroids[:,:,1],
                           tcc2[i,:,:],
                           vmin=0.0, vmax=vmax2)
    ax[1].set_xlabel('tcc 2')

    fig.colorbar(pc2, ax=ax[1])
    print(tcc2[i,:,:])

    title = fig.suptitle(f'time = {np.round(f.times[i], 1)}')

    if i < 0:
        def animate(i):
            pc1.set_array(tcc1[i,:,:])
            pc2.set_array(tcc2[i,:,:])
            fig.suptitle(f'time = {np.round(f.times[i], 1)}')
            return pc1,pc2

        ani = plta.FuncAnimation(fig, animate, frames=tcc1.shape[0], interval=300)
    plt.show()


if __name__ == '__main__':
    dname = sys.argv[-1]
    print(len(sys.argv))
    if len(sys.argv) >= 3:
        i = sys.argv[-2]
    else:
        i = 0

    plot(dname, 2, int(i))
