# try station offsets
from __future__ import division

import tables
import os
from sapphire import download_coincidences
from datetime import datetime
from sapphire import ReconstructESDCoincidences
from cluster_uptime import get_number_of_hours_with_data
from math import pi


STATIONS = (501, 502, 505)
# station 501-502 = +8ns
# station 501-505 = +22ns
# manually changing the station offsets in sapphire removes big sinewave
FILENAME = 'test_%d_%d_%d.h5' % STATIONS

start = datetime(2015,1,1)
end = datetime(2015,12,31)

def open():
    if os.path.exists(FILENAME):
        print "%s exist: opening" % FILENAME
        return tables.open_file(FILENAME, 'a')
    else:
        assert False
        data = tables.open_file(FILENAME, 'a')
        download_coincidences(data, stations=STATIONS, start=start, end=end, n=3)
        return data

def make_plot():
    ion()
    hist(p, bins=20, histtype='step')
    title('%s azimuth angle' % str(STATIONS))
    xlabel('azimuth (rad) from east over north')
    ylabel('counts')
    xlim(-pi,pi)
    #savefig('azimuth.png', dpi=200)

if __name__ == '__main__':
    print "stations: ", STATIONS
    print "uptime (days):", get_number_of_hours_with_data(STATIONS, start=start, end=end)/24

    data = open()  # keep open for interactive...

    rec = ReconstructESDCoincidences(data, overwrite=True)
    rec.reconstruct_and_store()

    # interactive %pylab
    from pylab import *
    from numpy import * 
    p = data.root.coincidences.reconstructions.col('azimuth')
    p = p.compress(~isnan(p))
    make_plot()
