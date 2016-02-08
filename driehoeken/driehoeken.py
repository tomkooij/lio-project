import json
import numpy as np
from station_maps import plot_station_map_OSM, get_station_locations
from itertools import combinations
from math import radians, degrees, sqrt, sin, cos, acos, atan2, pi
from sapphire import Network
from os import path
import cPickle as pickle
import pandas as pd


def geocalc((lat1, lon1), (lat2, lon2)):
    """
    http://stackoverflow.com/questions/8858838/need-help-calculating-geographical-distance
    :return: great circle distance in meters
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon1 - lon2

    EARTH_R = 6.3728e6

    y = sqrt(
        (cos(lat2) * sin(dlon)) ** 2
        + (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)) ** 2
        )
    x = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)
    c = atan2(y, x)
    return EARTH_R * c


def sss(a,b,c):
    """ compute angles A,B,C of triangle with legs a,b,c """
    A = acos((b**2 + c**2 - a**2) / (2 * b * c))
    B = acos((a**2 + c**2 - b**2) / (2 * a * c))
    C = pi - A - B
    return (A, B, C)


def check_triangle((lat1,lon1),(lat2,lon2),(lat3,lon3), max_distance=1500, max_ratio=10., min_angle=pi/10):

    leg1 = geocalc((lat1,lon1),(lat2,lon2))
    if leg1 > max_distance:
        return (None, None, None)
    leg2 = geocalc((lat1,lon1),(lat3,lon3))
    if leg2 > max_distance:
        return (None, None, None)
    leg3 = geocalc((lat2,lon2),(lat3,lon3))
    if leg3 > max_distance:
        return (None, None, None)

    #print "d legs: ",leg1, leg2, leg3
    p = leg1/leg2
    q = leg1/leg3
    r = leg2/leg3

    for x in [p,q,r]:
        if x > max_ratio or x < 1./max_ratio:
            return (None, None, None)

    # check shape
    angle, _, _ = sorted(sss(leg1, leg2, leg3))
    #print map(degrees, sss(leg1,leg2,leg3))
    if angle < min_angle:
        return (None, None, None)

    leg1, leg2, leg3 = sorted([leg1, leg2, leg3], reverse=True)
    return (leg1, leg3/leg1, angle)


def check(s1,s2,s3):
    """
    check a tuple of stations (for interactive use)
    >>> check(501, 506, 509)
    """

    stations = [s1, s2, s3]

    for s in get_station_locations(stations):
        latlon[int(s['number'])] = (float(s['latitude']), float(s['longitude']))
    print "debug:", latlon[s1]
    return check_triangle(latlon[s1], latlon[s2], latlon[s3])


def get_number_of_hours_with_data(stations, stations_with_events):
    """
    adapted from topaz 150805_n_active
    returns the number of HOURS all stations have simultaneous data/events

    :param stations: a list of station ids
    :param stations_with_events: a dict of tuples (see: get_data.py)
    """
    data = { key: stations_with_events[key] for key in stations}

    first = min(values['timestamp'][0] for values in data.values())
    last = max(values['timestamp'][-1] for values in data.values())

    is_active = np.zeros((len(data.keys()), (last - first) / 3600 + 1))
    all_active = np.array(len(is_active[0]) * [True])

    for i, sn in enumerate(data.keys()):
        start = (data[sn]['timestamp'][0] - first) / 3600
        end = start + len(data[sn])
        is_active[i, start:end] = (data[sn]['counts'] > 500) & (data[sn]['counts'] < 5000)
        all_active = all_active & (is_active[i]==1.)

    return sum(all_active)


if __name__ == '__main__':
    with open('locations.json') as f:
        station_locations = json.load(f)
    latlon = {}  # dict for fast lookups
    for s in station_locations:
        latlon[int(s['number'])] = (float(s['latitude']), float(s['longitude']))

    with open('stations_with_events', 'rb') as f:
        stations_with_events = pickle.load(f)

    clusters = Network().clusters()

    driehoeken = []
    for cluster in clusters:
        print "Cluster %s." % cluster['name']
        stations = Network().station_numbers(cluster=int(cluster['number']))

        if 501 in stations:
            print "removing SPA"
            stations = [x for x in stations if x not in range(501,512)]
        if 501 in stations:
            print "removing 507 and 510 from SPA",
            stations = [x for x in stations if x not in [507,510]]#range(501,512)]
            print stations

        print "%d stations in cluster." % len(stations)

        for s1,s2,s3 in combinations(stations, 3):
            d, r, a = check_triangle(latlon[s1], latlon[s2], latlon[s3])

            if d is not None:
                print "FOUND: %d %d %d. d = %4.1f max ratio = %.2f min angle = %.2f" % (s1, s2, s3, d, r, degrees(a))
                days = get_number_of_hours_with_data([s1,s2,s3], stations_with_events) / 24.
                driehoeken.append((int(d), int(degrees(a)), int(days),(s1,s2,s3)))

                filename = 'driehoek_%s_%s_%s_d_%4.f_a_%2.f.png'% (s1,s2,s3, d, degrees(a))
                #if not path.exists(filename):
                #    plot_station_map_OSM([s1,s2,s3], filename=filename)

    driehoeken.sort()
    df = pd.DataFrame(driehoeken, columns=['max distance', 'min angle', 'data days', 'stations'])
    print df
