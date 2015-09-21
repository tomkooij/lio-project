"""
Read data from station 501 and plot t1-t2 histogram

Goal: recreate graphs form D.Pennink 2010
t1-t2 from station 501, FULL YEAR 2010

Remark from D.Fokkema: select "1,2" for low,low (--> 3,4 high, high)
but then use 3,4 for high, high etc

Goal: controleer of de spreiding ook in "zelfde" events zit
Antwoord: Ja, dit is zo. Ook in events zijn fotonen later.

ph1 > TRIGGER = charged particle
ph1 < TRIGGER = gamma

"""
from __future__ import division

import gauss_fit_histogram
import datetime
import tables
import sapphire.esd
import numpy as np
import matplotlib.pyplot as plt
import os.path
import sys 

XKCD = False

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2010, 4, 1)
END = datetime.datetime(2010, 5, 1)
FILENAME = 'simulated_no_fotons_bigdiamond.h5'

#
# Pennink, 2010 p32 specifies these cutoff ADC counts
# >200 ADC count = charged particle
# <120 ADC counts = gamma
# These values are consistent with a pulseheight histogram
#
HIGH_PH = 200
LOW_PH = 60

# convert number of particles to pulseheight (in ADC) 1 MIP = 200 mV = 315 ADC
N_TO_PH_FACTOR = 1./315.

#
# Read event data from the ESD
#  store in table `/sSTATION' for example: /s501
#
def create_new_event_file(filename, stations, start, end):

    print "No way! create_new_event_file() called for no reason!"

    sys.exit(1)


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

    events = data.root.simrun.cluster_simulations.station_0.events

    t1 = events.col('t1')
    t2 = events.col('t2')
    t3 = events.col('t3')
    t4 = events.col('t4')

    # convert "number of particles n to ph"
    ph1 = events.col('n1') / N_TO_PH_FACTOR
    ph2 = events.col('n2') / N_TO_PH_FACTOR
    ph3 = events.col('n3') / N_TO_PH_FACTOR
    ph4 = events.col('n4') / N_TO_PH_FACTOR


    bins2ns5 = np.arange(-16.25, 16.26, 2.5)

    selectie_1hoog_2hoog = ((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                    & (ph1 > HIGH_PH) & (ph2 > HIGH_PH))

    selectie_3hoog_4hoog = ((t3 > 0) & (t4 > 0) & ((t3-t4) < 50.)
                                    & (ph3 > HIGH_PH) & (ph4 > HIGH_PH))

    t1 = t1.compress(selectie_1hoog_2hoog)
    t2 = t2.compress(selectie_1hoog_2hoog)


    t3 = t3.compress(selectie_3hoog_4hoog)
    t4 = t4.compress(selectie_3hoog_4hoog)

    grafiek = plt.figure()
    grafiek11 = grafiek.add_subplot(111)

    dt_12 = t1-t2
    #dt_12 = t3-t4

    print "All events", dt_12.size
    n1, bins1, blaat1 = grafiek11.hist(dt_12, bins=bins2ns5, histtype='step')
    sigma_list = np.sqrt(n1)
    c, fitx, fity = gauss_fit_histogram.gauss_fit_histogram(n1, bins1, sigma=sigma_list, initialguess = [500.,-10., -10., 5.], verbose=False)
    mu = c[1]
    print "gemiddelde van dataset: ", mu
    sigma = abs(c[2])
    print "sigma fit figuur11 = ", sigma

    grafiek11.plot(fitx, fity, 'r--', linewidth=3)
    grafiek11.set_title('ph1,ph2=hoog, hoog')
    grafiek11.set_xlabel('t1-t2 [ns]')
    grafiek11.set_ylabel('aantal events')


    plt.tight_layout()
    #grafiek.savefig('pennink4plots.png', dpi=150)
    grafiek.show()



if __name__=='__main__':

    if XKCD:
        print "plotting everything in xkcd style :-p"
        with plt.xkcd():
            do_it()
    else:
        do_it()
        # grafiek21.rcdefaults()   # reset matplotlib defaults
