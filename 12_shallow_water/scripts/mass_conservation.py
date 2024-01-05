# Script for mass conservation check at different time steps
import h5py
import numpy as np
import matplotlib.pyplot as plt
# Load the data 
f = h5py.File("../testing/ats_vis_network_data.h5", "r")
# Get ponded depth
wa = 'network-wetted_area'
#print(f[wa].keys()) # print time stamps that will have to be inputted into the time_stamps array

# Get time steps
time_steps = f[wa].keys() # find a way to sort the time steps
# print(time_steps)

length = 1
 
# MANUALLY INPUT TIME STAMPS after printing them above
#time_stamps = np.array(['0', '13', '21'])
time_stamps = f[wa].keys()
time_stamps = list(time_stamps);
time_stamps.sort(key=float)
ij = np.argsort(time_stamps)
print(ij)

print('Time stamps length = ')
print(len(time_stamps))

i = 0 # for plotting
l = len(time_stamps)
mass_plot = np.zeros((l,1))

for key in time_stamps:
    w  = f['network-wetted_area'][key]
    d1 = f['network-direction.0'][key]
    d2 = f['network-direction.1'][key]
    #cv = f['network-cell_volume'][key]
    wd = f['network-water_depth'][key]
    mass_array = np.zeros_like(w)
    
    for k in range(len(d1)):
        if (d1[k]==0 and d2[k]==0):
            mass_array[k] = wd[k]*2.0*0.3
        elif (d1[k]==1 and d2[k]==0):
            mass_array[k] = w[k]*2.0
        elif (d1[k]==0 and d2[k]==1):
            mass_array[k] = w[k]*0.3
            
    mass = np.sum(mass_array)
    print('time = ' + key)
    print('mass = ', mass)
    # store value for plotting
    mass_plot[i] = mass
    i = i + 1

# plot Mass vs time step number
fig_name = 'Mass.png'
fig, ax = plt.subplots()
plt.plot(time_stamps, mass_plot, ls = '-', linewidth=3)
plt.xticks(fontsize = 16)
plt.yticks(fontsize = 16)
ax = plt.gca
plt.xlabel('Time stamp', fontsize = 16)
plt.ylabel('Mass', fontsize = 16)
# remove xlabels
plt.xticks([])
# legend properties
plt.legend(loc = 'upper right', fontsize = 14)
plt.legend(frameon = True)
# save figure
#plt.savefig(fig_name, dpi = 400, bbox_inches='tight')
#print('Figure saved = ' + fig_name)
plt.show()


