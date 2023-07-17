import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_obs(test_name):
    obs_filename = './' + test_name + '.regression.gold/observation.dat'
    df_obs = pd.read_csv(obs_filename, delimiter=' ', comment='#')
    df_obs = df_obs[['time [d]', 'discharge [mol/d]', 
                     'negative_infiltration [mol/d]', 
                     'evaporation [m3/d]']]
    return df_obs


def plot(test_name, ax, label):
    df_test = load_obs(test_name)
    for col in df_test.columns:
        if col == 'time [d]':
            pass
        else:
            idx = list(df_test.columns).index(col)-1
            df_test.plot(x='time [d]', y=col, ax=ax[idx], ylabel=col, label=label, legend=False)
    return ax
    
    
    
if __name__ == '__main__':
    vg_test_name = 'permafrost_vangenuchten_column_singlelayer_realforcing'
    bc_test_name = 'permafrost_brookscorey_column_singlelayer_realforcing'
    bc_sellers_test_name = 'permafrost_brookscorey_column_singlelayer_realforcing_sellers'
    
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    plt.subplots_adjust(left=0.06, right=0.99, top=0.9, wspace=0.25)
    
    ax_vg = plot(vg_test_name, ax, 'van Genuchten rel perm')
    ax_bc = plot(bc_test_name, ax, 'Brooks-Corey based high frozen rel perm')
    ax_bc2 = plot(bc_sellers_test_name, ax, 'Brooks-Corey based high frozen rel perm, Sellers Rsoil')
    ax_bc2[0].legend(bbox_to_anchor=[3.5, 1.12], ncol=3);
    
    plt.show()
    
    
    

    
