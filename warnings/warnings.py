"""
Investigate warnings from direction reconstruction
"""
from __future__ import (division, print_function)

import pdb, traceback, sys
import tables
import numpy
from datetime import datetime

from sapphire import download_coincidences
from sapphire.analysis.reconstructions import ReconstructESDCoincidences

FILENAME = 'coinc.h5'
START = datetime(2015, 12, 1)
END = datetime(2016, 1, 1)
STATIONS = [501, 502, 508]


def get_coincidences(filename, stations, start, end):
    """ make sure a 'filename' with coincidences exists (or download)"""

    with tables.open_file(filename, 'a') as data:
        if '/coincidences' not in data:
            print('downloading coincidences...')
            download_coincidences(data, stations=stations, start=start, end=end)
        else:
            print('%d coincidences in datafile' %
                  (len(data.root.coincidences.coincidences)))

def reconstruct(filename):
    with tables.open_file(filename, 'a') as data:
        rec = ReconstructESDCoincidences(data, overwrite=True, force_stale=True)
        print('reconstructing...')
        with numpy.errstate(invalid='raise'):`
            try:
                rec.reconstruct_and_store()
            except:
                _, _, tb = sys.exc_info()
                traceback.print_exc()
                pdb.post_mortem(tb)

if __name__ == '__main__':
    #get_coincidences(FILENAME, STATIONS, START, END)
    reconstruct(FILENAME)

