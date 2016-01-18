"""
show CORSIKA simulation (input) info for all corsika subfolders in a folder
"""

from __future__ import division

import os
import glob
import math

from sapphire import CorsikaQuery


OVERVIEW = '../corsika_science_park/corsika_overview.h5'
DATADIR = '../corsika_science_park'
OVERVIEW_STBC = '/data/hisparc/corsika/corsika_overview.h5'
DATADIR_STBC = '/data/hisparc/adelaat/science_park_corsika'



def seeds_with_output(folder):
    """Get the seeds of simulations for which result.h5 exists in folder"""

    files = glob.glob(os.path.join(folder, '*_*/result.h5'))
    seeds = [os.path.basename(os.path.dirname(file)) for file in files]
    return set(seeds)


def show_simulations(folder):

    seeds = seeds_with_output(DATADIR)
    query = CorsikaQuery(OVERVIEW)

    for seed in seeds:

        simulation = query.get_info(seed)
        zenith = math.degrees(simulation['zenith'])
        energy = math.log10(simulation['energy'])
        print "Sim %s: energy = %.1f eV zenith = %.1f degrees" % (seed, energy, zenith)

    query.finish()


if __name__ == "__main__":

    if os.path.exists('/data/hisparc'):
        # @Nikhef
        OVERVIEW = OVERVIEW_STBC
        DATADIR = DATADIR_STBC

    show_simulations(DATADIR)
