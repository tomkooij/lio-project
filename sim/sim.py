import random

import matplotlib.pyplot as plt
import numpy as np

from progressbar import ProgressBar, ETA, Bar, Percentage

from next_time import time_series, next_time


# number of events to generate
N = int(1e5)

# events far from the core have low lepton detection probability
LEPTON_DETECTION_PROBABILITY = 0.50 # based on particle density in shower
PHOTON_DETECTION_PROBABILITY = 0.05 # based on scinitlator interaction
NUMBER_OF_PHOTONS = 5 # density photons = 10* density leptons
DELTA_TIME_PHOTONS = 5 # must fit in "shower pancake"
DELTA_TIME_LEPTONS = 20 # ns ref fig 2.3 Fokkema2012

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

    t = np.array([0,0,0,0])
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

if __name__=='__main__':

    t1 = []
    t2 = []
    t3 = []
    t4 = []
    ph1 = []
    ph2 = []
    ph3 = []
    ph4 = []
    total_ph = []


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

            total_ph.append(sum(ph))

    t1 = np.array(t1)
    t2 = np.array(t2)
    dt = t1 - t2

    ph1 = np.array(ph1)
    ph2 = np.array(ph2)

    dt_sel = dt.compress((ph1 == 10) & (ph2 == 10) & (t1 > 0) & (t2 > 0))
    print "Number of events in selection: ",dt_sel.size

    plt.hist(dt_sel,bins=20,histtype='step')
    plt.title('delta-t histogram left=low ph (photon) right=high ph (lepton)')
    plt.xlabel('t_HIGH - t2 [ns]')
    plt.ylabel('number of events')
    plt.show()
