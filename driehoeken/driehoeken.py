import json
from station_maps import plot_map_OSM
from itertools import combinations
from sapphire.utils import pbar
from math import radians, sqrt, sin, cos, atan2
from sapphire import Network

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

def check_triangle((lat1,lon1),(lat2,lon2),(lat3,lon3), max_distance=1000):

    leg1 = geocalc((lat1,lon1),(lat2,lon2))
    if leg1 > max_distance:
        return (None, None, None)
    leg2 = geocalc((lat1,lon1),(lat3,lon3))
    if leg2 > max_distance:
        return (None, None, None)
    leg3 = geocalc((lat2,lon2),(lat3,lon3))
    if leg3 > max_distance:
        return (None, None, None)

    p = leg1/leg2
    q = leg1/leg3
    r = leg2/leg3

    #print "legs: ", leg1, leg2, leg3
    #print "pqr:", p, q, r

    for x in [p,q,r]:
        if x > 1.25 or x < 0.8:
            return (None, None, None)

    return (leg1, leg2, leg3)

if __name__ == '__main__':
    with open('locations.json') as f:
        station_locations = json.load(f)

    latlon = {}  # dict for fast lookups
    for s in station_locations:
        latlon[int(s['number'])] = (float(s['latitude']), float(s['longitude']))

    cluster = Network().station_numbers(cluster=3000) #subcluster=500)

    for s1,s2,s3 in pbar(combinations(cluster, 3)):
        leg1, leg2, leg3 = check_triangle(latlon[s1], latlon[s2], latlon[s3])
        if leg1 is not None:
            print "FOUND!", s1,s2,s3, leg1, leg2, leg3
            #plot_map_OSM([s1,s2,s3])
