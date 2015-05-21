# -*- coding: utf-8 -*-
"""

Investigate Pytables.read_where()/Numpy.compress() performance

"""



max_core_distance = 400  	# m
N = 1000					# monte carlo runs

import tables
from timeit import default_timer as timer
import numpy as np

from sapphire.simulations.groundparticles import GroundParticlesSimulation
#from sapphire.simulations.groundparticles import OptimizeQueryGroundParticlesSimulation
#from sapphire.simulations.groundparticles import OptimizeQuery_ParticlesOnly_GroundParticlesSimulation
from sapphire.simulations.groundparticles import NumpyGPS

from sapphire.clusters import ScienceParkCluster


cluster = ScienceParkCluster()


SHOWERS = {'1e14 eV 7Mb unsorted': 'corsika_713335232_854491062.h5',
            '1e14 eV 6Mb sorted+csi': 'sorted_713335232.h5'}
    #        '1e16 eV 88Mb unsorted': 'corsika_10019744_792483217.h5',
    #        '1e14 eV 81Mb sorted+csi': 'sorted_10019744.h5'}

def do_compare(corsikafile_path):
    data_old = tables.open_file('bagger1.h5', 'w')
    data_opt = tables.open_file('bagger2.h5', 'w')

    print "N = ",N
    print "old code pytables_readwhere:"
    start = timer()

    sim_old = GroundParticlesSimulation(corsikafile_path, max_core_distance, cluster, data_old, '/', N, seed=42)

    sim_old.run()
    end = timer()
    t_old = end - start

    testvalue_old = data_old.root.coincidences.coincidences.read_where('N>0')
    print "number of coincidences: ", len(testvalue_old)

    print "new code: NumpyGPS"
    start = timer()

    sim_opt = NumpyGPS(corsikafile_path, max_core_distance, cluster, data_opt, '/', N, seed=42)

    sim_opt.run()
    end = timer()
    t_opt = end - start

    testvalue =  data_opt.root.coincidences.coincidences.read_where('N>0')
    print "number of coincidences: ", len(testvalue)

    for a,b in zip(testvalue_old,testvalue):
        if a != b:
            print "Coincidence not equal. Index equal? ", (a[0]==b[0]), a, b
    data_old.close()
    data_opt.close()

    return t_old, t_opt

if __name__ == '__main__':

    results = {}
    for shower_key in SHOWERS:
        print "\n*** testcase: ", shower_key
        results[shower_key] = do_compare(SHOWERS[shower_key])

    print "\n results:"
    for result_key in results:
        print "Testcase: %s pytables: %3.2f s compress: %3.2f s" % (result_key,results[result_key][0], results[result_key][1])
