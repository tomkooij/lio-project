# -*- coding: utf-8 -*-
"""

Investigate performance on small showers (E=small, N=large) (gamma's!)

"""


max_core_distance = 50 	# m
N = int(1e3)				# monte carlo runs

import tables
from timeit import default_timer as timer
import numpy as np

import cProfile
import pstats

from multiprocessing import Process
import thread

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.simulations.groundparticles import GroundParticlesGammaSimulation

from sapphire.clusters import SingleStation


cluster = SingleStation()

FILENAME = 'sorted_713335232.h5'


if __name__ == '__main__':

    data_1 = tables.open_file('bagger1.h5', 'w')
    data_2 = tables.open_file('bagger2.h5', 'w')

    print "N = ",N
    print "*****************\n"
    start = timer()
    sim_1 = GroundParticlesSimulation(FILENAME, max_core_distance, cluster, data_1, '/', N, seed=42)
    #cProfile.run('sim_old.run()', 'runstats')
    sim_1.run()
    end = timer()
    t1 = end - start

    start = timer()

    print "blosc"
    sim_2 = GroundParticlesGammaSimulation(FILENAME, max_core_distance, cluster, data_2, '/', N, seed=42)
    sim_2.run()
    end = timer()
    t2 = end - start

    print "runtime: ",t1,t2

    data_1.close()
    data_2.close()

    #p = pstats.Stats('runstats')
    #p.sort_stats('cumulative').print_stats(10)
