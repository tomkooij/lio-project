"""
from: topaz/151013_clusterefficiency
"""


from __future__ import division

import os
import glob

from numpy import isnan, degrees, log10, array, sqrt
import tables
import matplotlib.pyplot as plt

from sapphire.utils import pbar

PATHS = '/data/hisparc/tom/science_park/*.h5'
LOCALPATH = '2*.h5'
#STATIONS = [501, 502, 503, 504, 505, 506, 508, 509]

def get_combined_results():
    zenith = []
    zenith_in = []
    energy_in = []
    size_in = []
    r_in = []

    zenith_init = []
    energy_init = []
    size_init = []
    r_init = []

    #station_query = ' & '.join(str(station) for station in STATIONS)

    print glob.glob(PATHS)

    for path in glob.glob(PATHS):
        print "processing: ", path
        with tables.open_file(path, 'r') as data:
            #print data
            recs = data.root.coincidences.reconstructions
            filtered_recs = recs.read() #_where(station_query)
            print 'number of rows in query: ', len(filtered_recs)
            zenith.extend(degrees(filtered_recs['zenith']))
            zenith_in.extend(degrees(filtered_recs['reference_zenith']))
            energy_in.extend(log10(filtered_recs['energy']))
            size_in.extend(log10(filtered_recs['size']))
            r_in.extend(sqrt(filtered_recs['x']**2 + filtered_recs['y']**2))

            zenith_init.extend(degrees(recs.col('reference_zenith')))
            energy_init.extend(log10(recs.col('reference_energy')))
            size_init.extend(log10(recs.col('reference_size')))
            r_init.extend(sqrt(recs.col('reference_x')**2 + recs.col('reference_y')**2))


    zenith = array(zenith)
    print "%d events before zenith is not NaN filter" % zenith.size
    """
    filter = ~isnan(zenith)

    zenith = zenith.compress(filter)
    print "%d events AFTER zenith is not NaN filter" % zenith.size

    zenith_in = array(zenith_in).compress(filter)
    energy_in = array(energy_in).compress(filter)
    size_in = array(size_in).compress(filter)
    r_in = array(r_in).compress(filter)
    """

    zenith_init = array(zenith_init)
    energy_init = array(energy_init)
    size_init = array(size_init)
    r_init = array(r_init)


    return (zenith, zenith_in, energy_in, size_in, r_in,
            zenith_init, energy_init, size_init, r_init)

def plot_reconstruction_error(r_reconstructed, r):

    print "%d events: " % len(r)

    r = array(r)
    r_reconstructed = array(r_reconstructed)

    delta_r = abs(r_reconstructed - r)

    plt.figure()
    plt.title('11x11 (50mx50m) grid: Core reconstruction error')
    plt.ylabel('delta R [m]')
    plt.xlabel('R [m] = distance from center of grid')
    plt.scatter(r, delta_r)
    plt.plot([50,50],[0,100])




if __name__ == "__main__":

    if not os.path.exists('/data/hisparc'):
        PATHS = LOCALPATH

    zenith, zenith_in, energy_in, size_in, r_in, zenith_init, energy_init, \
        size_init, r_init = get_combined_results()
