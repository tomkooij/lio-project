# coding: utf-8
#
# Lees ESD data en maak richting reconstructie
#
from __future__ import division
import tables
import sapphire
import math
import matplotlib.pyplot as plt

s501 = sapphire.HiSPARCStations([501]).get_station(501)
rec = sapphire.analysis.direction_reconstruction.EventDirectionReconstruction(s501)

FILENAME  = 'station_501_april2010.h5'
data = tables.open_file(FILENAME, 'r')

query = '(n2 > 2.0) & (n3 > 2.0) & (n4 > 2.0)'

e = data.root.s501.events.read_where(query)
n1 = data.root.s501.events.col('n1')

angles = []

for event in e:
    zenith, azimuth, detectors = rec.reconstruct_event(event)
    if not math.isnan(zenith):
        angles.append((zenith,azimuth, len(detectors)))
        if len(angles) % 1000 == 0:
            print len(angles)

print "aantal gereconstrueerde events:", len(angles),
print len(angles)/n1.size

a = np.asarray(angles)
zenith = a[:,0]
azimuth = a[:,1]

plt.figure()
plt.hist(zenith, bins=20)
#plt.hist(azimuth, bins=20)
plt.show()
