"""
Determine the GPS clock offset from real data
"""

from datetime import datetime
import os

import tables
import numpy as np
import matplotlib.pyplot as plt

import sapphire
from sapphire import (download_coincidences, ProcessTimeDeltas,
                      DetermineStationTimingOffsets)

from PatchedStation import PatchedStation

STATIONS = (501, 510)
FILENAME = 's%d_%d.h5' % STATIONS

start = datetime(2015, 12, 25)
end = datetime(2016, 1, 5)


def download():
    if not os.path.exists(FILENAME):
        with tables.open_file(FILENAME, 'w') as data:
            print('downloading: ', FILENAME)
            download_coincidences(data, stations=STATIONS, start=start,
                                  end=end, n=len(STATIONS))
            print('determining time deltas : ', FILENAME)
            td = ProcessTimeDeltas(data)
            td.determine_and_store_time_deltas()

def offsets():
    with tables.open_file(FILENAME, 'r') as data:
        off = DetermineStationTimingOffsets(stations=STATIONS, data=data)
        return off.determine_station_timing_offsets(STATIONS[1], STATIONS[0])

download()
sapphire.api.Station = PatchedStation

o = offsets()
print (o)
