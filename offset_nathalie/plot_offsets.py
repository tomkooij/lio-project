import matplotlib.pyplot as plt
from sapphire import Station


def plot_offsets(stations, outputfile=None):
    stations.sort()

    ref = stations.pop(0)

    plt.figure()
    plt.title('GPS timing offsets ref %d' % ref)
    legend = []
    so = Station(ref, force_stale=True)
    for station in stations:
        o = so.station_timing_offsets(station)
        plt.plot(o['timestamp'], o['offset'])
        legend.append('s%d' % station)
    plt.legend(legend)
    if outputfile:
        plt.savefig('naam.png', dpi=200)
    else:
        plt.show()
    plt.close()


plot_offsets([501, 502, 508])
SPA = [501, 502, 503, 504, 505, 506, 508, 509, 510, 511]
plot_offsets(SPA)
