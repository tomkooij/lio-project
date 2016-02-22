import tables
import numpy as np
from fit_ciampa import get_zenith, fit_zenith
from cluster_uptime import get_number_of_hours_with_data
from sapphire import download_coincidences
from datetime import datetime
import matplotlib.pyplot as plt

#DATASTORE = 'd:/Datastore/driehoeken/'
DATASTORE = '/data/hisparc/tom/driehoeken/'


def get_data(filename, stations, start, end):
    """ open filename and download coincidences if /coincidences group does not exists """
    
    with tables.open_file(filename, 'a') as data:
        if '/coincidences' not in data:
            download_coincidences(data, stations=stations, start=start, end=end, n=3)
        else:
            print '/coincidences exists in %s.' % filename

        n = len(data.root.coincidences.coincidences)
    return n


if __name__ == '__main__':
    data = np.load('driehoeken.npy')
    
    start = datetime(2015,1,1)
    end = datetime(2015,12,31)

    results = {}

    for row in data:
        stations = row['stations']
        maxdist = row['max distance']

        s1, s2, s3 = stations
        filename = DATASTORE+'2015full_%d_%d_%d.h5' % (s1, s2, s3)
        print filename

        if 1: # check file exist, events exist... bla
            n = get_data(filename, stations, start, end)

        zenith = get_zenith(filename, stations)
        if zenith is not None:
            results[tuple(stations)] = (maxdist, n, len(zenith), fit_zenith(zenith, nbins=15))
            # store everything in np.recarray

    # stupid hack to create some figs for midterm. Refactor!
    n_list = []
    d_list = []  
    d2_list = []
    C_list = []
    chi2_list = []

    for key in results.keys():

        d, n, n_zenith, fit = results[key]
        C, chi2 = fit
        if n < 1000: 
            continue

        hours_data = get_number_of_hours_with_data(key)

        n_year = (365.25*24)/hours_data * n

        print key, n, n_year, d
        n_list.append(n)
        d_list.append(d)
        d2_list.append(d**2)
        C_list.append(C)
        chi2_list.append(chi2)

    if 1:
        plt.figure()
        plt.scatter(d2_list, n_list)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('kwadraat lange zijde [m^2]')
        plt.ylabel('counts [per jaar]')
        plt.title('Aantal coincidenties vs driehoek oppervlak')
        plt.savefig('coinc_vs_opp.png', dpi=200)
        plt.show()
    if 1:
        plt.figure()
        plt.scatter(d2_list, C_list)
        plt.xscale('log')
        plt.xlabel('kwadraat lange zijde [m^2]')
        plt.ylabel('C')
        plt.title('Absorptie coefficient C vs driehoek oppervlak')
        plt.savefig('c_vs_opp.png', dpi=200)
        plt.show()
