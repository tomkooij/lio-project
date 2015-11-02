# read time differences from GroundParticlesSimulation runs

from sapphire import CorsikaQuery
from math import degrees, log10

import tables
import glob
import os

PATHS = '/data/hisparc/tom/simruns/s15eV_no_fotons/*_*.h5'
OVERVIEW = '/data/hisparc/corsika/corsika_overview.h5'

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
    print seeds, energy, zenith

    with tables.open_file(FILENAME, 'r') as data:
        events = data.root.simrun.cluster_simulations.station_0.events
        print event.size

        n1 = np.concatenate((n1, events.col('n1')))
        n2 = np.concatenate((n2, events.col('n2')))
        n3 = np.concatenate((n3, events.col('n3')))
        n4 = np.concatenate((n4, events.col('n4')))
        t1 = np.concatenate((t1, events.col('t1')))
        t2 = np.concatenate((t2, events.col('t2')))
        t3 = np.concatenate((t3, events.col('t3')))
        t4 = np.concatenate((t4, events.col('t4')))

    print t1.size, t2.size
