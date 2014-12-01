"""

corsika pulseintegral

Process datafiles met "sapphire.simulations.GroundParticleSim" output

bron simulaties AdL zie email 1dec2014

"""

import tables

# datafiles (AdL email 1dec2014)
FILENAME1 = '15_45_simulation.h5'
FILENAME2 =  '16_45_simulation.h5'
FILENAME3 = '16_7_5_simulation.h5'
FILENAME4 = '17_45_simulation.h5'

if __name__='__main__'

    print 'pulseheight histograms from CORSIKA sims (using GroundParticleSim output) \n'
    data = table.file_open(FILENAME1, 'r')

    events = data.root.cluster_simulations.station_501.events

    n1 = events.col('n1') # er is geen pulseintegral data, maar "n" aantal mips is hetzelfde

    bins = arange(0.1, 5.,0.05)

    hist(n1, bins)
