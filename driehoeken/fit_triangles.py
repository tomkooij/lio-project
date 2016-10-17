import pandas as pd
import tables
from fit_ciampa import get_zenith, fit_zenith
from sapphire import download_coincidences
from datetime import datetime
from ast import literal_eval


# lio project datatore
DATASTORE = '/data/hisparc/tom/Datastore/driehoeken/'

if __name__ == '__main__':
    df = pd.read_csv('driehoeken.csv')

    all_triangles = []
    for s in df['stations']:
        sns = list(literal_eval(s))
        d = int(df.loc[df['stations']==s]['max distance'])
        all_triangles.append((sns, d))
    print(all_triangles)

    results = {}

    for stations, d in all_triangles:
        print(stations)

        s1, s2, s3 = stations
        filename = DATASTORE+'%d_%d_%d_all.h5' % (s1, s2, s3)
        print(filename)

        zenith = get_zenith(filename, stations)
        if zenith is not None:
            results[tuple(stations)] = (d, len(zenith), fit_zenith(zenith, nbins=15))

    print(results)

    d, n, C = [], [], []

    for r in results.values():
        d.append(r[0])
        n.append(r[1])
        C.append(r[2]['C'])

    import matplotlib.pyplot as plt

    plt.figure()
    plt.scatter(d, n)
    plt.title('Aantal gereconstrueerde coincidenties vs afstand tussen meetstations')
    plt.show()
