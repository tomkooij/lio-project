# Bosboom, figure 3.16, blz 40.
# editted interactive %save

FILENAME = 'test_501_502_505.h5'
STATIONS = [501, 502, 505]

import tables
data = tables.open_file(FILENAME, 'a')

from sapphire import download_coincidences
from datetime import datetime
start = datetime(2015,1,1)
end = datetime(2015,12,31)
download_coincidences(data, stations=STATIONS, start=start, end=end, n=3)

from sapphire import ReconstructESDCoincidences
rec = ReconstructESDCoincidences(data, overwrite=True)
rec.reconstruct_and_store()

from cluster_uptime import get_number_of_hours_with_data
hours = get_number_of_hours_with_data(STATIONS, start=start, end=end)
print "hours = ", hours
print "%f % uptime", hours/365./24*100.

# interactive %pylab
from pylab import *
from numpy import * 

p = data.root.coincidences.reconstructions.col('azimuth')
p = p.compress(~isnan(p))

ion()
hist(p, bins=20, histtype='step')
title('%d azimuth angle' % STATIONS)
xlabel('azimuth (rad) from east over north')
ylabel('counts')
from math import pi
xlim(-pi,pi)
savefig('bosboom_fig3.16.png', dpi=200)
