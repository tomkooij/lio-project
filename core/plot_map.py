"""
plot map of (simulated) cluster extracted from GroundparticlesSim result file
"""

import matplotlib.pyplot as plt
import tables

RESULTFILE = 'result-11x11.h5'

if __name__ == '__main__':

    with tables.open_file(RESULTFILE, 'r') as data:
        cluster = data.root.coincidences._v_attrs.cluster
        x = [station.x for station in cluster.stations]
        y = [station.y for station in cluster.stations]

        plt.figure()
        plt.title('stations with a single detector')
        plt.scatter(x,y)
        plt.show(block=False)
