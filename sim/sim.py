import random

import matplotlib.pyplot as plt
import numpy as np

from progressbar import ProgressBar, ETA, Bar, Percentage

from next_time import time_series, next_time

FILENAME = 'data.txt'

# number of events to generate
N = int(2e6)

# events far from the core have low lepton detection probability
LEPTON_DETECTION_PROBABILITY = 0.50 # based on particle density in shower
PHOTON_DETECTION_PROBABILITY = 0.05 # based on scinitlator interaction
NUMBER_OF_PHOTONS = 5 # density photons = 10* density leptons
DELTA_TIME_PHOTONS = 10 # must fit in "shower pancake"
DELTA_TIME_LEPTONS = 10 # ns ref fig 2.3 Fokkema2012

def detect_lepton():

    if random.random() < LEPTON_DETECTION_PROBABILITY:
        return next_time(DELTA_TIME_LEPTONS)
    else:
        return 0. # no trigger

def detect_photon():

    arrival_times = time_series(DELTA_TIME_PHOTONS, NUMBER_OF_PHOTONS)

    for t in arrival_times:
        if random.random() < PHOTON_DETECTION_PROBABILITY: # detected!
            return t

    return 0. # not detected


def station():
    """ simulate event """
    t = np.array([-999.,-999.,-999.,999.])
    #ph = [-999,-999,-999,-999]
    ph = [0,0,0,0]

    n_leptons = 0

    for detector in range(4):

        t[detector] = detect_lepton()

        if t[detector] > 0:
            n_leptons += 1
            ph[detector] = 100
            continue

        t[detector] = detect_photon()
        ph[detector] = 10

    if n_leptons > 1:
        base = min(t)
        return t-base, ph
    else:
        return [], []


def simulate_events():
    """ simulate arrival times and phs (to distinguish cp and gammas)"""
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    ph1 = []
    ph2 = []
    ph3 = []
    ph4 = []

    progress = ProgressBar(widgets=[ETA(), Bar(), Percentage()])

    print "N = ", N

    for _ in progress(range(N)):
        t, ph  = station()

        if t != []:

            t1.append(t[0])
            t2.append(t[1])
            t3.append(t[2])
            t4.append(t[3])

            ph1.append(ph[0])
            ph2.append(ph[1])
            ph3.append(ph[2])
            ph4.append(ph[3])

    return t1,t2,t3,t4, ph1, ph2, ph3, ph4


def do_plots(t1, t2, t3, t4, ph1, ph2, ph3, ph4):
    t1 = np.array(t1)
    t2 = np.array(t2)
    dt = t1 - t2

    ph1 = np.array(ph1)
    ph2 = np.array(ph2)

    dt_high_low = dt.compress((ph1 == 100) & (ph2 == 10) & (t1 > 0) & (t2 > 0))
    print "Number of events in selection (high-low): ",dt_high_low.size
    dt_low_low = dt.compress((ph1 == 10) & (ph2 == 10) & (t1 > 0) & (t2 > 0))
    print "Number of events in selection (low-low): ",dt_low_low.size

    bins = np.arange(-72.5,72.5,5)
    plt.hist(dt_high_low,bins=bins,histtype='step')
    plt.title('sim/sim.py: delta-t histogram left=low ph (photon) right=high ph (lepton)')
    plt.xlabel('t1 - t2 [ns]')
    plt.ylabel('number of events')
    plt.savefig('laaghoog.png',dpi=150)
    plt.show()

    plt.hist(dt_low_low,bins=bins,histtype='step')
    plt.title('sim/sim.py: delta-t histogram low,low (photon, photon)')
    plt.xlabel('t1 - t2 [ns]')
    plt.ylabel('number of events')
    plt.savefig('laaglaag.png',dpi=150)
    plt.show()

if __name__=='__main__':
    try:
        t1, t2, t3, t4, ph1, ph2, ph3, ph4 = np.loadtxt(FILENAME)
    except IOError:
        t1, t2, t3, t4, ph1, ph2, ph3, ph4 = simulate_events()
        np.savetxt(FILENAME, [t1, t2, t3, t4, ph1, ph2, ph3, ph4])
        print "saved: ", FILENAME
    do_plots(t1, t2, t3, t4, ph1, ph2, ph3, ph4)
