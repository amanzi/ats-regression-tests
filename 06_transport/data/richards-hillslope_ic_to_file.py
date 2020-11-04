import h5py
import numpy as np

with h5py.File("./richards-hillslope_steadystate.h5",'w') as fout:
    grp_sat = fout.create_group('saturation_liquid.cell.0')
    grp_flux = fout.create_group('mass_flux.face.0')
    fout.create_dataset('time', data=np.array([0.,],'d'))

    with h5py.File("./richards-hillslope_ic.run/checkpoint_final.h5",'r') as fin:
        grp_sat.create_dataset('0', data=fin['saturation_liquid.cell.0'][:])
        grp_flux.create_dataset('0', data=fin['mass_flux.face.0'][:])
    

   
    
