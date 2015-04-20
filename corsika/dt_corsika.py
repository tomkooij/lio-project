"""
investigate time difference t1-t2 in corsika groundparticlesim data
"""

import tables
import numpy as np

def prepare_t_n(events):
    """
    extract timecolumns from event table

    clean np.array for example events.col('t1')

    remove t = -999 (no particle)

    substract time of first particle (needed for corsika gpsim)
    """
    t1 = events.col('t1')
    t2 = events.col('t2')
    t3 = events.col('t3')
    t4 = events.col('t4')

    n1 = events.col('n1').compress(t1 > 0) # remove t = -999 events
    n2 = events.col('n2').compress(t2 > 0)
    n3 = events.col('n3').compress(t3 > 0)
    n4 = events.col('n4').compress(t4 > 0)

    t1 = t1.compress(t1 > 0)
    t2 = t2.compress(t2 > 0)
    t3 = t3.compress(t3 > 0)
    t4 = t4.compress(t4 > 0)

    t0 = min(np.min(t1),np.min(t2),np.min(t3),np.min(t4))   # timestamp of first particle in shower

    assert(t0 > 0)

    t1 = t1 - t0
    t2 = t2 - t0
    t3 = t3 - t0
    t4 = t4 - t0

    assert(t1.size==n1.size)
    assert(t2.size==n2.size)
    assert(t3.size==n3.size)
    assert(t4.size==n4.size)
    
    return t1,t2,t3,t4, n1, n2, n3, n4

if __name__=='__main__':

    data = tables.open_file('10k_gamma.h5', 'r')

    events = data.root.cluster_simulations.station_0.events

    t1,t2,t3,t4, n1, n2, n3, n4 = prepare_t_n(events)
