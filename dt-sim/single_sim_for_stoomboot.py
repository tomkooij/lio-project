#
# run a single simulation (selected by seed) on stoomboot
#
from __future__ import division

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import SingleTwoDetectorStation

import tables

max_r = 100
N = int(1e5)
cluster = SingleTwoDetectorStation()

CORSIKAFILE = '/data/hisparc/corsika/data/{seed}/corsika.h5'.format(seed=seed)
OUTPUTFILE = '/data/hisparc/tom/simruns/twodetector/{seed}.h5'.format(seed=seed)

with tables.open_file(OUTPUTFILE, 'w') as data:
    sim = GroundParticlesSimulation(CORSIKAFILE, max_r, cluster, data, '/simrun', N)
    sim.run()
    sim.finish()
