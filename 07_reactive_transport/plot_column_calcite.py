import plot_column_data
import os, sys
from matplotlib import pyplot as plt


if __name__ == '__main__':
    dname = sys.argv[-1]
    if not os.path.isdir(dname):
        raise RuntimeError("USAGE: python plot_column_calcite.py DIRNAME")

    hco3_key = 'HCO3-'

    fig = plt.figure(figsize=(12,8))
    
    def plot(hco3_key, surf_hco3_key):
        axs = plot_column_data.plotColumnData([dname,],
                                              color_mode='time',
                                              layout=f"[[surface-pressure,surface-ponded_depth,surface-total_component_concentration.H+,surface-total_component_concentration.{surf_hco3_key},surface-total_component_concentration.Ca++,surface-total_component_concentration.Tracer],[pressure,saturation_liquid,total_component_concentration.H+,total_component_concentration.{hco3_key},total_component_concentration.Ca++,total_component_concentration.Tracer]]",
                                              fig=fig)

    try:
        plot('HCO3-', 'HCO3-')
    except KeyError:
        plt.clf()
        try:
            plot('HCO3', 'HCO3-')
        except KeyError:
            plt.clf()
            try:            
                plot('HCO3', 'HCO3')
            except KeyError:
                plt.clf()
                plot('HCO3-', 'HCO3')
    
    plt.show()
