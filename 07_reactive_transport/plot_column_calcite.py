import plot_column_data
import os, sys
from matplotlib import pyplot as plt


if __name__ == '__main__':
    dname = sys.argv[-1]
    if not os.path.isdir(dname):
        raise RuntimeError("USAGE: python plot_column_calcite.py DIRNAME")

    axs = plot_column_data.plotColumnData([dname,],
                                          color_mode='time',
                                          layout="[[surface-pressure,surface-ponded_depth,surface-total_component_concentration.H+,surface-total_component_concentration.HCO3-,surface-total_component_concentration.Ca++,surface-total_component_concentration.Tracer],[pressure,saturation_liquid,total_component_concentration.H+,total_component_concentration.HCO3-,total_component_concentration.Ca++,total_component_concentration.Tracer]]",
                                          figsize=(12,8))

    
    plt.show()
