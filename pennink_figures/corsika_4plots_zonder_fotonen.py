"""
Read data from station 501 and plot t1-t2 histogram

Goal: recreate graphs form D.Pennink 2010
t1-t2 from station 501, FULL YEAR 2010

ph1 > TRIGGER = charged particle
ph1 < TRIGGER = gamma

"""

import gauss_fit_histogram
import datetime
import tables
import sapphire.esd
import numpy as np
import matplotlib.pyplot as plt
import os.path
import sys


XKCD = False

FILENAME = 'simulated_no_fotons_200k_simB.h5'

MIP = 380  # ADC   1.0 MIP = 380 ADC
#
# Pennink, 2010 p32 specifies these cutoff ADC counts
# >200 ADC count = charged particle
# <120 ADC counts = gamma
# These values are consistent with a pulseheight histogram
#
HIGH_PH = 200.
LOW_PH = 120.


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
            print "%s does not exit. Can't create. Please fix!", FILENAME
            sys.exit(0)
    else:
        print "data already in globals."

    #events = data.root.s501.events
    events = data.root.simrun.cluster_simulations.station_0.events

    t1 = events.col('t1')
    t2 = events.col('t2')
    t3 = events.col('t3')
    t4 = events.col('t4')

    n1 = events.col('n1')
    n2 = events.col('n2')
    n3 = events.col('n3')
    n4 = events.col('n4')

    ph1 = n1 * MIP
    ph2 = n2 * MIP
    ph3 = n3 * MIP
    ph4 = n4 * MIP


    bins2ns5 = np.arange(-41.25, 41.26, 2.5)

    dt_all = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.))
    dt_t1hoog_t2laag = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                        & (ph2 < LOW_PH) & (ph1 > HIGH_PH))
    dt_t1laag_t2hoog = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                        & (ph2 > HIGH_PH) & (ph1 < LOW_PH))
    dt_t1laag_t2laag = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                        & (ph1 < LOW_PH) & (ph2 < LOW_PH))

    plt.hist(ph1,np.arange(0.1,2000.,30.))
    plt.show()

    grafiek = plt.figure()
    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)


    if grafiek11:
        print "All events", dt_all.size
        n1, bins1, blaat1 = grafiek11.hist(dt_all, bins=bins2ns5, histtype='step')
        sigma_list = np.sqrt(n1)
        c, fitx, fity = gauss_fit_histogram.gauss_fit_histogram(n1, bins1, sigma=sigma_list, initialguess = [100.,10., 10., 0.], verbose=False)
        mu = c[1]
        print "gemiddelde van dataset: ", mu
        sigma = abs(c[2])
        print "sigma fit figuur11 = ", sigma

        grafiek11.plot(fitx, fity, 'r--', linewidth=3)
        grafiek11.set_title('ph1,ph2=hoog, hoog')
        #grafiek11.set_xlabel('t1-t2 [ns]')
        grafiek11.set_ylabel('aantal events')


    if grafiek12:  # bovenste rij, laag laag met fit
        print "ph1 laag, ph2 laag", dt_t1laag_t2laag.size
        n1, bins1, blaat1 = grafiek12.hist(dt_t1laag_t2laag, bins=bins2ns5, histtype='step')

        sigma_list = np.sqrt(n1)

        #c, fitx, fity = gauss_fit_histogram.gauss_fit_histogram(n1, bins1, sigma=sigma_list, initialguess = [100.,10., 10., 0.], verbose=False)
        #mu = c[1]
        #sigma = abs(c[2])
        print "sigma fit 12 = ", sigma

        #grafiek12.plot(fitx, fity, 'r--', linewidth=3)
        grafiek12.set_title('ph1,ph2=laag, laag')
        #grafiek12.set_xlabel('t1-t2 [ns]')
        #grafiek12.set_ylabel('aantal events')


    if grafiek21:  # onderste rij, scheve verdelingen, zonder fit
        print "ph1 hoog, ph2 laag", dt_t1hoog_t2laag.size
        n1, bins1, blaat1 = grafiek21.hist(dt_t1hoog_t2laag, bins=bins2ns5, histtype='step')
        grafiek21.set_title('ph1,ph2=hoog, laag')
        grafiek21.set_xlabel('t1-t2 [ns]')
        grafiek21.set_ylabel('aantal events')

    if grafiek22:
        print "ph1 laag, ph2 hoog", dt_t1laag_t2hoog.size
        n1, bins1, blaat1 = grafiek22.hist(dt_t1laag_t2hoog, bins=bins2ns5, histtype='step')
        grafiek22.set_title('ph1,ph2=laag, hoog')
        grafiek22.set_xlabel('t1-t2 [ns]')
        #grafiek22.set_ylabel('aantal events')


    plt.tight_layout()
    grafiek.savefig('pennink4plots-corsika_data.png', dpi=150)
    grafiek.show()



if __name__=='__main__':

    if XKCD:
        print "plotting everything in xkcd style :-p"
        with plt.xkcd():
            do_it()
    else:
        do_it()
        # grafiek21.rcdefaults()   # reset matplotlib defaults