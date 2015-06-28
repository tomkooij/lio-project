# -*- coding: utf-8 -*-
"""

Throw CORSIKA results on a single 4 plate HiSPARC station

Monte Carlo parameters:
max_core_distance = maximum distance of station to the shower core (randomised each run)
N = number of simulations

"""


max_core_distance = 100	# m
N = 5000				# monte carlo runs

import tables
import matplotlib.pyplot as plt
import numpy as np

from sapphire.simulations.groundparticles import GroundParticlesGammaSimulation
from sapphire.clusters import SingleStation

FILENAME = 'corsika_713335232_854491062_sorted.h5'    # 1e14 p theta = 0
GAMMAS = 'corsika_no_leptons_sorted.h5'
LEPTONS = 'leptons.h5'

cluster = SingleStation()
#cluster = SingleDiamondStation()

class NoTrigger(GroundParticlesGammaSimulation):
    """
    disable trigger
    """
    def simulate_trigger(self, detector_observables):
        return True


if __name__ == '__main__':
    data = tables.open_file('gp_sim_output.h5', 'w')
    #sim = NoTrigger(GAMMAS, max_core_distance, cluster, data, '/gammas', N, seed=43)
    #sim.run()
    sim = NoTrigger(LEPTONS, max_core_distance, cluster, data, '/leptons', N, seed=43)
    sim.run()
    print "closing datafile... and opening readonly"
    data.close()
    data = tables.open_file('gp_sim_output.h5', 'r')
    #
    #
    nodes = ['/gammas', '/leptons']
    for node in nodes:
        events = data.get_node(node).cluster_simulations.station_0.events
        n1 = events.col('n1')
        plt.hist(n1, bins=np.arange(0.1,4.,0.1), histtype='step')

    plt.title('GroundParticlesGammaSimulation() - trigger disabled - lepton_gamma.py')
    plt.ylabel('counts')
    plt.xlabel('number of particles')
    plt.legend(['gammas', 'leptons'])
    plt.savefig('lepton_gamma.png', dpi=150)
    plt.show()
    data.close()
