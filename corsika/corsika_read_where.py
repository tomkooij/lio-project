# -*- coding: utf-8 -*-
"""
read_where() profiling

in sapphire.groundparticlesim:

query = ('(x >= %f) & (x <= %f) & (y >= %f) & (y <= %f)'
                 ' & (particle_id >= 2) & (particle_id <= 6)' %
                 (x - detector_boundary, x + detector_boundary,
                  y - detector_boundary, y + detector_boundary))
        return self.groundparticles.read_where(query)

This is SLOoooooww... Can it be optimised?

"""
import tables
import numpy as np


#FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 0
FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
#FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 22.5

data = tables.open_file(FILENAME, 'r')
gp = data.root.groundparticles

groundparticles = data.get_node('/groundparticles')

SCALE = 50 # scale of dataset

def test_query(N):
    coordinates = SCALE*np.random.randn(N,2)
    for x,y in coordinates:
        query_xy = '(x >= %f) & (x <= %f) & (y >= %f) & (y <= %f)' % (x,y,x+0.5,y+0.5)
        #query_x = '(x >= %f) & (x <= %f) ' % (x,x+0.5)
        selection = groundparticles.read_where(query_xy)
        print len(selection)

def test_query_compress(N):
    """ read_where query in y, compress for y selection """
    coordinates = SCALE*np.random.randn(N,2)
    for x,y in coordinates:
        query_y = '(y >= %f) & (y <= %f)' % (y,y+0.5)
        selection = groundparticles.read_where(query_y)
        sel = selection.compress((selection['x'] >= x) & (selection['x'] <= x+0.5))
        print len(selection)

def query_compress():
    """ read_where query in y, compress for y selection """
    coordinates = SCALE*np.random.randn(1,2)
    for x,y in coordinates:
        query_y = '(y >= %f) & (y <= %f)' % (y,y+0.5)
        return groundparticles.read_where(query_y)


if __name__=='__main__':
    print "profiel read_where()!"
    test_query_compress(10)
