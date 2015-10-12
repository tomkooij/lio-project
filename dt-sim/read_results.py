# read time differences from GroundParticlesSimulation runs

from sapphire import CorsikaQuery
from math import degrees, log10

import matplotlib.pyplot as plt
import numpy as np
import tables
import glob
import os

PATHS = '/data/hisparc/tom/simruns/s15eV_no_fotons/*_*.h5'
OVERVIEW = '/data/hisparc/corsika/corsika_overview.h5'

MIP = 380  # ADC   1.0 MIP = 380 ADC
#
# Pennink, 2010 p32 specifies these cutoff ADC counts
# >200 ADC count = charged particle
# <120 ADC counts = gamma
# These values are consistent with a pulseheight histogram
#
HIGH_PH = 200.
LOW_PH = 120.


if __name__ == '__main__':

    n1  = np.array([])
    n2  = np.array([])
    n3  = np.array([])
    n4  = np.array([])
    t1  = np.array([])
    t2  = np.array([])
    t3  = np.array([])
    t4  = np.array([])



    cq = CorsikaQuery(OVERVIEW)
    for path in glob.glob(PATHS):
        seeds = os.path.basename(path)[:-3]
        sim = cq.get_info(seeds)
        energy = log10(sim['energy'])
        zenith = degrees(sim['zenith'])

        print path
        with tables.open_file(path, 'r') as data:
            events = data.root.simrun.cluster_simulations.station_0.events
            print len(events)

            n1 = np.concatenate((n1, events.col('n1')))
            n2 = np.concatenate((n2, events.col('n2')))
            n3 = np.concatenate((n3, events.col('n3')))
            n4 = np.concatenate((n4, events.col('n4')))
            t1 = np.concatenate((t1, events.col('t1')))
            t2 = np.concatenate((t2, events.col('t2')))
            t3 = np.concatenate((t3, events.col('t3')))
            t4 = np.concatenate((t4, events.col('t4')))

    print t1.size, t2.size

    print n1.size, t1.size
    print "Analysis:"

    ph1 = n1 * MIP
    ph2 = n2 * MIP
    ph3 = n3 * MIP
    ph4 = n4 * MIP

    dt_all = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.))
    dt_t1hoog_t2hoog = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                        & (ph2 > HIGH_PH) & (ph1 > HIGH_PH))
    dt_t1hoog_t2laag = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                        & (ph2 < LOW_PH) & (ph1 > HIGH_PH))
    dt_t1laag_t2hoog = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                        & (ph2 > HIGH_PH) & (ph1 < LOW_PH))
    dt_t1laag_t2laag = (t1-t2).compress((t1 > 0) & (t2 > 0) & ((t1-t2) < 50.)
                                        & (ph1 < LOW_PH) & (ph2 < LOW_PH))

    print dt_all.size, dt_t1hoog_t2hoog.size, dt_t1laag_t2laag.size, dt_t1laag_t2hoog.size, dt_t1hoog_t2laag.size

    bins2ns5 = np.arange(-41.25, 41.26, 2.5)

    grafiek = plt.figure()

    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    grafiek11.hist(dt_t1hoog_t2hoog, bins2ns5, histtype='step')
    grafiek11.set_title('ph1,ph2 == HOOG')
    #grafiek11.set_xlabel('t1-t2 [ns]')

    grafiek12.hist(dt_t1laag_t2laag, bins2ns5, histtype='step')
    grafiek12.set_title('ph1,ph2 == LAAG')
    #grafiek12.set_xlabel('t1-t2 [ns]')

    grafiek21.hist(dt_t1laag_t2hoog, bins2ns5, histtype='step')
    grafiek21.set_title('ph1,ph2 == LAAG, HOOG')
    grafiek21.set_xlabel('t1-t2 [ns]')

    grafiek22.hist(dt_t1hoog_t2laag, bins2ns5, histtype='step')
    grafiek22.set_title('ph1,ph2 == HOOG, LAAG')
    grafiek22.set_xlabel('t1-t2 [ns]')

    grafiek.show()

    print "t1-t2, std dev (HOOG HOOG): %2.1f ns. " % np.std(dt_t1hoog_t2hoog)
    print "t1-t2, std dev (LAAG LAAG): %2.1f ns. " % np.std(dt_t1laag_t2laag)
