"""
26 juni 2015

Welke type events zitten in de pennink selectie:

hhHH laag laag | hoog hoog
hhLH laag laag | laag hoog
hhHL laag laag | hoog laag
hhLL laag laag | laag laag

ph1 > HIGH_PH = charged particle
ph1 < LOW_PH = gamma

"""

import gauss_fit_histogram
import datetime
import tables
import sapphire.esd
import numpy as np
import matplotlib.pyplot as plt
import os.path


XKCD = False

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2010, 4, 1)
END = datetime.datetime(2010, 5, 1)
FILENAME = 'sorted.h5'

#
# Pennink, 2010 p32 specifies these cutoff ADC counts
# >200 ADC count = charged particle
# <120 ADC counts = gamma
# These values are consistent with a pulseheight histogram
#
HIGH_PH = 200
LOW_PH = 120


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


def do_it():

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

    t1 = events.col('t1')
    t2 = events.col('t2')
    t3 = events.col('t3')
    t4 = events.col('t4')

    ph = events.col('pulseheights')
    ph1 = ph[:, 0]
    ph2 = ph[:, 1]
    ph3 = ph[:, 2]
    ph4 = ph[:, 3]

    bins2ns5 = np.arange(-41.25, 41.26, 2.5)

    # 3,4 hoog == 1,2 laag
    selectie_1laag_2laag = ((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                    & (ph1 < LOW_PH) & (ph2 < LOW_PH))

    t1 = t1.compress(selectie_1laag_2laag)
    t2 = t2.compress(selectie_1laag_2laag)
    t3 = t3.compress(selectie_1laag_2laag)
    t4 = t4.compress(selectie_1laag_2laag)

    ph1 = ph1.compress(selectie_1laag_2laag)
    ph2 = ph2.compress(selectie_1laag_2laag)
    ph3 = ph3.compress(selectie_1laag_2laag)
    ph4 = ph4.compress(selectie_1laag_2laag)

    """
    plt.figure()
    plt.hist(ph1, bins=np.arange(0,400,10.), histtype='step')
    plt.hist(ph2, bins=np.arange(0,400,10.), histtype='step')
    plt.hist(ph3, bins=np.arange(0,400,10.), histtype='step')
    plt.hist(ph4, bins=np.arange(0,400,10.), histtype='step')
    plt.show()
    """

    timestamps = events.col('timestamp')
    nanoseconds = events.col('nanoseconds')
    timestamps = timestamps.compress(selectie_1laag_2laag)
    nanoseconds = nanoseconds.compress(selectie_1laag_2laag)

    print "number of events (llXX): ", timestamps.size
    print "aantal niet llHH (en dus 3x laag): ", timestamps.compress((ph3 < LOW_PH) & (ph4 < LOW_PH)).size

    """
    for timestamp, ns in zip(timestamps, nanoseconds):

        query = '(timestamp == %s) & (nanoseconds == %s) ' % (timestamp, ns)
        print timestamp, ns
        #print query
        print events.read_where(query)[0][4]
    """

if __name__=='__main__':

    if XKCD:
        print "plotting everything in xkcd style :-p"
        with plt.xkcd():
            do_it()
    else:
        do_it()
        # grafiek21.rcdefaults()   # reset matplotlib defaults
