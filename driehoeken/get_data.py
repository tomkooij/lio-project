#  adapted from topaz 150805_n_active
# create dict of eventtimes for all stations in hisparc network.
# serialise and save to disk for driehoeken.py

from glob import glob
import os
import cPickle as pickle

from numpy import genfromtxt, zeros, histogram, arange
PATH = '../Datastore/publicdb_csv/eventtime/*.tsv'


def read_eventtime(path):
    return genfromtxt(path, delimiter='\t', dtype=None, names=['timestamp', 'counts'])


def get_data():
    return {int(os.path.basename(path)[:-4]): read_eventtime(path)
            for path in glob(PATH)}


if __name__ == "__main__":
    data = get_data()
    with open('stations_with_events','wb') as f:
        pickle.dump(data, f, protocol=2)
