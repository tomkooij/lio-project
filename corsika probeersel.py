# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 16:57:46 2014

@author: Tom
"""

import tables

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import *

FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 0 
#FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
#FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 22.5


cluster = SingleStation()
#cluster = SingleDiamondStation()


data = tables.open_file('gp_sim_output.h5', 'w')
#
# Use GroundParticlesSimulation --> randomize azimuth and core distance
# we set max core distance to 0, only azimuth is varied
#
sim = GroundParticlesSimulation(FILENAME, 500, cluster, data, '/simrun', 10000)
sim.run()
