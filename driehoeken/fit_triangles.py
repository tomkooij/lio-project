import pandas as pd
import numpy as np
import tables
from fit_ciampa import get_zenith, fit_zenith
from sapphire import download_coincidences
from datetime import datetime
from ast import literal_eval


# lio project datatore
DATASTORE = 'D:/Datastore/driehoeken/'


if __name__ == '__main__':
    df = pd.read_csv('driehoeken.csv')

    results = []
    for index, row in df.iterrows():
        stations = list(literal_eval(row['stations']))
        print(stations)
        s1, s2, s3 = stations
        filename = DATASTORE+'%d_%d_%d_all.h5' % (s1, s2, s3)
        print(filename)

        zenith = get_zenith(filename, stations)
        if zenith is not None:
            print(len(zenith))
            n = len(zenith)
            fit = fit_zenith(zenith, nbins=15)
            C = fit['C']
            rchi2 = fit['Chi2']
            stations = list(literal_eval(row['stations']))
            d = row['max distance']
            print('results = ', stations, n, d, C, rchi2)
            results.append((stations, n, d, C, rchi2))

    resdf = np.array(results, dtype=[('stations', tuple), ('n', int), ('max distance', int), ('C', float), ('rchi2', float)])

    resdf = pd.DataFrame(resdf)

    resdf.to_csv('driehoeken-fits.csv')
