# coding: utf-8
from __future__ import division
import tables
from sapphire.utils import pbar
from sapphire.corsika.store_corsika_data import GroundParticles
from collections import namedtuple
from heapq import merge

FILENAME = 'corsika_unsorted.h5'
FILENAME = 'huge_corsika_unsorted.h5'

TEMP = 'tempfile.h5'

def iter_chunk(table):
    """
    iter over sorted rows of particles
    return key first

    """
    for row in table.iterrows():
        yield row['x'], (row)


def sort_table(tablechunk):
    """
    sort the chunk by x
    alg = quicksort O(n^2), mergesort O(nlogn) is available
    TODO: check performance of mergesort
    TODO: is this just a "view" or an in place sort?
    """
    return tablechunk.sort(order='x', kind='mergesort')


def write_table(out_file, table_name, tablechunk):
    """
    write a chunk to a table
    """
    out_table = out_file.create_table('/', table_name, GroundParticles,
                          expectedrows=len(tablechunk))

    out_table.append(tablechunk)
    out_table.flush()

    return out_table


def create_temp_table(t, out, idx, start, stop):
    print "read...", idx
    tablechunk = t.read(start=start, stop=stop)
    print "sort...", idx
    sort_table(tablechunk)
    print " write...", idx
    table = write_table(out, 'table_%d' % idx, tablechunk)

    return iter_chunk(table)

with tables.open_file(FILENAME,'r') as data, \
        tables.open_file(TEMP, 'w') as out:
    t = data.get_node('/groundparticles')
    nrows = len(t)
    print "nrows: ", nrows
    print "hdf5 chunksize, nrowsinbuf", t.chunkshape[0], t.nrowsinbuf
    # chunksize is 10 millions rows (350MB)
    chunk = int(1e7)

    print "chopping in %d chunks of %d rows" % (int(nrows/chunk)+1, chunk)
    iterators = []
    for idx, start in pbar(enumerate(xrange(0, nrows, chunk)),
                           length=int(nrows/chunk)):
        iterators.append(create_temp_table(t, out, idx, start, start+chunk))

    old, new = (-1e99, -1e99)

    for idx, keyedrow in enumerate(merge(*iterators)):
        #print row['x']
        x, row = keyedrow

        old, new = new, row['x']
        if new < old:
            print "FAIL: line, new, old: ", idx, new, old
            print row
            break

        if not idx % 100000:
            print "line: ", idx, x

