import h5py
import numpy as np

filename = "test.h5"

hfw= h5py.File(filename,"w")

g1 = hfw.create_group('pipe-direction.cell.0')
n1 = np.zeros((100,2))

for i in range(100):
    n1[i][0]=1


g1.create_dataset('0',data=n1)

hfw.close()


