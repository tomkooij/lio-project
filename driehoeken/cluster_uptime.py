# adapted from topaz 150805_n_active
# create dict of eventtimes for all stations in hisparc network.
# serialise and save to disk for driehoeken.py

import warnings
import functools
import os
import urllib
import numpy as np
import datetime
from sapphire.transformations.clock import datetime_to_gps

BASE = 'http://data.hisparc.nl/show/source/eventtime/%d/' 
PATH = '../Datastore/publicdb/eventtime/'

def process_time(time):
    if type(time)  == int:
        return time
    if type(time) == datetime.datetime:
        return datetime_to_gps(time)
    raise RuntimeError('Unable to parse time: ', time)

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
        data[sn] = get_eventtime(sn, binfiles=True)

    first = min(values['timestamp'][0] for values in data.values())
    last = max(values['timestamp'][-1] for values in data.values())

    len_array = (last - first) / 3600 + 1
    all_active = np.ones(len_array)


    for sn in data.keys():
        is_active = np.zeros(len_array)
        start_i = (data[sn]['timestamp'][0] - first) / 3600
        end_i = start_i + len(data[sn])
        is_active[start_i:end_i] = (data[sn]['counts'] > 500) & (data[sn]['counts'] < 5000)
        #print "debug: ", sn, np.count_nonzero(is_active)
        all_active = np.logical_and(all_active, is_active)

    # filter start, end
    if start is not None:
        start_index = max(0, process_time(start) - first) / 3600
    else:
        start_index = 0

    if end is not None:
        end_index = min(last, process_time(end) - first) / 3600
    else:
        end_index = len(all_active)

    return np.count_nonzero(all_active[start_index:end_index])


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
def get_eventtime(sn, binfiles=False):
    """
    download eventtime histogram if not in cache
    returns eventtime histogram for station sn
    """
    if binfiles:
        path = PATH + '%d.npy' % sn
        if not os.path.exists(path):
            warnings.warn('%d not on disk in numpy bin format. Getting TSV and converting' % sn)
            data = get_eventtime(sn, binfiles=False)
            with open(path, 'wb') as f:
                np.save(f, data)
            return data
        return np.load(path)
    else:
        path = PATH + '%d.tsv' % sn
        if not os.path.exists(path):
           warnings.warn('%d not on disk. Downloading eventtime (slow)' % sn)
           urllib.urlretrieve(BASE % sn, path)

        return np.genfromtxt(path, delimiter='\t', dtype=np.uint32, names=['timestamp', 'counts'])


if __name__ == "__main__":
    print "testing station uptime from eventtime hist"
    print "PATH = ", PATH
    print get_number_of_hours_with_data([102,104,105])/24
    print get_number_of_hours_with_data([504,509, 511])/24
