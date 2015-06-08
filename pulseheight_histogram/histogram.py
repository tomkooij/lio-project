import sapphire
import datetime
import tables
import os

import matplotlib.pyplot as plt

import numpy as np

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2010, 4, 1)
END = datetime.datetime(2010, 4, 2)
FILENAME = 'station_501_1dag.h5'


#
# Read event data from the ESD
#  store in table `/sSTATION' for example: /s501
#
def create_new_event_file(filename, stations, start, end):

    print  "creating file: ", filename
    data = tables.open_file(filename, 'w')

    print "reading from the ESD"
    for station in stations:
        print "Now reading station %d" % station
        sapphire.esd.download_data(data, '/s%d' % station, station, START, END)

    return data


if __name__ == '__main__':
    if 'data' not in globals():
        print "%s not in memory yet " % FILENAME
        if os.path.exists(FILENAME):
            print "%s exists. Opening." % FILENAME
            data = tables.open_file(FILENAME, 'a')
        else:
            print "%s does not exist. Trying to read from ESD"
            data = create_new_event_file(FILENAME, STATIONS, START, END)
    else:
        print "data already in globals."

    events = data.root.s501.events

    ph = events.col('pulseheights')
    ph1 = ph[:, 0]
    ph2 = ph[:, 1]
    ph3 = ph[:, 2]
    ph4 = ph[:, 3]

    plt.xkcd()
    plt.figure()
    plt.hist(ph1, bins=np.arange(10.,1200.,20.), histtype='step')
    plt.title('/lio-project/pulseheight_histogram/histogram.py')
    #plt.legend('[s501. detector 1. 2010-4-1 24h]')
    plt.xlabel('pulshoogte [ADC]')
    plt.ylabel('aantal')
    plt.savefig('histogram.py.xkcd.png',dpi=150)
    plt.show()
    data.close()
