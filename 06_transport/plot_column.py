import plot_column_data
import os, sys
from matplotlib import pyplot as plt


if __name__ == '__main__':
    dname = sys.argv[-1]
    if not os.path.isdir(dname):
        raise RuntimeError("USAGE: python plot_column.py DIRNAME")

    axs = plot_column_data.plotColumnData([dname,],
                                          color_mode='time',
                                          layout="[[surface-pressure,surface-ponded_depth,surface-total_component_concentration.Tracer1],[pressure,saturation_liquid,total_component_concentration.Tracer1]]",
                                          figsize=(12,8))

    
    plt.show()
