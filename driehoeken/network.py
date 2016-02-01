from sapphire import Network, Station
from sapphire.utils import pbar
import json
import matplotlib.pyplot as plt

def get_station_locations(stations):
    """ get station locations from API add station id """
    station_locations = []

    for station in pbar(stations):
        try:
            loc = Station(station,allow_stale=False).location()
            loc['number'] = station
            station_locations.append(loc)
        except:
            print 'API call for station %d failed. Skipping.' % station

    return station_locations

def plot_map(x,y):
    plt.figure()
    plt.plot(x,y,'ro')
    plt.ylim(min(y)-1,max(y)+1)
    plt.xlim(min(x)-1,max(x)+1)
    plt.show()

if __name__ == '__main__':
    stations = Network().station_numbers()
    #station_locations = get_station_locations(stations)
    #with open('locations.json','w') as f:
    #    json.dump(station_locations, f)

    with open('locations.json') as f:
        station_locations = json.load(f)

    y = [station['latitude'] for station in station_locations]
    x = [station['longitude'] for station in station_locations]

    plot_map()
