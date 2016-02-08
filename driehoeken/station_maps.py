from sapphire import Network, Station
import matplotlib.pyplot as plt
import smopy


def get_station_locations(stations):
    """ get station locations from API add station id """
    return [get_station_location(station) for station in stations]


def get_station_location(station):
    """ get station location from API add station id """
    try:
        loc = Station(station).location()
    except:
        print 'API call for station %d failed. Setting to (0,0).' % station
        loc['latitude'] = 0.0
        loc['longitude'] = 0.0

    loc['number'] = station
    return loc


def plot_station_map_OSM(stations, filename=None):
    """
    plot a map with OSM tile background
    :param: stations: list of tuples (lat, lon, marker)
    """

    loc = [get_station_location(station) for station in stations]
    lat = [l['latitude'] for l in loc]
    lon = [l['longitude'] for l in loc]
    numbers = [l['number'] for l in loc]
    plot_map_OSM(lat, lon, numbers)
    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()

def plot_map_OSM(lat, lon, numbers):
    """
    plot stations on top of OSM tiles
    """

    # this REALLY needs fixing
    assert smopy.__version__ == '0.0.3-arne', 'Wrong smopy!'

    map = smopy.Map((min(lat), min(lon)), (max(lat), max(lon)), margin=.1)
    ax = map.show_mpl(figsize=(8, 6))
    for px, py, station in zip(lat, lon, numbers):
        x, y = map.to_pixels(px, py)
        ax.plot(x, y, 'or', ms=10, mew=2)
        ax.text(x, y, str(station))


if __name__ == '__main__':
    cluster = Network().station_numbers(subcluster=500)
    plot_station_map_OSM(cluster)
