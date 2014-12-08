"""

corsika pulseintegral

Process datafiles met "sapphire.simulations.GroundParticleSim" output

bron simulaties AdL zie email 1dec2014

"""

import tables
import numpy as np
import matplotlib.pyplot as plt

# datafiles (AdL email 1dec2014)
FILENAME1 = '15_45_simulation.h5'
FILENAME2 =  '16_45_simulation.h5'
FILENAME3 = '16_7_5_simulation.h5'
FILENAME4 = '17_45_simulation.h5'

# TK generated data from corsika_run_sim.py
FILENAME5 = 'gp_sim_output.h5'
FILENAME6 = 'gp_sim_output_bruikbaar.h5'

if __name__=='__main__':

    print 'pulseheight histograms from CORSIKA sims (using GroundParticleSim output) \n'
    data = tables.open_file(FILENAME5, 'r')

# for FILENAME 1-4 (AdL)
#    events = data.root.cluster_simulations.station_501.events
    events = data.root.simrun.cluster_simulations.station_0.events

    n1 = events.col('n1') # er is geen pulseintegral data, maar "n" aantal mips is hetzelfde

    bins = np.arange(0.1, 5.,0.05)

    plt.figure()
    plt.hist(n1, bins)
