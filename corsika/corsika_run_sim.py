# -*- coding: utf-8 -*-
"""

Throw CORSIKA results on a single 4 plate HiSPARC station

sep-2015:
-use the new diamond configuration
-print CORSIKA datafile stats before running

Monte Carlo parameters:
max_core_distance = maximum distance of station to the shower core (randomised each run)
N = number of simulations

"""
from __future__ import division

DEBUG = 1

max_core_distance = 50	# m
N = int(1e5)					# monte carlo runs

import tables
import matplotlib.pyplot as plt
import numpy as np
import math

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import SingleDiamondStation, ScienceParkCluster

#FILENAME = 'corsika_834927089_144221120.h5'    # SIM C 1e14 p theta = 0
FILENAME = 'corsika_713335232_854491062.h5'    # SIM B 1e14 p theta = 0
#FILENAME = 'corsika_77102826_200916071.h5'     # SIM A 1e14  p theta = 22.5

OUTPUTFILE = 'simulated_no_fotons_test.h5'

cluster = SingleDiamondStation()
#cluster = ScienceParkCluster()

if __name__ == '__main__':
    corsikafile = tables.open_file(FILENAME, 'r')

    eventheader = corsikafile.get_node_attr('/', 'event_header')
    print "CORSIKA Inputfile: ", FILENAME
    print "primary particle: %s energy: E+%d zenith: %2.1f" % (eventheader.particle, math.log10(eventheader.energy),
            math.degrees(eventheader.zenith))
    corsikafile.close()
    data = tables.open_file(OUTPUTFILE, 'w')
    #
    # print cluster/station/detectors
    if DEBUG:
        for station in cluster.stations:
            print "station: ", station.station_id
            for detector_number, detector in enumerate(station.detectors):
                print station.station_id,':',detector_number, detector.get_coordinates()
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
