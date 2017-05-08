import csv
import tables
from sapphire import Station
import numpy as np



def distance_coordinates(latitude1, longitude1, latitude2, longitude2):
    """Calculate distance between two coordinates

    :return: distance between points
    """
    R = 6371000  # [m] Radius of earth
    dLat = np.radians(latitude2 - latitude1)
    dLon = np.radians(longitude2 - longitude1)
    a = (np.sin(dLat / 2) ** 2 + np.cos(np.radians(latitude1)) *
         np.cos(np.radians(latitude2)) * np.sin(dLon / 2) ** 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c

    return distance


def get_station_from_group(s):
    """ '/s202' --> int(202) """
    return int(s.split('s')[1])


with open('coincidences0416_10km_min0,0ms_0,2ms.txt') as f:
    csv_reader = csv.reader(f, delimiter=' ')
    next(csv_reader)
    lid_sid = [(int(x[0]), get_station_from_group(x[1]), int(x[3][:-1:]), int(x[4][:-2:]))  for x in csv_reader]

with open('lightning0416_10000.csv') as f:
    csv_reader = csv.reader(f, delimiter='\t')
    lid_lat_lon = []
    for lid, line in enumerate(csv_reader, 1):
        lid_lat_lon.append((lid, float(line[3]), float(line[4]),
                           float(line[5]), list(map(int, line[10].split(',')))))


#data = tables.open_file('lightning0416_10000.h5', 'r')
#station_array = data.root.lightning.stations
distances = []
for lid, sid, ts, ns in lid_sid[365:]:    # vanaf lid == 2993
    lightning_id, lat, lon, err, stations = lid_lat_lon[lid]
    assert sid in stations
    so = Station(sid, force_stale=True)
    loc = so.gps_location(ts)
    lat_station = loc['latitude']
    lon_station = loc['longitude']
    distance = distance_coordinates(lat, lon, lat_station, lon_station)
    print(lid, sid, distance, err)
    distances.append(distance)
