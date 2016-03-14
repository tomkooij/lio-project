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

#STATIONS = (501, 504, 505)
#STATIONS = (501, 502, 505)
STATIONS = (501, 502, 508)
# station 501-502 = +8ns
# station 501-505 = +22ns
# manually changing the station offsets in sapphire removes big sinewave
FILENAME = '2014_%d_%d_%d.h5' % STATIONS

start = datetime(2014,1,1)
end = datetime(2014,12,31)

class MonkeyPatchedRecESD(ReconstructESDCoincidences):

    def reconstruct(self, station_numbers=None):
        """Shorthand function to reconstruct coincidences and store results"""

        print "WARNING: MONKEY PATCHED ReconstructESDCoincidences. no cores. return theta, phi"
        self.prepare_output()
        self.get_station_timing_offsets()
        self.reconstruct_directions(station_numbers=station_numbers)
        #self.reconstruct_cores(station_numbers=station_numbers)
        self.store_reconstructions()
        return self.theta, self.phi

class OldOffsets(MonkeyPatchedRecESD):
    def get_station_timing_offsets(self):
        self.offsets = {102: [-3.1832, 0.0000, 0.0000, 0.0000],
                104: [-1.5925, -5.0107, 0.0000, 0.0000],
                105: [-14.1325, -10.9451, 0.0000, 0.0000],
                501: [-1.10338, 0.0000, 5.35711, 3.1686],
                502: [-8.11711, -8.5528, -8.72451, -9.3388],
                503: [-22.9796, -26.6098, -22.7522, -21.8723],
                504: [-15.4349, -15.2281, -15.1860, -16.5545],
                505: [-21.6035, -21.3060, -19.6826, -25.5366],
                506: [-20.2320, -15.8309, -14.1818, -14.1548],
                508: [-26.2402, -24.9859, -24.0131, -23.2882],
                509: [-24.8369, -23.0218, -20.6011, -24.3757]}

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

    try:
        t_ = data.root.coincidences.reconstructions.col('zenith')
        t_ = t_.compress(~np.isnan(t_))
        p_ = data.root.coincidences.reconstructions.col('azimuth')
        p_ = p_.compress(~np.isnan(p_))
    except:
        rec = OldOffsets(data, overwrite=True)
        t_, p_ = rec.reconstruct()
        t_ = np.array(t_)
        t_ = t_.compress(~np.isnan(t_))
        p_ = np.array(p_)
        p_ = p_.compress(~np.isnan(p_))

    try:
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
    ax.set_title('Coincidences. N=3 2014 jan-dec.\nestimated offsets')
    ax.hist(p, bins=20, histtype='step')
    ax.set_xlim(-np.pi, np.pi)

    ax = plt.subplot(224, projection='polar')
    polar_hist(p, ax=ax, N=20)
    ax.set_xticklabels(['E','','N','','W','','S',''])
    ax.set_xlabel('azimuth distribution')

    plt.savefig('azimuth_%d_%d_%d.png' % STATIONS, dpi=200)
    plt.show()
