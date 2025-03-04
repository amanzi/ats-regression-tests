import plot_column_data
import os, sys
from matplotlib import pyplot as plt


if __name__ == '__main__':
    dname = sys.argv[-1]
    if not os.path.isdir(dname):
        raise RuntimeError("USAGE: python plot_diffuse_three.py DIRNAME")

    axs = plot_column_data.plotColumnData([dname,],
                                          color_mode='time',
                                          layout="[total_component_concentration.O2,total_component_concentration.Ar,total_component_concentration.N2O]",
                                          figsize=(12,8))

    
    plt.show()
