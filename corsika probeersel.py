# -*- coding: utf-8 -*-
"""
Created on Mon Oct 06 16:57:46 2014

@author: Tom
"""

import tables

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import ScienceParkCluster

data = tables.open_file('test_groundparticle_simulation.h5', 'w')
cluster = ScienceParkCluster()

sim = GroundParticlesSimulation('corsika.h5', 500, cluster, data, '/', 100)
sim.run()