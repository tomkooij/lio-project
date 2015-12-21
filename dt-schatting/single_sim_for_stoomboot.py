#
# run a single simulation (selected by seed) on stoomboot
#
from __future__ import division

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import SingleTwoDetectorStation

import tables

max_r = 100
N = 1e5
cluster = SingleDiamondStation()

CORSIKAFILE = '/data/hisparc/corsika/data/{seed}/corsika.h5'
OUTPUTFILE = '/data/hisparc/tom/simruns/twodetector/{seed}.h5'

with tables.open_file(OUTPUTFILE, 'w') as data:
    sim = GroundParticlesSimulation(CORSIKAFILE, max_r, cluster, data, '/simrun', N, progress=False)
    sim.run()
    sim.finish()
