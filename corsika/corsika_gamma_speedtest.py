# -*- coding: utf-8 -*-
"""

Investigate performance on small showers (E=small, N=large) (gamma's!)

"""


max_core_distance = 50 	# m
N = int(1e5)				# monte carlo runs

import tables
from timeit import default_timer as timer
import numpy as np

import cProfile
import pstats

from sapphire.simulations.groundparticles import GroundParticlesSimulation
#from sapphire.simulations.groundparticles import NumpyGPS
from sapphire.clusters import SingleStation


cluster = SingleStation()

FILENAME = 'sorted_713335232.h5'



if __name__ == '__main__':

    data_old = tables.open_file('bagger1.h5', 'w')
    data_opt = tables.open_file('bagger2.h5', 'w')

    print "N = ",N
    print "old code pytables_readwhere:"

    start = timer()
    sim_old = GroundParticlesSimulation(FILENAME, max_core_distance, cluster, data_old, '/', N, seed=42)
    #cProfile.run('sim_old.run()', 'runstats')
    sim_old.run()

    end = timer()
    t_old = end - start

    testvalue_old = data_old.root.cluster_simulations.station_0.events

    print "number of coincidences: ", len(testvalue_old)
    """
    print "new code: pytbales_readwhere on x. compress on y and particle_id"

    start = timer()
    #sim_opt = NumpyGPS(FILENAME, max_core_distance, cluster, data_opt, '/', N, seed=42)
    #sim_opt.run()
    end = timer()
    t_opt = end - start

    testvalue =  data_opt.root.cluster_simulations.station_0.events
    print "number of coincidences: ", len(testvalue)

    print "runtime:", t_old, t_opt
    """
    data_old.close()
    data_opt.close()

    #p = pstats.Stats('runstats')
    #p.sort_stats('cumulative').print_stats(10)
