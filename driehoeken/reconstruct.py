from __future__ import print_function, division

#PATH = '/data/hisparc/tom/Datastore/driehoeken/505_508_511*'
PATH = '/data/hisparc/tom/Datastore/driehoeken/*.h5'

from glob import glob
from datetime import datetime

import tables

from sapphire import ReconstructESDCoincidences

for h5file in glob(PATH):
    print(h5file, datetime.now())
    with tables.open_file(h5file, 'a') as data:
        try:
            n = len(data.root.coincidences.coincidences)
            if n == 0:
                print('%s has no coincidences. Skip' % h5file)
                continue
        except:
            print('Error, skip!')
            continue
        try:
            data.get_node('/coincidences/reconstructions')
            n = len(data.root.coincidences.coincidences)
            print('Number of reconstructions = ', n)
        except tables.NoSuchNodeError:
            print('reconstructing!')
            rec = ReconstructESDCoincidences(data, overwrite=True, progress=True)
            rec.reconstruct_and_store()
