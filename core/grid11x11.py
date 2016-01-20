from __future__ import division

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import BaseCluster

import tables

Ngrid = 10  # (n+1) x (n+1) stations with 1 detector each
Dgrid = 10  # m   stations (grid) distance

max_r = 600
N = 10


def make_grid(N_grid = 10, D_grid = 10):
    """
    Create a cluster object with a square grid of stations
    (N_grid+1) x (N_grid+1) stations with a single detector each
    D_grid = distance between each station. (Grid constant)
    """
    transform = lambda x : D_grid * x - N_grid/2 * D_grid
    cluster = BaseCluster()

    for x in range(N_grid+1):
        for y in range(N_grid+1):
            #print "Adding station at: ", transform(x), transform(y)
            cluster._add_station((transform(x),transform(y),0),detectors=[((0,0,0), 'UD')])

    return cluster

CORSIKAFILE = 'corsika.h5'
OUTPUTFILE = 'result-11x11.h5'

#CORSIKAFILE = '/data/hisparc/corsika/data/{seed}/corsika.h5'
#OUTPUTFILE = '/data/hisparc/tom/science_park/{seed}.h5'

cluster = make_grid(Ngrid, Dgrid)

with tables.open_file(OUTPUTFILE, 'w') as data:
    # change progress=False for Stoomboot!
    sim = GroundParticlesSimulation(CORSIKAFILE, max_r, cluster, data, '/', N, progress=True)
    sim.run()
    sim.finish()
