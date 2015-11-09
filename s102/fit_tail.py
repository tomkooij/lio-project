"""
maak een histogram van aankomsttijdveschillen van station 102 (2 plaats)
t2-t1
t1 = laag (<0.5MIP)
t2 = hoog (>1 MIP)

Dataset: s102, jan t/m okt
"""
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import math
import tables
from scipy.optimize import curve_fit



PLOT_TRACES = False   # download en plot traces
FILENAME = 's102_heel2015.h5'

MIP = 150 / 0.57  # ADC =  mV/0.57
LOW_PH = 0.5*MIP
HIGH_PH = 1.*MIP

def fit_func_for_plot(x, a, mu, sigma, background):
    gauss = a*np.exp(-0.5*((x-mu)/sigma)**2)

    if x < 0:
        tail = 650000.
    else:
        tail = 0

    return gauss + tail + background
#
# fit = gauss + tail + background
#
def fit_func(x, a, mu, sigma, tail_amp, tail_l, background):
    gauss = a*np.exp(-0.5*((x-mu)/sigma)**2)

    tail = np.where(x < 0, tail_amp*np.exp(1./tail_l*x), 0.)

    return gauss + tail + background


if __name__ == '__main__':

    if 'data' not in globals():
        data = tables.open_file(FILENAME, 'a')

    events = data.root.s102.events

    ext_stamp = events.col('ext_timestamp')
    t1 = events.col('t1')
    t2 = events.col('t2')

    ph = events.col('pulseheights')
    ph1 = ph[:, 0]
    ph2 = ph[:, 1]

    bins = np.arange(-251.25, 251.25, 7.5)  # 7.5 ns kan ook. 5ns NIET!

    # remove -1 and -999
    # select events based on pulseheight
    filter = (t1 >= 0) & (t2 >= 0) & (ph1 > 0) & (ph1 < LOW_PH) & (ph2 > HIGH_PH)
    t1_laag = t1.compress(filter)
    t2_hoog = t2.compress(filter)
    ph1_filtered = ph1.compress(filter)
    ph2_filtered = ph2.compress(filter)
    timestamp_filtered = ext_stamp.compress(filter)

    dt = t2_hoog - t1_laag

    print "number of events in hoog/laag filter:", dt.size

    grafiek = plt.figure()

    n1, bins1, blaat1 = plt.hist(dt, bins=bins, histtype='step')
    plt.xlim(-250,250)

    plt.title('s102, jan-okt 2015, t1-t2 (ph1<0.5MIP, ph2>1.0MIP)')
    plt.show()

    #
    # Middens van de bins:
    #
    middle = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]

    sigma = np.sqrt(n1)

    # Least squares: scipy.optimize.curve_fit:
    c, cov = curve_fit(fit_func, middle, n1, p0=[100.,0.,10.,5000.,50.,2000.], sigma=sigma, absolute_sigma=True)

    mu = c[1]
    sigma = abs(c[2])
    tail_amp = c[3]
    tail_l = c[4]
    background = c[5]

    fitx = middle
    fity = fit_func_for_plot(fitx, c[0], c[1], abs(c[2]), c[5])

    plt.plot(fitx, fity ,'r--', linewidth=2)
    plt.plot(fitx, n1-fity, 'g--')
    plt.title('gauss_fit_histogram.py');
    plt.xlabel('pulseheight [ADC]')
    plt.legend([r'fit: $ \mu = %.3f\  \sigma = %.3f\ $' %(mu, sigma), 't2-t1' ], loc = 2, bbox_to_anchor=(1,1))
    plt.show()
