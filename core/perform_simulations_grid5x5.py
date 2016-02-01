from __future__ import division

import os
import math

from numpy.random import choice

from sapphire import CorsikaQuery
from sapphire.qsub import check_queue, submit_job, create_script
from sapphire.utils import pbar
from sapphire.simulations.detector import HiSPARCSimulation


NUMBER_OF_JOBS = 10

max_r = 40  #
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

Ngrid = 4  # (n+1) x (n+1) stations with 1 detector each
Dgrid = 10  # m   stations (grid) distance

max_r = {max_r}
N = {N}


class GroundParticlesSimulationModifiedTrigger(GroundParticlesSimulation):
    # overwrite simulate_trigger for stations with a single detector
    #  use simulated low trigger for the single detector
    def simulate_trigger(self, detector_observables):

        n_detectors = len(detector_observables)
        detectors_low = sum([True for observables in detector_observables
                             if observables['n'] > 0.3])

        if n_detectors == 1 and detectors_low == 1:
            return True
        else:
            return False

    def simulate_gps(self, station_observables, shower_parameters, station):
    # overwrite simulate_gps to set t_trigger (needed for dirrec) even if n_dectectors == 1

        arrival_times = [station_observables['t%d' % id]
                         for id in range(1, 5)
                         if station_observables.get('n%d' % id, -1) > 0]

        if len(arrival_times) == 1:
            trigger_time = arrival_times[0]
            
            ext_timestamp = shower_parameters['ext_timestamp']
            ext_timestamp += int(trigger_time + station.gps_offset +
                                 self.simulate_gps_uncertainty())
            timestamp = int(ext_timestamp / int(1e9))
            nanoseconds = int(ext_timestamp % int(1e9))

            gps_timestamp = {{ 'ext_timestamp': ext_timestamp,
                             'timestamp': timestamp,
                             'nanoseconds': nanoseconds,
                             't_trigger': trigger_time}}
            station_observables.update(gps_timestamp)

            return station_observables

        else:
            return super(GroundParticlesSimulation, self).simulate_gps(station_observables, shower_parameters, station)


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
OUTPUTFILE = '/data/hisparc/tom/grid/5x5/{seed}.h5'

cluster = make_grid(Ngrid, Dgrid)

with tables.open_file(OUTPUTFILE, 'w') as data:
    sim = GroundParticlesSimulationModifiedTrigger(CORSIKAFILE, max_r, cluster, data, '/', N, progress=False)
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

        perform_job(seed, 'short')

    query.finish()


def perform_job(seeds, queue):
    script = SCRIPT.format(seed=seeds, N=N, max_r=max_r)
    #submit_job(script, seeds, queue)
    print create_script(script, 'test')


if __name__ == "__main__":
    if not os.path.exists('/data/hisparc'):
        # local test
        OVERVIEW = OVERVIEW_LOCAL

    perform_simulations()
