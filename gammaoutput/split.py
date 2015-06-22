"""
split corsika file into "leptons" and "gammas"
"""

import tables
import numpy as np
from sapphire.corsika.store_corsika_data import GroundParticles

FILENAME = 'corsika_713335232_854491062_sorted.h5'

def copy_rows(source, destination, query, n):
    table = destination.create_table('/', 'groundparticles', GroundParticles,
                                                 'Particles',
                                                 expectedrows=n)
    source.append_where(table, query)

    table.flush()
    print "number of records: ", len(destination.root.groundparticles)

if __name__=='__main__':
    with tables.open_file(FILENAME, 'r') as data:
        with tables.open_file('gammas.h5', 'w') as gammas:
            with tables.open_file('leptons.h5', 'w') as leptons:

                table = data.root.groundparticles



                n_gammas = len(data.root.groundparticles)
                n_leptons = len(data.root.groundparticles) / 10

                print "gammas."
                copy_rows(table, gammas, 'particle_id==1', n_gammas)

                print "leptons."
                copy_rows(table, leptons, '(particle_id >= 2) & (particle_id <= 6)', n_leptons)

                # copy hdf5 attr
                data.copy_node_attrs('/', leptons.get_node('/'))
                data.copy_node_attrs('/', gammas.get_node('/'))
                print "Don't forget to ptrepack --sortby x --propindexes"
