# -*- coding: utf-8 -*-
"""

Compare histograms between  GroundParticlesSimulation and
    GroundParticlesGammaSimulation

part of test sapphire:GroundParticlesGammaSimulation (pull request #60)

Apr28, 2015: Passed!

"""


max_core_distance = 50 	# m
N = int(5e4)				# monte carlo runs

import tables
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt


from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.simulations.groundparticles import GroundParticlesGammaSimulation

from sapphire.clusters import SingleStation


cluster = SingleStation()

FILENAME = 'sorted_713335232.h5'


if __name__ == '__main__':

    data_1 = tables.open_file('leptons.h5', 'w')
    data_2 = tables.open_file('leptons_and_gamma.h5', 'w')

    print "N = ", N
    print "*****************\n"
    start = timer()
    sim_1 = GroundParticlesSimulation(FILENAME, max_core_distance, cluster,
                                     data_1, '/', N, seed=51)
    # cProfile.run('sim_old.run()', 'runstats')
    sim_1.run()
    end = timer()
    t1 = end - start

    start = timer()

    print "GroundParticlesGammaSimulation: "
    sim_2 = GroundParticlesGammaSimulation(FILENAME, max_core_distance,
                                           cluster, data_2, '/', N, seed=51)
    sim_2.run()
    end = timer()
    t2 = end - start

    print "runtime: ", t1, t2

    events1 = data_1.root.cluster_simulations.station_0.events
    n1 = events1.col('n1')
    events2 = data_2.root.cluster_simulations.station_0.events
    n2 = events2.col('n1')

    plt.figure()
    plt.hist(n1, bins=np.arange(0.1, 5, 0.1), histtype='step')
    plt.hist(n2, bins=np.arange(0.1, 5, 0.1), histtype='step')
    plt.show()

    data_1.close()
    data_2.close()
