from __future__ import division

import glob

import tables

from sapphire import ReconstructESDEvents, ReconstructESDCoincidences
from sapphire.utils import pbar

#PATHS = '/Users/arne/Datastore/cluster_efficiency/151013*.h5'
PATHS = '/data/hisparc/tom/grid/*.h5'


def reconstruct_simulations(path):
    with tables.open_file(path, 'a') as data:
        cluster = data.root.coincidences._v_attrs.cluster

        try:
            _ = data.getNode('/coincidences/reconstructions')
            print 'Reconstructions exist. Skipping'
            return False

        except tables.NoSuchNodeError: 
            print "Reconstructiong coincidences:"
            # Reconstruct coincidences
            rec_coins = ReconstructESDCoincidences(data, '/coincidences',
                                               overwrite=True, progress=False)
            rec_coins.prepare_output()
            rec_coins.offsets = {station.number: [d.offset + station.gps_offset
                                              for d in station.detectors]
                             for station in cluster.stations}
            rec_coins.reconstruct_directions()
            rec_coins.reconstruct_cores()
            rec_coins.store_reconstructions()


if __name__ == "__main__":
    for path in pbar(glob.glob(PATHS)):
        print 'Now processing: ', path
        reconstruct_simulations(path)
