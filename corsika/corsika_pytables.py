# -*- coding: utf-8 -*-
"""

Throw CORSIKA results on a single 4 plate HiSPARC station

Monte Carlo parameters:
max_core_distance = maximum distance of station to the shower core (randomised each run)
N = number of simulations

"""


max_core_distance = 400  	# m
N = 200					# monte carlo runs

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

FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
FILENAME_SORTED = 'sorted.h5' # corsika_713335232_854491062.h5 sorted by x

cluster = ScienceParkCluster()


if __name__ == '__main__':
    data1 = tables.open_file('bagger1.h5', 'w')

    #
    # Use GroundParticlesSimulation --> randomize azimuth and core distance
    # we set max core distance to 0, only azimuth is varied
    #
    #sim_old = GroundParticlesSimulation(FILENAME, max_core_distance, cluster, data1, '/', N, seed=42)
    #sim_old.run()
    sim_opt = OptimizeQueryGroundParticlesSimulation(FILENAME_SORTED, max_core_distance, cluster, data1, '/', N, seed=42)
    sim_opt.run()
    #sim_numpy = NumpyGPS(FILENAME, max_core_distance, cluster, data3, '/', N, seed=42)
    #sim_numpy.run()

    #%timeit sim_old.run()
