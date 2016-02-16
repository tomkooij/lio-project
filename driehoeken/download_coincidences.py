import json
import tables
from fit_ciampa import get_zenith, fit_zenith
from sapphire import download_coincidences
from datetime import datetime

DATASTORE = 'd:/Datastore/driehoeken/'
#DATASTORE = '/data/hisparc/tom/driehoeken/'

if __name__ == '__main__':
    with open('driehoeken.json') as f:
        d = json.load(f)

        start = datetime(2015,1,1)
        end = datetime(2015,12,31)

        for stations in d['stations'].values():
            print stations
            s1, s2, s3 = stations
            filename = DATASTORE+'2015full_%d_%d_%d.h5' % (s1, s2, s3)
            with tables.open_file(filename, 'a') as data:
                download_coincidences(data, stations=stations, start=start, end=end, n=3)
