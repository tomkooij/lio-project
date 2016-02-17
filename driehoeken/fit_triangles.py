import pandas as pd
import tables
from fit_ciampa import get_zenith, fit_zenith
from sapphire import download_coincidences
from datetime import datetime
from ast import literal_eval


#DATASTORE = 'd:/Datastore/driehoeken/'
DATASTORE = '/data/hisparc/tom/driehoeken/'


def get_data(filename, stations, start, end):
    """ open filename and download coincidences if /coincidences group does not exists """
    with tables.open_file(filename, 'a') as data:
        if '/coincidences' not in data:
            download_coincidences(data, stations=stations, start=start, end=end, n=3)
        else:
            print '/coincidences exists in %s.' % filename


if __name__ == '__main__':
    df = pd.read_csv('driehoeken.csv')
    
    all_triangles = []    
    for s in df['stations']:
        all_triangles.append(list(literal_eval(s)))
    #print all_triangles
    #assert False

    start = datetime(2015,1,1)
    end = datetime(2015,12,31)

    results = {}

    for stations in all_triangles:
        print stations

        s1, s2, s3 = stations
        filename = DATASTORE+'2015full_%d_%d_%d.h5' % (s1, s2, s3)
        print filename

        if 1: # check file exist, events exist... bla
            get_data(filename, stations, start, end)

        zenith = get_zenith(filename, stations)
        if zenith is not None:
            results[tuple(stations)] = (len(zenith), fit_zenith(zenith, nbins=15))

    print results
