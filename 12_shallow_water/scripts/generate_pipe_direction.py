# Starting with the simple case of mapping pipe domain to SW domain.
# That is, we have one way manhole coupling going from SW -> pipe, and 
# hence in the evaluator for loop we need the corresponding SW cell c1 = c1(c), \forall c \in \{pipe_cells\}.
import h5py
import numpy as np

filename = "manhole_cell_map.h5" #maps pipe to pipe domain

hfw= h5py.File(filename,"w")

g1 = hfw.create_group('map_cell')
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


