"""
Modified from AdL:
topaz/150930_coincidences_distance/download_pair_data.py"

download coincidences from triangles
"""
from __future__ import division, print_function

import os
import multiprocessing
import datetime
import random

import tables
import pandas as pd

from sapphire import download_coincidences

DATAPATH = '/data/hisparc/tom/Datastore/driehoeken/%d_%d_%d_all.h5'

def download_coincidences_multi(triangles):
    """Like download_coincidences_triangles, but multithreaded"""

    worker_pool = multiprocessing.Pool(4)
    worker_pool.map(download_coincidences_triangle, triangles)
    worker_pool.close()
    worker_pool.join()


def download_coincidences_triangles(triangles):
    """Download coincidences for the given sn"""

    for triangle in triangles:
        download_coincidences_triangle(triangle)


def download_coincidences_triangle(triangle):
    path = DATAPATH % tuple(triangle)
    tmp_path = path + '_tmp'
    if os.path.exists(path):
        print('Skipping', triangle)
        return
    start_dt = datetime.datetime.now()
    print('Starting', triangle, start_dt)
    with tables.open_file(tmp_path, 'w') as data:
        for year in list(range(2008, 2017)):
            for month in list(range(1, 13)):
                start = datetime.datetime(year, month, 1)
                if month < 12:
                    end = datetime.datetime(year, month+1, 1)
                else:
                    end = datetime.datetime(year+1, 1, 1)
                print(start, end)
                try:
                    download_coincidences(data, stations=list(triangle),
                                          start=start, end=end,
                                          progress=True, n=3)
                except Exception:  # retry at timeout, second time is faster due to cache
                    print('retry!', datetime.datetime.now())
                    download_coincidences(data, stations=list(triangle),
                                          start=start, end=end,
                                          progress=True, n=3)
    os.rename(tmp_path, path)
    print('Finished', triangle, datetime.datetime.now()-start_dt)


if __name__ == "__main__":
    df = pd.read_json('driehoeken.json')
    todo = list(df['stations'])
    print(todo)
    for _ in range(20):
        print('iteration: ', _)
        random.shuffle(todo)
        try:
            download_coincidences_triangles(todo)
        except:
            print('Catch exception..!')
