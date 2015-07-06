"""
create seperate table with only "charged leptons" in hdf5
when sortedby=x this should be fast
"""

import tables
import numpy as np
from sapphire.corsika.store_corsika_data import GroundParticles

FILENAME = 'corsika_713335232_854491062_sorted.h5'


if __name__=='__main__':
    with tables.open_file(FILENAME, 'a') as data:

        n_leptons = len(data.root.groundparticles) / 10
        try:
            data.get_node('/groundparticles')._f_move(newname='all')
        except tables.NodeError:
            pass

        source_table = data.root.all

        dest_table = data.create_table('/', 'groundparticles', GroundParticles,
                                             'only charged leptons',
                                             expectedrows=n_leptons)

        print "creating lepton table in /groundparticles"

        source_table.append_where(dest_table, '(particle_id >= 2) & (particle_id <= 6)')
        dest_table.flush()
        #print "number of records: ", len(dest_table.root.leptons)

        print "Don't forget to ptrepack --sortby x --propindexes"
