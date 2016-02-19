# adapted from topaz 150805_n_active
# create dict of eventtimes for all stations in hisparc network.
# serialise and save to disk for driehoeken.py

import warnings
import functools
import os
import urllib
import numpy as np

PATH = '../Datastore/publicdb_csv/eventtime/'
BASE = 'http://data.hisparc.nl/show/source/eventtime/%d/'


def get_number_of_hours_with_data(stations, start=None, end=None):
    """
    adapted from topaz 150805_n_active
    returns the number of HOURS all stations have simultaneous data/events

    :param stations: a list of station ids
    :param start, end: start, end timestamp
    :returns: number of hours with simultaneous data
    """
    data = {}
    for sn in stations:
        data[sn] = get_eventtime(sn)

    if start is None:
        first = int(min(values['timestamp'][0] for values in data.values()))
        last = int(max(values['timestamp'][-1] for values in data.values()))
    else:
        # do some sanity checks
        pass

    is_active = np.zeros((last - first) / 3600 + 1)
    all_active = np.ones(len(is_active))

    for sn in data.keys():
        start = (data[sn]['timestamp'][0] - first) / 3600
        end = start + len(data[sn])
        is_active[start:end] = (data[sn]['counts'] > 500) & (data[sn]['counts'] < 5000)
        #pdb.set_trace()
        all_active = np.logical_and(all_active, is_active)

    return np.count_nonzero(all_active)


def memoize(obj):
    """
    memoiser decorator
    https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


@memoize
def get_eventtime(sn):
    """
    download eventtime histogram if not in cache
    returns eventtime histogram for station sn
    """

    path = PATH + '%d.tsv' % sn
    if not os.path.exists(path):
       warnings.warn('%d not on disk. Downloading eventtime (slow)' % sn)
       urllib.urlretrieve(BASE % sn, path)

    return np.genfromtxt(path, delimiter='\t', dtype=np.uint32, names=['timestamp', 'counts'])


if __name__ == "__main__":
    print "testing station uptime from eventtime hist"
    print "PATH = ", PATH
    print get_number_of_hours_with_data([102,104,105])
    print "testing @memoisation cache. First call ", get_eventtime(501)
    print "next 10 calls:"
    for _ in range(10):
        print get_eventtime(501)
