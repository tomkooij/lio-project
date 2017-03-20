from datetime import datetime
import os

import tables
import numpy as np
import matplotlib.pyplot as plt

import sapphire
from sapphire import (download_coincidences,
                      ReconstructESDCoincidences)

from AltitudeCorrectedStation import AltitudeCorrectedStation

STATIONS = (501, 502, 511)
FILENAME = 's%d_%d_%d.h5' % STATIONS

start = datetime(2016, 1, 1)
end = datetime(2016, 5, 1)


def download():
    if not os.path.exists(FILENAME):
        with tables.open_file(FILENAME, 'w') as data:
            print('downloading: ', FILENAME)
            download_coincidences(data, stations=STATIONS, start=start,
                                  end=end, n=3)


def reconstruct_and_plot(scale=1.0):
    with tables.open_file(FILENAME, 'r') as data:
        rec = ReconstructESDCoincidences(data, progress=True, force_stale=True)
        rec.reconstruct_directions()

        print('n = ', len(rec.phi))
        x = np.array(rec.phi)
        x = x.compress(~np.isnan(x))
        x = x * scale
        plt.hist(x, bins=25, histtype='step')


plot = plt.figure()
download()
reconstruct_and_plot()
print('Patching api.Station:')
sapphire.api.Station = AltitudeCorrectedStation
reconstruct_and_plot(0.5)
plt.legend(['default offsets', 'adjusted offsets'])
plt.savefig('s%d_%d_%d.png' % STATIONS, dpi=200)
plt.show()
