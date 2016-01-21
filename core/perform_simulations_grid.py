from __future__ import division

import os
import math

from numpy.random import choice

from sapphire import CorsikaQuery
from sapphire.qsub import check_queue, submit_job, create_script
from sapphire.utils import pbar
from sapphire.simulations.detector import HiSPARCSimulation


NUMBER_OF_JOBS = 10

max_r = 100  #
N = 1000
ENERGY_LOG10 = 16

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


class GroundParticlesSimulationNoTrigger(GroundParticlesSimulation):
    # overwrite simulate_trigger for stations with a single detector
    def simulate_trigger(self, detector_observables):

        n_detectors = len(detector_observables)
        detectors_low = sum([True for observables in detector_observables
                             if observables['n'] > 0.3])
        detectors_high = sum([True for observables in detector_observables
                              if observables['n'] > 0.5])

        if n_detectors == 4 and (detectors_high >= 2 or detectors_low >= 3):
            return True
        elif n_detectors == 2 and detectors_low >= 2:
            return True
        elif n_detectors == 1 and detectors_low == 1:
            return True
        else:
            return False


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
    sim = GroundParticlesSimulationNoTrigger(CORSIKAFILE, max_r, cluster, data, '/', N, progress=False)
    sim.run()
    sim.finish()

#
END

"""

def round_to_7_5(x, base=7.5):
    return base * round(float(x)/base)

def perform_simulations(TEST=False):
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

        perform_job(seed, 'long')

    query.finish()


def perform_job(seeds, queue):
    script = SCRIPT.format(seed=seeds, N=N, max_r=max_r)
    submit_job(script, seeds, queue)
    #print create_script(script, 'test')


if __name__ == "__main__":
    if not os.path.exists('/data/hisparc'):
        # local test
        OVERVIEW = OVERVIEW_LOCAL

    perform_simulations()
