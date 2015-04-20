"""
investigate time difference t1-t2 in corsika groundparticlesim data
"""

import tables
import numpy as np
import matplotlib.pyplot as plt
import itertools

MIP = 220 # ADC

PH_MIN = 20  # minimum mips that still is particle/event (t!=-999)
PH_MIN_LEPTON = 120  # everything above = lepton
PH_MAX_PHOTON = 70 # everything below = gamma

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

def prepare_delta_t(events, k, l, esddata=False, mip=220):
    """
    extract timecolumns k and j from event table. Compute t_k - t_j

    remove t = -999 (no particle)

    substract time of first particle (needed for corsika gpsim)

    :param events: events table in ESD of groundparticlesim output
    :param k,j: detector ids
    :param esddata=false: use ESD data when true. Default is use groundparticlesim data
    :param mip=220: height of the MIP peak in ADC. Used to convert n1,n2... to pulseheights
    :returns: dt, ph_k, ph_j : timedifference and corresponding pulseheights
    """

    t0 = get_timestamp_of_first_groundparticle(events)

    t_k = events.col('t%d' % k) - t0
    t_l = events.col('t%d' % l) - t0

    dt = (t_k - t_l).compress((t_k > 0) & (t_l > 0))

    if esddata:
        """
        real data from the ESD
        pulseheights are stored in ADC
        """
        ph = events.col('pulseheights')
        ph_k = ph[:,(k-1)].compress((t_k > 0) & (t_l > 0))
        ph_l = ph[:,(l-1)].compress((t_k > 0) & (t_l > 0))

    else:
        """
        sapphire.groundparticlesim() output
        convert number of mips columns (n1, n2...) to pulseheights
        """
        ph_k = events.col('n1').compress((t_k > 0) & (t_l > 0))*mip
        ph_l = events.col('n2').compress((t_k > 0) & (t_l > 0))*mip

    assert(ph_k.size==dt.size)
    assert(ph_l.size==dt.size)

    return dt, ph_k, ph_l

if __name__=='__main__':

    #data = tables.open_file('600k_events_gammas.h5', 'r')

    #events = data.root.cluster_simulations.station_0.events


    data = tables.open_file('station_501_april2010.h5', 'r')
    events = data.root.s501.events

    dt_hoog_laag = np.array([], dtype='float32')
    dt_laag_hoog = np.array([], dtype='float32')
    dt_laag_laag = np.array([], dtype='float32')

    for i,j in itertools.combinations(range(1,5),2):

        print "detectoren: ",i,j
        dt, ph1, ph2 = prepare_delta_t(events, i, j, esddata=True)

        dt_hoog_laag = np.concatenate((dt.compress((ph1>PH_MIN_LEPTON) & (ph2>PH_MIN) & (ph2 < PH_MAX_PHOTON)), dt_hoog_laag))
        dt_laag_hoog = np.concatenate((dt.compress((ph2>PH_MIN_LEPTON) & (ph1>PH_MIN) & (ph1 < PH_MAX_PHOTON)), dt_laag_hoog))
        dt_laag_laag = np.concatenate((dt.compress((ph1>PH_MIN) & (ph1 < PH_MAX_PHOTON) & (ph2>PH_MIN) & (ph2 < PH_MAX_PHOTON)), dt_laag_laag))
        print "laag_laag.size = ", dt_laag_laag.size

    plt.figure()
    plt.hist(dt_hoog_laag, bins=np.arange(-21.25,21.24,2.5))
    plt.figure()
    plt.hist(dt_laag_hoog, bins=np.arange(-21.25,21.24,2.5))
    plt.figure()
    plt.hist(dt_laag_laag, bins=np.arange(-52.5,52.49,5.))
    plt.show()
