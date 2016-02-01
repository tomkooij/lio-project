from sapphire import Network, Station
from sapphire.utils import pbar
import json

def get_all_station_numbers():
    network = Network()
    all_stations = Network().stations()

    stations = [station['number'] for station in all_stations]
    return stations

def get_station_locations(stations):
    """ get station locations from API add station id """
    station_locations = []

    for station in pbar(stations):
        try:
            loc = Station(station,allow_stale=False).location()
        except:
            loc = {}
        loc['number'] = station
        station_locations.append(loc)
    return station_locations

if __name__ == '__main__':
    stations = get_all_station_numbers()
    station_locations = get_station_locations(stations)
    with open('locations.json','w') as f:
        json.dump(station_locations, f)
