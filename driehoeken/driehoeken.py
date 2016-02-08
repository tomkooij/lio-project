import json
import numpy as np
from station_maps import plot_station_map_OSM
from itertools import combinations
from math import radians, degrees, sqrt, sin, cos, acos, atan2, pi
from sapphire import Network
from os import path


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


def check_triangle((lat1,lon1),(lat2,lon2),(lat3,lon3), max_distance=1000, max_ratio=4., min_angle=pi/6):

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

    legs = sorted([leg1, leg2, leg3], reverse=True)
    return (legs[0], legs[1]/legs[0], legs[2]/legs[0])


if __name__ == '__main__':
    with open('locations.json') as f:
        station_locations = json.load(f)

    latlon = {}  # dict for fast lookups
    for s in station_locations:
        latlon[int(s['number'])] = (float(s['latitude']), float(s['longitude']))

    clusters = Network().clusters()

    for cluster in clusters:
        print "Cluster %s." % cluster['name']
        stations = Network().station_numbers(cluster=int(cluster['number']))

        if 501 in stations:
            print "removing SPA"
            stations = [x for x in stations if x not in range(501,512)]
        print "%d stations in cluster." % len(stations)
        for s1,s2,s3 in combinations(stations, 3):
            d, r2, r3 = check_triangle(latlon[s1], latlon[s2], latlon[s3], max_ratio=5., min_angle=pi/4)
            if d is not None:
                print "FOUND: %d %d %d. max_d = %4.f m. r2/r1 = %.2f r3/r1 = %.2f" % (s1,s2,s3, d, r2, r3)
                filename = 'driehoek_%s_%s_%s.png'% (s1,s2,s3)
                if not path.exists(filename):
                    plot_station_map_OSM([s1,s2,s3], filename=filename)
