from __future__ import division

import os
import math

from numpy.random import choice

from sapphire import CorsikaQuery
from sapphire.qsub import check_queue, submit_job
from sapphire.utils import pbar
from sapphire.simulations.detector import HiSPARCSimulation


NUMBER_OF_JOBS = 10

max_r = 200  #
N = int(1e3)
ENERGY_LOG10 = 17

OVERVIEW_LOCAL = '../science_park/corsika_overview.h5'
OVERVIEW = '/data/hisparc/corsika/corsika_overview.h5'

SCRIPT = """\
#!/usr/bin/env bash

python << END
from __future__ import division

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import BaseCluster

import tables

Ngrid = 10  # (n+1) x (n+1) stations with 1 detector each
Dgrid = 10  # m   stations (grid) distance

max_r = {max_r}
N = {N}


def make_grid(N_grid = 10, D_grid = 10):
    # Create a cluster object with a square grid of stations
    
    transform = lambda x : D_grid * x - N_grid/2 * D_grid
    cluster = BaseCluster()

    for x in range(N_grid+1):
        for y in range(N_grid+1):
            #print "Adding station at: ", transform(x), transform(y)
            cluster._add_station((transform(x),transform(y),0),detectors=[((0,0,0), 'UD')])

    return cluster

CORSIKAFILE = '/data/hisparc/corsika/data/{seed}/corsika.h5'
OUTPUTFILE = '/data/hisparc/tom/grid/{seed}.h5'

cluster = make_grid(Ngrid, Dgrid)

with tables.open_file(OUTPUTFILE, 'w') as data:
    sim = GroundParticlesSimulation(CORSIKAFILE, max_r, cluster, data, '/', N, progress=False)
    sim.run()
    sim.finish()

#
END

"""

def round_to_7_5(x, base=7.5):
    return base * round(float(x)/base)

def perform_simulations():
    query = CorsikaQuery(OVERVIEW)

    for job in range(NUMBER_OF_JOBS):

        zenith = round_to_7_5(math.degrees(HiSPARCSimulation.generate_zenith()))

        print "starting job %d of %d, zenith = %2.1f" % (job, NUMBER_OF_JOBS, zenith)

        # make a list of all seeds that match the query, and chose a single random seed
        seed = choice(query.seeds(query.simulations(energy=ENERGY_LOG10, zenith=zenith)))

        print "seed %s (E=1e%d, zenith=%2.1f)" % (seed, ENERGY_LOG10, zenith)

        if not os.path.exists('/data/hisparc/corsika/data/{seeds}/corsika.h5'.format(seeds=seed)):
            print "/data/hisparc/corsika/data/{seeds}/corsika.h5 does not exist".format(seeds=seed)
            continue

        perform_job(seed, 'short')

    query.finish()


def perform_job(seeds, queue):
    script = SCRIPT.format(seed=seeds, N=N, max_r=max_r)
    submit_job(script, seeds, queue)


if __name__ == "__main__":
    if not os.path.exists('/data/hisparc'):
        # local test
        OVERVIEW = OVERVIEW_LOCAL

    perform_simulations()
