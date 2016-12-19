from datetime import datetime
from ast import literal_eval
from math import pi

import pandas as pd
import numpy as np
import tables

import matplotlib.pyplot as plt
from sapphire import Station, HiSPARCStations

import smopy


# lio project datatore
DATASTORE = 'D:/Datastore/driehoeken/'

def get_latlontext(cluster):
    """Create list of latitude, longitudes, and legend text for a cluster

    Make a list of locations for each of station and its detectors, for the
    stations the number is included.

    :param cluster: HiSPARCStations object.

    """
    latlon = []
    for station in cluster.stations:
        latitude, longitude, _ = station.get_lla_coordinates()
        latlon.append((latitude, longitude, station.number))
        for detector in station.detectors:
            latitude, longitude, _ = detector.get_lla_coordinates()
            latlon.append((latitude, longitude, None))
    return latlon


def plot_cluster_OSM(stations, plot_detectors=False, force_stale=True, axis=None):
    """Plot cluster (station and detectors) on top of OSM tiles

    :param cluster: (list of) station number(s).
    :param plot_detectors: plot detectors if True.
    :param force_stale: if True do not get lla info from api, but use local data.

    """
    if isinstance(stations, int):
        stations = [stations]

    cluster = HiSPARCStations(stations, force_stale=force_stale)

    latlon = get_latlontext(cluster)
    lat = [ll[0] for ll in latlon]
    lon = [ll[1] for ll in latlon]

    map = smopy.Map((min(lat), min(lon)), (max(lat), max(lon)), margin=0.01)
    ax = map.show_mpl(ax=axis)
    for px, py, label in latlon:
        x, y = map.to_pixels(px, py)
        if label is not None:
            ax.plot(x, y, 'or', ms=10, mew=2)
            ax.text(x, y, '  '  + str(label))
        elif plot_detectors:  # detector
            ax.plot(x, y, 'xb', ms=10)


def plot_azimuth(azimuth, stations, d, outputfile=None):

    s1, s2, s3 = stations

    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax0, ax1 = axes.flat
    ax0.set_title('%d %d %d azimuth distribution' % (s1, s2, s3))

    ax0.hist(azimuth, bins=40, histtype='step')
    ax0.set_xlabel('azimuth (rad) from east over north')
    ax0.set_ylabel('counts')
    ax0.set_xlim(-pi,pi)

    plot_cluster_OSM(stations, axis=ax1)
    ax1.set_title('max distance = %d m' % d)
    ax1.set_axis_off()

    if outputfile:
        plt.savefig(outputfile, dpi=200)
    else:
        plt.show()


    plt.close()


def get_reconstructions(filename):
    """ open hdf5 filename. Read directions. Return zenith, azimuth"""

    with tables.open_file(filename, 'r') as data:
        try:
            n = len(data.root.coincidences.coincidences)
            if n == 0:
                return None
        except:
            return None


        #if not CountReconstructedDirections(data):
        #    rec = DirectionsOnly(data, overwrite=True)
        #    rec.reconstruct_and_store(stations)

        zenith = data.root.coincidences.reconstructions.col('zenith')
        azimuth =  data.root.coincidences.reconstructions.col('azimuth')
        azimuth = azimuth[~np.isnan(zenith)]
        zenith = zenith[~np.isnan(zenith)]
    return zenith, azimuth


if __name__ == '__main__':
    df = pd.read_csv('driehoeken.csv')

    results = []
    for index, row in df.iterrows():
        stations = list(literal_eval(row['stations']))
        d = row['max distance']
        s1, s2, s3 = stations
        print(stations, d)

        filename = DATASTORE+'%d_%d_%d_all.h5' % (s1, s2, s3)
        print(filename)

        zenazi = get_reconstructions(filename)

        if zenazi is not None:
            zenith, azimuth = zenazi
            print(len(zenith))
            if len(zenith) > 1000:
                plot_azimuth(azimuth, stations, d, outputfile='azimuth_%s' % stations)
