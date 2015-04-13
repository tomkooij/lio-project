# -*- coding: utf-8 -*-
"""

Throw CORSIKA results on a single 4 plate HiSPARC station

Monte Carlo parameters:
max_core_distance = maximum distance of station to the shower core (randomised each run)
N = number of simulations

"""


max_core_distance = 400  	# m
N = 100					# monte carlo runs

import tables
import matplotlib.pyplot as plt
import numpy as np

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.simulations.groundparticles import OptimizeQueryGroundParticlesSimulation
from sapphire.simulations.groundparticles import OptimizeQuery_ParticlesOnly_GroundParticlesSimulation
from sapphire.simulations.groundparticles import NumpyGPS

from sapphire.clusters import ScienceParkCluster

#FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 0
#FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 22.5

#FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
#FILENAME_SORTED = 'sorted.h5' # corsika_713335232_854491062.h5 sorted by x
FILENAME = 'corsika_10019744_792483217.h5'  # 1e16 theta = 22.5
FILENAME_SORTED = 'sorted_10019744.h5'

cluster = ScienceParkCluster()


if __name__ == '__main__':
    data_old = tables.open_file('bagger1.h5', 'w')
    data_opt = tables.open_file('bagger2.h5', 'w') 
    #
    # Use GroundParticlesSimulation --> randomize azimuth and core distance
    # we set max core distance to 0, only azimuth is varied
    #
    print "N = ",N
    print "old code:"
    sim_old = GroundParticlesSimulation(FILENAME, max_core_distance, cluster, data_old, '/', N, seed=42)
    sim_old.run()
    testvalue_old = data_old.root.coincidences.coincidences.read_where('N>0') 
    print "number of coincidences: ", len(testvalue_old) 	
 
    print "new code:"
    sim_opt = OptimizeQueryGroundParticlesSimulation(FILENAME_SORTED, max_core_distance, cluster, data_opt, '/', N, seed=42)
    sim_opt.run()
    
    testvalue =  data_opt.root.coincidences.coincidences.read_where('N>0')
    print "number of coincidences: ", len(testvalue)

    print "TEST: coincidence[0]==coincidence[0]", (testvalue_old[0]==testvalue[0]) 
