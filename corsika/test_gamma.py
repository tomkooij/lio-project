# -*- coding: utf-8 -*-
"""

Test gamma digitisation implementation

"""

max_core_distance = 50 	# m

N = int(1e4)				# monte carlo runs

import tables
import numpy as np

from sapphire.simulations.groundparticles import GroundParticlesGammaSimulation
from sapphire.clusters import BaseCluster


class SingleDetectorStation(BaseCluster):
    """Define a cluster containing a single detector """

    def __init__(self):
        super(SingleDetectorStation, self).__init__()

        detectors = [((0, 0, 0), 'UD')]

        self._add_station((0, 0, 0), 0, detectors)


class TestGammas(GroundParticlesGammaSimulation):
    """
    Overwrite get_particles_in_detector to
    generate only specific gamma's
    disregard corsika hdf5 groundparticle
    """
    def get_particles_in_detector(self, detector):

        E = [1000.]

        gammas = [(0, 0, energy*1e6, 0) for energy in E]

        # no leptons, just gamma's
        return [], np.array(gammas, dtype=np.dtype([('p_x', float),
                            ('p_y', float), ('p_z', float), ('t', float)]))


cluster = SingleDetectorStation()
FILENAME = 'sorted_713335232.h5'  # needs to exist, opened, not used

if __name__ == '__main__':

    data = tables.open_file('gamma_test.h5', 'w')

    print "N = %d \n" % N

    sim = TestGammas(FILENAME, max_core_distance, cluster, data, '/',
                     N, seed=12345)
    sim.run()
    print "number of events: ", \
        len(data.root.coincidences.coincidences.read_where('N==1'))
    print data.root.cluster_simulations.station_0.events

    data.close()
