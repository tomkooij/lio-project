"""
Read data from station 501 and plot t1-t2 histogram

Goal: recreate graphs form D.Pennink 2010
t1-t2 from station 501, FULL YEAR 2010

ph1 > TRIGGER = charged particle
ph1 < TRIGGER = gamma

"""


import datetime
import tables
import sapphire.esd
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq


# time walk correction function
#t_walk = lambda x: 8.36 * np.exp(-0.06702*(x-20.)) + 5.22 # fit from walk.py
A = 50. # fit 13.11
B = 0. # fit 3.97
t_walk = lambda x: A / np.sqrt(x-20.) + B

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2014,1,1)
END = datetime.datetime(2014,2,1)
FILENAME = 's501_mrt.h5'

#
# Pennink, 2010 p32 specifies these cutoff ADC counts
# >200 ADC count = charged particle
# <120 ADC counts = gamma
# These values are consistent with a pulseheight histogram
#
HIGH_PH = 200
LOW_PH = 120

#
# Open existing coincidence table.
# Only check if "/coincidences" are in table, no other checks
def open_existing_event_file(filename):
    data = tables.open_file(FILENAME, 'a')
    return data


if __name__=='__main__':


    phs = [21., 30., 40., 50., 100., 200., 500.]
    for ph in phs:
        print "t_walk (ph=%3.1f) = %1.2f" % (ph, t_walk(ph))

    #data = create_new_event_file(FILENAME, STATIONS, START, END)
    #data.close()
    if 'data' not in globals():
        data = open_existing_event_file(FILENAME)

    events = data.root.s501.events

    t1 = events.col('t1')
    t2 = events.col('t2')
    t3 = events.col('t3')
    t4 = events.col('t4')

    ph = events.col('pulseheights')
    ph1 = ph[:,0]
    ph2 = ph[:,1]
    ph3 = ph[:,2]
    ph4 = ph[:,3]

    #bins2ns5 = arange(-201.25,202.26,2.5)
    bins2ns5 = np.arange(-51.25,51.26,2.5)
    bins2ns5_midden = np.arange(-50,50.1,2.5)

    #
    # TODO: 4 subplots to recreate the figure from Pennink 2010
    #
    grafiek = plt.figure()

    # time walk correction
    t1_corr = t1 - t_walk(ph1)
    t2_corr = t2 - t_walk(ph2)
    #
    # Plot histogram for t1-t2 using event selection based on pulseheight
    dt = t1 - t2
    dt_corr = t1_corr - t2_corr

    # gemiddelden van de gaussianfit
    OFFSET1 = 5.
    OFFSET2 = 0

    # remove -1 and -999
    # select events based on pulseheight
    dt1_corr = dt_corr.compress((t1 >= 0) & (t2 >= 0) & (ph1 < LOW_PH) & (ph2 > HIGH_PH))
    dt1 = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 < LOW_PH) & (ph2 > HIGH_PH))

    print "number of events", dt1.size
    n1, bins1, blaat1 = plt.hist(dt1-OFFSET1, bins=bins2ns5, histtype='step')
    n2, bins2, blaat2 = plt.hist(dt1_corr-OFFSET2, bins=bins2ns5, histtype='step')
    plt.title('s501, april 2010, delta PMT 1 - PMT 2')
    plt.legend(['t1-t2','-walk'], loc=1)
    plt.show()
