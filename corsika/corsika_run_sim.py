# -*- coding: utf-8 -*-
"""

Throw CORSIKA results on a single 4 plate HiSPARC station

Monte Carlo parameters:
max_core_distance = maximum distance of station to the shower core (randomised each run)
N = number of simulations

"""

max_core_distance = 3000 	# m
N = 100000					# monte carlo runs

import tables

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import *

#FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 0
#FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 22.5


cluster = SingleStation()
#cluster = SingleDiamondStation()


data = tables.open_file('gp_sim_output.h5', 'w')
#
# Use GroundParticlesSimulation --> randomize azimuth and core distance
# we set max core distance to 0, only azimuth is varied
#
sim = GroundParticlesSimulation(FILENAME, max_core_distance, cluster, data, '/simrun', N)
sim.run()
print "closing datafile..."
data.close()
#data = tables.open_file('gp_sim_output.h5', 'r')
#
#
