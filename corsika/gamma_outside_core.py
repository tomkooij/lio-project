# -*- coding: utf-8 -*-
"""

Investigate number of events "outside the core"

"""


max_core_distance = 750 	# m
MIN_CORE_DISTANCE = 50      # m

N = int(1e4)				# monte carlo runs

import tables
import numpy as np

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.clusters import SingleStation

from math import sin, cos, sqrt, pi

cluster = SingleStation()

FILENAME = 'sorted_713335232.h5'

class OutsideCoreGPS(GroundParticlesSimulation):
    """
    Overwrite generate_core_distance classmethod (../detector.py)
    to generate events with R > MIN_CORE_DISTANCE 
    """

    @classmethod
    def generate_core_position(cls, R):
        """Generate a random core position within a circle

        :param R: Maximum core distance, in meters.
        :returns: Random x, y position in the disc with radius R.

        """
        assert(MIN_CORE_DISTANCE < R)
        """
        r = sqrt(np.random.uniform(MIN_CORE_DISTANCE**2 , R ** 2))
        phi = np.random.uniform(-pi, pi)
        x = r * cos(phi)
        y = r * sin(phi)
        """
        while 1:
            x = np.random.uniform(-R,R)
            y = np.random.uniform(-R,R)
            if sqrt(x**2+y**2) < R:
                break

        return x, y


if __name__ == '__main__':

    data_1 = tables.open_file('gamma_outside_core.h5', 'w')

    print "N = %d \n" % N

    sim_1 = OutsideCoreGPS(FILENAME, max_core_distance, cluster, data_1, '/', N, seed=42)
    #cProfile.run('sim_old.run()', 'runstats')
    sim_1.run()
    print "number of events: ",len(data_1.root.coincidences.coincidences.read_where('N==1'))
    print data_1.root.cluster_simulations.station_0.events

    # calculate core positions for "detected" events
    x =data_1.root.coincidences.coincidences.read_where('N==1')['x']
    y =data_1.root.coincidences.coincidences.read_where('N==1')['y']
    r = np.sqrt(x**2+y**2)
    print r.size

    data_1.close()
