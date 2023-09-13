import h5py
import numpy as np

filename = "pipe_direction.h5"

hfw= h5py.File(filename,"w")

g1 = hfw.create_group('pipe-direction.cell.0')
size = 50
n1 = np.zeros((size,1))

for i in range(size):
    n1[i][0]=1


g1.create_dataset('0',data=n1)

g1 = hfw.create_group('pipe-direction.cell.1')
size = 50
n1 = np.zeros((size,1))

for i in range(size):
    n1[i][0]=0


g1.create_dataset('0',data=n1)


hfw.close()


