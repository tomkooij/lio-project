"""
histogram van aankomsttijdveschillen van station 102 (2 plaats)
t2-t1
t1 = laag (<0.5MIP)
t2 = hoog (>1 MIP)

Dataset: s102, jan t/m okt

Fit een gauss+achtergrond+exponentiele verdeling
"""
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import math
import tables
from scipy.optimize import curve_fit


# time walk correction function
# fit_clas_note_02_2007.py:
t_walk = lambda x: -3.944 + 22.3 / (x-20.)**0.156


PLOT_TRACES = False   # download en plot traces
#FILENAME = 'station_501_april2010.h5'
FILENAME = 's501_jan_mei_2014.h5'
#FILENAME = 's501_jan_feb_2012.h5'

MIP = 150 / 0.57  # ADC =  mV/0.57
LOW_PH = 90.  #0.5*MIP
HIGH_PH = 200. #1.*MIP

#
# fit = gauss + tail + background
# symmetrisch!
#
def fit_func(x, a, mu, sigma, background, tail_A, tail_l):

    gauss = a*np.exp(-0.5*((x-mu)/sigma)**2)

    tail_links = np.where(x < 0., tail_A * np.exp(x/tail_l), 0)
    tail_rechts = np.where(x > 0., tail_A * np.exp(-x/tail_l), 0)

    return gauss + background #+ tail_links + tail_rechts

if __name__ == '__main__':

    if 'data' not in globals():
        data = tables.open_file(FILENAME, 'r')

    events = data.root.s501.events

    ext_stamp = events.col('ext_timestamp')
    t1 = events.col('t3')
    t2 = events.col('t4')

    ph = events.col('pulseheights')
    ph1 = ph[:, 2]
    ph2 = ph[:, 3]

    # time walk correction
    t1 = t1 - t_walk(ph1)
    t2 = t2 - t_walk(ph2) + 5

    bins = np.arange(-71.25, 71.25, 2.5)  # 7.5 ns kan ook. 5ns NIET!

    # remove -1 and -999
    # select events based on pulseheight
    hoog_hoog_filter = (t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH) & (ph2 > HIGH_PH)
    laag_laag_filter = (t1 >= 0) & (t2 >= 0) & (ph1 > 0) & (ph2 > 0) & (ph1 < LOW_PH) & (ph2 < LOW_PH)
    filter = laag_laag_filter
    t1_laag = t1.compress(filter)
    t2_laag = t2.compress(filter)
    ph1_filtered = ph1.compress(filter)
    ph2_filtered = ph2.compress(filter)
    timestamp_filtered = ext_stamp.compress(filter)


    dt = t2_laag - t1_laag
    filter = hoog_hoog_filter
    t1_hoog = t1.compress(filter)
    t2_hoog = t2.compress(filter)

    OFFSET = 3
    dt_hh = t1_hoog - t2_hoog + OFFSET

    print "number of events in filter:", dt.size

    grafiek = plt.figure()

    n1, bins1, blaat1 = plt.hist(dt, bins=bins, histtype='step', normed=True)
    n2, bins2, blaat2 = plt.hist(dt_hh, bins=bins, histtype='step', normed=True)

    #plt.xlim(-200,200)

    plt.title('s501, t1-t2 (unkown filter)')

    #
    # Middens van de bins:
    #
    middle = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]

    sigma = np.sqrt(n1)

    if 1:
        # Least squares: scipy.optimize.curve_fit:
        c, cov = curve_fit(fit_func, middle, n1, p0=[10000.,0.,15.,100.,100.,20.], sigma=sigma, absolute_sigma=True)

        a = c[0]
        mu = c[1]
        s = abs(c[2])
        bg = c[3]
        tail_A = c[4]
        tail_l = c[5]

        print "Fit: a = %.1f, mu = %.1f, sigma = %2.1f, background = %4.0f, tail_A = %4.0f, tail_l =%2.1f" % (a, mu, s, bg, tail_A, tail_l)

        fitx = np.asarray(middle)
        fity = fit_func(fitx, a, mu, s, bg, tail_A, tail_l)

        chi2 = sum(np.power((n1 - fity)/sigma,2)) / (len(n1) - len(c))
        print "Reduced Chi-squared: ", chi2

        plt.plot(fitx, fity ,'r--', linewidth=2)
        plt.legend([r'fit: $ \sigma $ = %.0f ns' % s, 'laag-laag', 'hoog-hoog'])

    plt.title('Station 501. Jan-Mei 2014. Detector 3 en 4 (10 m afstand)');
    plt.xlabel('t3-t4 [ns] gecorrigeerd voor timewalk')
    plt.ylabel('N (genormaliseerd)')
    plt.xlim(-60,60)
    plt.savefig('501_hh_vs_ll_na_timewalk.png', dpi=200)
    plt.show()
