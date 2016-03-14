# try station offsets
from __future__ import division

import tables
import os
from sapphire import download_coincidences
from datetime import datetime
from sapphire import ReconstructESDCoincidences
from math import pi
import numpy as np
import pylab as plt

from polar_hist import polar_hist

STATIONS = (501, 504, 505)
#STATIONS = (501, 502, 505)
# station 501-502 = +8ns
# station 501-505 = +22ns
# manually changing the station offsets in sapphire removes big sinewave
FILENAME = 'test_%d_%d_%d.h5' % STATIONS

start = datetime(2014,1,1)
end = datetime(2014,12,31)
x
c:lass MonkeyPatchedRecESD(ReconstructESDCoincidences):
    def get_station_timing_offsets(self):
        self.offsets = {
                        501: [0., 0., 0., 0.],
                        502: [8.,8.,8.,8.],
                        504: [32.,32.,32.,32.],
                        505: [22.,22.,22.,22.]}

    def reconstruct(self, station_numbers=None):
        """Shorthand function to reconstruct coincidences and store results"""

        print "WARNING: MONKEY PATCHED ReconstructESDCoincidences. no cores. return theta, phi"
        self.prepare_output()
        self.get_station_timing_offsets()
        self.reconstruct_directions(station_numbers=station_numbers)
        #self.reconstruct_cores(station_numbers=station_numbers)
        self.store_reconstructions()
        return self.theta, self.phi

def open():
    if os.path.exists(FILENAME):
        print "%s exist: opening" % FILENAME
        return tables.open_file(FILENAME, 'a')
    else:
        data = tables.open_file(FILENAME, 'a')
        download_coincidences(data, stations=STATIONS, start=start, end=end, n=3)
        return data

def make_plot(phi ):
    ax.hist(phi, bins=20, histtype='step')
    #ax.title('%s azimuth angle' % str(STATIONS)
    #ax.xlabel('azimuth (rad) from east over north')
    #ax.ylabel('counts')
    ax.set_xlim(-pi,pi)
    #savefig('azimuth.png', dpi=200)


if __name__ == '__main__':
    print "stations: ", STATIONS
    #print "uptime (days):", get_number_of_hours_with_data(STATIONS, start=start, end=end)/24

    data = open()  # keep open for interactive...

    t_ = data.root.coincidences.reconstructions.col('zenith')
    t_ = t_.compress(~np.isnan(t_))
    p_ = data.root.coincidences.reconstructions.col('azimuth')
    p_ = p_.compress(~np.isnan(p_))

    try:
        data.get_node('/coincidences/rec_offsets')
        print "skipping reconstruction"
        t = data.root.coincidences.rec_offsets.col('zenith')
        t = t.compress(~np.isnan(t))
        p = data.root.coincidences.rec_offsets.col('azimuth')
        p = p.compress(~np.isnan(p))
    except:
        rec = MonkeyPatchedRecESD(data, destination='rec_offsets', overwrite=True)
        t, p = rec.reconstruct()
        t = np.array(t)
        t = t.compress(~np.isnan(t))
        p = np.array(p)
        p = p.compress(~np.isnan(p))

    plt.figure()
    ax = plt.subplot(221)
    ax.set_title('%d %d %d\ndefault offsets' % STATIONS)
    ax.hist(p_, bins=20, histtype='step')
    ax.set_xlim(-np.pi, np.pi)

    ax = plt.subplot(223, projection='polar')
    polar_hist(p_, ax=ax, N=20)
    ax.set_xlabel('azimuth distribution')
    ax.set_xticklabels(['E','','N','','W','','S',''])

    ax = plt.subplot(222)
    ax.set_title('Coincidences. N=3 2015 jan-dec.\nestimated offsets')
    ax.hist(p, bins=20, histtype='step')
    ax.set_xlim(-np.pi, np.pi)

    ax = plt.subplot(224, projection='polar')
    polar_hist(p, ax=ax, N=20)
    ax.set_xticklabels(['E','','N','','W','','S',''])
    ax.set_xlabel('azimuth distribution')

    plt.savefig('azimuth_%d_%d_%d.png' % 
             
             
             STATIONS, dpi=200)
    plt.show()
