import netCDF4
import numpy as np
dat = netCDF4.Dataset('checkpoint00001.h5')
distributed_precip_rate = dat.variables['snow-precipitation.cell.0']
precip_forcing_rate = 1.0e-5
rel_error = (precip_forcing_rate - np.average(distributed_precip_rate)) / precip_forcing_rate
print('The relative error in precipitation distributiion is ', rel_error)
