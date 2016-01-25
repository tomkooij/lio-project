"""
plot map of (simulated) cluster extracted from GroundparticlesSim result file
"""

import matplotlib.pyplot as plt
import tables

RESULTFILE = 'small.h5'

if __name__ == '__main__':

    with tables.open_file(RESULTFILE, 'r') as data:
        cluster = data.root.coincidences._v_attrs.cluster
        x = [station.x for station in cluster.stations]
        y = [station.y for station in cluster.stations]

        plt.figure()
        plt.title('stations with a single detector')
        plt.scatter(x,y)
        plt.show(block=False)

        recs = data.root.coincidences.reconstructions.read()

        for rec in recs:
            # figure out which station is active and plot
            reconstructed_core = (rec['x'], rec['y'])
            core = (rec['reference_x'], rec['reference_y'])
            print core, reconstructed_core
