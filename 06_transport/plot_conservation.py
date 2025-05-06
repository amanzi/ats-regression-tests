import sys, os
import numpy as np
from matplotlib import pyplot as plt
import ats_xdmf
import colors

def getName(domain, varname, comp=None):
    if domain is None or domain == '':
        res = varname
    else:
        res = domain + '-' + varname

    if comp is not None:
        res = res + '.' + comp
    return res

def checkConservation(dirname, subsurface=True, surface=True):

    def getDomain(domain):
        qty = dict()
        f = ats_xdmf.VisFile(dirname, domain)
        f.loadMesh(columnar=True)

        lwc = f.getArray(getName(domain, 'liquid_water_content'))
        for varname in f.search('total_component_concentration'):
            split = varname.split('.')
            assert(len(split) == 2)
            component = split[1]

            # conserved quantity is tcc * lwc + solid_qty
            tcc_name = getName(domain, 'total_component_concentration', component)
            solid_name = getName(domain, 'solid_residue_quantity', component)

            conserved = f.getArray(tcc_name)*lwc + f.getArray(solid_name)
            while len(conserved.shape) > 1:
                conserved = conserved.sum(axis=-1)

            qty[component] = conserved

        return f.times, qty

    if subsurface:
        times, qty_sub = getDomain(None)

        if surface:
            _, qty_surf = getDomain('surface')
            qty = dict()
            for k in qty_sub.keys():
                assert k in qty_surf
                qty[k] = qty_surf[k] + qty_sub[k]
        else:
            qty = qty_sub

    elif surface:
        times, qty = getDomain('surface')

    fig, ax = plt.subplots(1,1)
        
    # check conservation
    cm = colors.enumerated_colors(20)
    for i, k in enumerate(qty):
        diff = np.abs(qty[k][1:] - qty[k][0])
        print(k, diff.min(), diff.mean(), diff.max())

        plt.plot(times, qty[k], color=cm[i])
        try:
            plt.plot(times, qty_surf[k], '--', color=cm[i])
        except AttributeError:
            pass

        try:
            plt.plot(times, qty_sub[k], '-.', color=cm[i])
        except AttributeError:
            pass
            

if __name__ == "__main__":
    dirname = sys.argv[-1]
    assert os.path.isdir(dirname)
    sub = os.path.isfile(os.path.join(dirname, 'ats_vis_data.h5'))
    surf = os.path.isfile(os.path.join(dirname, 'ats_vis_surface_data.h5'))
    checkConservation(dirname, sub, surf)
    plt.show()
