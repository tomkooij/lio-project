# -*- coding: utf-8 -*-
"""

Throw CORSIKA results on a single 4 plate HiSPARC station

Monte Carlo parameters:
max_core_distance = maximum distance of station to the shower core (randomised each run)
N = number of simulations

"""


from __future__ import division

max_core_distance = 100	# m
N = int(1e6)					# monte carlo runs


import tables
import matplotlib.pyplot as plt
import numpy as np

from math import sqrt
from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import BaseCluster

class BigDiamond(BaseCluster):

    """Define a cluster containing a single diamond shaped station
    Detectors 1, 3 and 4 are in the usual position for a 4 detector
    layout, detector 2 is moved out of the center and positioned to
    create a second equilateral triangle with detectors 1, 2 and 4.
    """

    def __init__(self):
        super(BigDiamond, self).__init__()

        # size 100m 
        station_size = 20
        a = station_size / 2
        b = a * sqrt(3)
        detectors = [((0., b, 0), 'UD'), ((a * 2, b, 0), 'UD'),
                     ((-a, 0., 0), 'LR'), ((a, 0., 0), 'LR')]

        self._add_station((0, 0, 0), 0, detectors)



#FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 22.5
#FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 22.5
FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 0

OUTPUTFILE = 'simulated_no_fotons_bigdiamond.h5'

cluster = BigDiamond()

if __name__ == '__main__':
    data = tables.open_file(OUTPUTFILE, 'w')

    print "detector layout = ", [d.get_coordinates() for d in cluster.stations[0].detectors]
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
