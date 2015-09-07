# -*- coding: utf-8 -*-
"""

Throw CORSIKA results on a single 4 plate HiSPARC station

Monte Carlo parameters:
max_core_distance = maximum distance of station to the shower core (randomised each run)
N = number of simulations

"""


max_core_distance = 300	# m
N = int(1e6)					# monte carlo runs

import tables
import matplotlib.pyplot as plt
import numpy as np

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import *

#FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 0
FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
#FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 22.5

OUTPUTFILE = 'simulated_no_fotons_200k_simB.h5'

cluster = SingleStation()
#cluster = SingleDiamondStation()

if __name__ == '__main__':
    data = tables.open_file(OUTPUTFILE, 'w')
    #
    # Use GroundParticlesSimulation --> randomize azimuth and core distance
    # we set max core distance to 0, only azimuth is varied
    #
    sim = GroundParticlesSimulation(FILENAME, max_core_distance, cluster, data, '/simrun', N)
    sim.run()
    print "closing datafile... and opening readonly"
    data.close()
    data = tables.open_file(OUTPUTFILE, 'r')
    #
    #
    events = data.root.simrun.cluster_simulations.station_0.events
    n1 = events.col('n1')
    plt.hist(n1, bins=np.arange(0,4.,0.1))
    plt.show()
    data.close()
