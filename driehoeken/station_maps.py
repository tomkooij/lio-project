from sapphire import Network, Station
from sapphire.utils import pbar
import json
import matplotlib.pyplot as plt
import smopy
from mpl_toolkits.basemap import Basemap

def get_station_locations(stations):
    """ get station locations from API add station id """
    station_locations = []

    for station in pbar(stations):
        try:
            loc = Station(station).location()

        except:
            print 'API call for station %d failed. Setting to (0,0).' % station
            loc['latitude'] = 0.0
            loc['longitude'] = 0.0

        loc['number'] = station
        station_locations.append(loc)

    return station_locations

def plot_map_basemap(x,y):
    """
    plot stations with country borders
    only useful for full network
    """
    x_min = min(x) - .1
    y_min = min(y) - .1
    x_max = max(x) + .1
    y_max = max(y) + .1
    x_avg = (x_max+x_min)/2.
    y_avg = (y_max+y_min)/2.

    print y_min, x_min, y_max, x_max

    map = Basemap(llcrnrlon=x_min,llcrnrlat=y_min,urcrnrlon=x_max,urcrnrlat=y_max,
             resolution='i', projection='tmerc', lat_0=y_avg, lon_0=x_avg)

    #map.drawmapboundary(fill_color='aqua')
    #map.fillcontinents(color='coral',lake_color='aqua')
    map.drawcoastlines()
    #map.etopo()
    xx,yy = map(x,y)
    map.scatter(xx,yy)
    plt.show()

def plot_map_OSM(x,y,numbers):
    """
    plot stations on top of OSM tiles
    """

    assert smopy.__version__ == '0.0.3-arne', 'Wrong smopy!'  # this REALLY needs fixing

    map = smopy.Map((min(y), min(x)), (max(y),max(x)), margin=.1)
    ax = map.show_mpl(figsize=(8, 6))
    for px,py,station in zip(x,y,numbers):
        y, x = map.to_pixels(py, px)
        ax.plot(y, x, 'or', ms=10, mew=2)
        ax.text(y, x, str(station))
    #plt.savefig('science_park.png', dpi=200)
    plt.show()

def plot_map(x,y):
    plt.figure()
    plt.plot(x,y,'ro')
    plt.ylim(min(y)-.1,max(y)+.1)
    plt.xlim(min(x)-.1,max(x)+.1)
    plt.show()

if __name__ == '__main__':
    stations = Network().station_numbers()
    #station_locations = get_station_locations(stations)
    #with open('locations.json','w') as f:
    #    json.dump(station_locations, f)

    with open('locations.json') as f:
        station_locations = json.load(f)


    cluster = Network().station_numbers(subcluster=500)
    #cluster = [102,104,105]
    #cluster = [101,102,103,104,105]
    y = [station['latitude'] for station in station_locations if station['number'] in cluster]
    x = [station['longitude'] for station in station_locations if station['number'] in cluster]

    plot_map_OSM(x,y,cluster)
