import pandas as pd
import numpy as np
import tables
from fit_ciampa import get_zenith, fit_zenith, plot_zenith, Iyono
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
            # KIES 10k elementen!
            #if n > 10000:
            #    print('HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEELP!!!!')
            #    zenith = np.random.choice(zenith, 10000)
            #    n = len(zenith)
            #    print('new length', n)
            fit = fit_zenith(zenith, nbins=15, fitfunc=Iyono)
            stations = list(literal_eval(row['stations']))
            s1, s2, s3 = stations
            #plot_zenith(zenith, filename='zenitverdeling_%d_%d_%d.png' % (s1,s2,s3))
            C = fit['C']
            rchi2 = fit['Chi2']
            d = row['max distance']
            datadays = row['data days']
            with tables.open_file(filename, 'r') as data:
                n_total = len(data.root.coincidences.coincidences)
                n_1000 = n_total * (1000./datadays)   # scale to 1000 datadays
                print('n_1000 = ', n_1000)
            subcluster = row['subcluster']
            print('results = ', stations, n, d, C, rchi2)
            results.append((stations, subcluster, d, datadays, n, n_1000,
                            C, rchi2))

    resdf = np.array(results, dtype=[('stations', tuple), ('subcluster', (str, 35)),
                                     ('max distance', int),
                                     ('datadays', int),
                                     ('n', int), ('n_1000', int),
                                     ('C', float), ('rchi2', float)])

    resdf = pd.DataFrame(resdf)

    resdf.to_csv('driehoeken-fits.csv')
