"""
investigate time difference t1-t2 in corsika groundparticlesim data
"""

import tables
import numpy as np
import matplotlib.pyplot as plt
import itertools

N_MIN = 0.05 # minimum mips that still is particle/event (t!=-999)
N_MIN_LEPTON = 0.7 # everything above = lepton
N_MAX_PHOTON = 0.2 # everything below = gamma

def get_timestamp_of_first_groundparticle(events):
    """
    get timestamp of first groundparticle (usually >>1e5 ns in corsika)
    """
    t1 = events.col('t1')
    t2 = events.col('t2')
    t3 = events.col('t3')
    t4 = events.col('t4')

    t1 = t1.compress(t1>0)
    t2 = t2.compress(t2>0)
    t3 = t3.compress(t3>0)
    t4 = t4.compress(t4>0)

    t0 = min(np.min(t1),np.min(t2),np.min(t3),np.min(t4))   # timestamp of first particle in shower

    assert(t0 > 0)

    return t0

def prepare_delta_t(events, k, j):
    """
    extract timecolumns k and j from event table. Compute t_k - t_j

    remove t = -999 (no particle)

    substract time of first particle (needed for corsika gpsim)
    """

    t0 = get_timestamp_of_first_groundparticle(events)

    t_k = events.col('t%d' % k) - t0
    t_j = events.col('t%d' % j) - t0

    dt = (t_k - t_j).compress((t_k > 0) & (t_j > 0))

    n_k = events.col('n1').compress((t_k > 0) & (t_j > 0))
    n_j = events.col('n2').compress((t_k > 0) & (t_j > 0))

    assert(n_k.size==dt.size)
    assert(n_j.size==dt.size)

    return dt, n_k, n_j

if __name__=='__main__':

    data = tables.open_file('600k_events_gammas.h5', 'r')

    events = data.root.cluster_simulations.station_0.events

    dt_hoog_laag = np.array([], dtype='float32')
    dt_laag_hoog = np.array([], dtype='float32')
    dt_laag_laag = np.array([], dtype='float32')

    for i,j in itertools.combinations(range(1,5),2):

        print "combinatie: ",i,j
        dt, n1, n2 = prepare_delta_t(events, i, j)
        print "dt.size, dt_laag_laag.size", dt.size, dt.compress((n1>N_MIN) & (n2>N_MIN) & (n2 < N_MAX_PHOTON)).size

        dt_hoog_laag = np.concatenate((dt.compress((n1>N_MIN_LEPTON) & (n2>N_MIN) & (n2 < N_MAX_PHOTON)), dt_hoog_laag))
        dt_laag_hoog = np.concatenate((dt.compress((n2>N_MIN_LEPTON) & (n1>N_MIN) & (n1 < N_MAX_PHOTON)), dt_laag_hoog))
        dt_laag_laag = np.concatenate((dt.compress((n2>N_MIN) & (n2 < N_MAX_PHOTON) & (n1>N_MIN) & (n1 < N_MAX_PHOTON)), dt_laag_laag))

    plt.figure()
    plt.hist(dt_hoog_laag, bins=np.arange(-21.25,21.24,2.5))
    plt.figure()
    plt.hist(dt_laag_hoog, bins=np.arange(-21.25,21.24,2.5))
    plt.figure()
    plt.hist(dt_laag_laag, bins=np.arange(-52.5,52.49,5.))
    plt.show()
