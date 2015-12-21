# zenit.py
#
# prepare a set of CORSIKA simulations to simulate a real zenit distribution
#
from __future__ import division

import numpy as np
import math
import random
import tables
import os.path
import matplotlib.pyplot as plt

from sapphire.corsika.corsika_queries import CorsikaQuery

from sapphire.simulations.groundparticles import GroundParticlesSimulation
from sapphire.simulations.detector import HiSPARCSimulation
from sapphire.clusters import SingleDiamondStation


max_core_distance = 25
N = 5000
cluster = SingleDiamondStation()
ENERGY_LOG10 = 14

MIP = 380  # ADC   1.0 MIP = 380 ADC
#
# Pennink, 2010 p32 specifies these cutoff ADC counts
# >200 ADC count = charged particle
# <120 ADC counts = gamma
# These values are consistent with a pulseheight histogram
#
HIGH_PH = 200.
LOW_PH = 120.


ITERATIONS = 40

CORSIKAPATH = '/data/hisparc/corsika/data/'
INDEXFILE = '/data/hisparc/corsika/corsika_overview.h5'
OUTPUTFILE = '1day_1e15ev_fotons.h5'

def round_to_7_5(x, base=7.5):
    return base * round(float(x)/base)

def simrun():
    query = CorsikaQuery(INDEXFILE)
    zenith_list = []

    with tables.open_file(OUTPUTFILE, 'w') as data:

        for iteration in range(ITERATIONS):

            zenith = round_to_7_5(math.degrees(HiSPARCSimulation.generate_zenith()))

            print "iteration %d of %d, zenith = %2.1f" % (iteration, ITERATIONS, zenith)
            zenith_list.append(zenith)

            sim = random.choice(query.simulations(energy=ENERGY_LOG10,zenith=zenith))
            seed = str(sim[0])+'_'+str(sim[1])
            print "seed %s (E=1e%d, zenith=%2.1f)" % (seed, ENERGY_LOG10, zenith)

            CORSIKAFILENAME = CORSIKAPATH + seed + '/corsika.h5'

            # show corsika output file stats
            with tables.open_file(CORSIKAFILENAME, 'r') as corsikafile:
                eventheader = corsikafile.get_node_attr('/', 'event_header')
                print "CORSIKA Inputfile: ", CORSIKAFILENAME
                print "primary particle: %s energy: E+%d zenith: %2.1f" % (eventheader.particle, math.log10(eventheader.energy),
                     math.degrees(eventheader.zenith))
                print "number of groundparticles: ", corsikafile.root.groundparticles.nrows

            sim = GroundParticlesSimulation(CORSIKAFILENAME, max_core_distance, cluster, data, '/simrun'+str(iteration), N)
            sim.run()

def readdata():
    n1  = np.array([])
    n2  = np.array([])
    n3  = np.array([])
    n4  = np.array([])
    t1  = np.array([])
    t2  = np.array([])
    t3  = np.array([])
    t4  = np.array([])
    with tables.open_file(OUTPUTFILE, 'r') as data:
        for node in data.walk_nodes('/', 'Leaf'):
            if type(node) is tables.table.Table:
                if node.name == 'events':
                    print node
                    n1 = np.concatenate((n1, node.col('n1')))
                    n2 = np.concatenate((n2, node.col('n2')))
                    n3 = np.concatenate((n3, node.col('n3')))
                    n4 = np.concatenate((n4, node.col('n4')))
                    t1 = np.concatenate((t1, node.col('t1')))
                    t2 = np.concatenate((t2, node.col('t2')))
                    t3 = np.concatenate((t3, node.col('t3')))
                    t4 = np.concatenate((t4, node.col('t4')))

    return t1,t2,t3,t4,n1,n2,n3,n4

if __name__ == '__main__':
    if not os.path.exists(OUTPUTFILE):
        simrun()
    else:
        print "%s exists. Skipping simrun." % OUTPUTFILE
    print "Gathering data:"
    t1,t2,t3,t4,n1,n2,n3,n4 = readdata()
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
