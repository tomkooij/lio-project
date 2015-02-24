# -*- coding: utf-8 -*-
"""
Plot gamma energy histogram at groundlevel
x,y in meters!
p_x, p_y, p_z in eV

"""
import tables
import matplotlib.pyplot as plt
import numpy as np


FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 0
#FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
#FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 22.5

if __name__=='__main__':
    data = tables.open_file(FILENAME, 'r')
    gp = data.root.groundparticles


    id = gp.col('particle_id')
    t = gp.col('t')
    x = gp.col('x')
    y = gp.col('y')
    r = gp.col('r')
    p_x = gp.col('p_x')
    p_y = gp.col('p_y')
    p_z = gp.col('p_z')
    phi = gp.col('phi')

    p = np.sqrt(p_x**2+p_y**2+p_z**2)/1e6  # total momentum [MeV]

    p_gamma = p.compress(id==1)
    #electron = p.compress((id==3)
    plt.figure()
    plt.hist(p_gamma, bins=np.arange(0,5,.01))
    plt.show()

    data.close()
