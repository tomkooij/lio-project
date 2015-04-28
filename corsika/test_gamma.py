# -*- coding: utf-8 -*-
"""

Test gamma digitisation implementation

"""


max_core_distance = 50 	# m

N = int(1e4)				# monte carlo runs

import tables
import numpy as np

from sapphire.simulations.groundparticles import GroundParticlesGammaSimulation
from sapphire.clusters import SingleStation

cluster = SingleStation()

FILENAME = 'sorted_713335232.h5'


class TestGammas(GroundParticlesGammaSimulation):
    """
    Overwrite get_particles_in_detector to
    generate only specific gamma's
    disregard corsika hdf5 groundparticle
    """
    def get_particles_in_detector(self, detector):

        E = [10.0]

        gammas = [(0, 0, energy*1e6, 0) for energy in E]

        # no leptons, just gamma's
        return [], np.array(gammas, dtype=np.dtype([('p_x', float),
                            ('p_y', float), ('p_z', float), ('t', float)]))

if __name__ == '__main__':

    data = tables.open_file('gamma_test.h5', 'w')

    print "N = %d \n" % N

    sim = TestGammas(FILENAME, max_core_distance, cluster, data, '/',
                     N, seed=42)
    sim.run()
    print "number of events: ", \
        len(data.root.coincidences.coincidences.read_where('N==1'))
    print data.root.cluster_simulations.station_0.events

    data.close()
