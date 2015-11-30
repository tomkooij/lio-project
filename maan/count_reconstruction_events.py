# coding: utf-8
#
# Lees ESD data en maak richting reconstructie
#
from __future__ import division
import tables
import sapphire
import math

s501 = sapphire.HiSPARCStations([501]).get_station(501)
rec = sapphire.analysis.direction_reconstruction.EventDirectionReconstruction(s501)

FILENAME  = 'station_501_april2010.h5'
data = tables.open_file(FILENAME, 'r')

query = '(n2 > 2.0) & (n3 > 2.0) & (n4 > 2.0)'


e = data.root.s501.events.read_where(query)
n1 = data.root.s501.events.col('n1')

teller = 0

for event in e:
    r = rec.reconstruct_event(event)
    if not math.isnan(r[0]):
        teller += 1
        if teller % 1000 == 0:
            print teller

print "aantal gereconstrueerde events:", teller,
print teller/n1.size
