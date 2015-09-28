# zenit.py
#
# prepare a set of CORSIKA simulations to simulate a real zenit distribution
#
from __future__ import division
import numpy as np
import math
import random
from sapphire.corsika.corsika_queries import CorsikaQuery

MAX_ZENITH = 40.   # maximum zenith angle to include in analysis
INDEXFILE = '../corsika/simulation_overview.h5'

if __name__=='__main__':
    query = CorsikaQuery(INDEXFILE)
    zenith_list = [hoek for hoek in sorted(query.all_zeniths) if hoek < MAX_ZENITH]
    print zenith_list
    #middle = [math.radians((zenit_list[i]+zenit_list[i+1])/2.) for i in range(0, len(zenit_list)-1)]
    #print middle

    for zenith in zenith_list:
        weging = np.sin(math.radians(zenith))*(np.cos(math.radians(zenith)))**6
        sim = random.choice(query.simulations(energy=15.,zenith=zenith))
        seed = str(sim[0])+'_'+str(sim[1])
        print "seed %s met weging %1.3f (E=1E+15, zenith=%2.1f)" % (seed, 100*weging, zenith)

        print "copy %s from . to . "
        
        print "running simulation"
