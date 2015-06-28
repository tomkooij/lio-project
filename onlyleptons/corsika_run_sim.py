# -*- coding: utf-8 -*-
"""

Throw CORSIKA results on a single 4 plate HiSPARC station

Monte Carlo parameters:
max_core_distance = maximum distance of station to the shower core (randomised each run)
N = number of simulations

"""


max_core_distance = 300	    # m
N = 1000					# monte carlo runs

import tables
from timeit import default_timer as timer

from sapphire import GroundParticlesSimulation
from sapphire.clusters import SingleStation

#FILENAME = 'bigcorsika_unsorted.h5'
FILENAME = 'bigcorsika_sorted.h5'    # 1e14 p theta = 0
#FILENAME = 'bigcorsika_split.h5'     # 1e14 p theta = 0

cluster = SingleStation()

if __name__ == '__main__':
    print "Input: ", FILENAME
    data = tables.open_file('gp_sim_output.h5', 'w')
    start = timer()
    sim = GroundParticlesSimulation(FILENAME, max_core_distance, cluster, data, '/simrun', N, seed=42)
    sim.run()
    end = timer()
    print "runtime: ", end - start
    print "closing datafile... "
    data.close()
