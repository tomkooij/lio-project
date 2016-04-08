# coding: utf-8
from __future__ import division
import tables
from sapphire.utils import pbar
from sapphire.corsika.store_corsika_data import (GroundParticles,
                                                 create_index)
from heapq import merge

FILENAME = 'corsika_unsorted.h5'
#FILENAME = 'huge_corsika_unsorted.h5'

TEMP = 'tempfile.h5'
DEST = 'sorted.h5'

BUFSIZE = 100000


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
    use mergesort: much faster than quicksort and heapsort for large chunks
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
    tablechunk = t.read(start=start, stop=stop)
    sort_table(tablechunk)
    table = write_table(out, 'table_%d' % idx, tablechunk)

    return iter_chunk(table)


with tables.open_file(FILENAME, 'r') as data, \
        tables.open_file(TEMP, 'w') as temp, \
        tables.open_file(DEST, 'w') as output:
    t = data.get_node('/groundparticles')
    nrows = len(t)
    print "nrows: ", nrows
    print "hdf5 chunksize, nrowsinbuf", t.chunkshape[0], t.nrowsinbuf
    # chunksize is 10 millions rows (350MB)
    chunk = int(1e7)

    print "chopping in %d chunks of %d rows" % (int(nrows / chunk) + 1, chunk)
    iterators = []
    for idx, start in pbar(enumerate(xrange(0, nrows, chunk)),
                           length=int(nrows / chunk)):
        iterators.append(create_temp_table(t, temp, idx, start, start + chunk))

    output_table = output.create_table('/', 'groundparticles',
                                       GroundParticles,
                                       expectedrows=int(1e9))
    rowbuf = output_table._get_container(BUFSIZE)
    idx = 0

    old, new = (-1e99, -1e99)
    print "merging: "
    for keyedrow in pbar(merge(*iterators), length=nrows):
        x, row = keyedrow

        if idx == BUFSIZE:
            output_table.append(rowbuf)
            output_table.flush()
            idx = 0

        values = row.fetch_all_fields()
        rowbuf[idx] = values
        idx += 1

        old, new = new, row['x']
        if new < old:
            print "FAIL: new, old: ", new, old
            print row
            break

    # store last lines in buffer
    output_table.append(rowbuf[0:idx])
    output_table.flush()

print "Adding CSIndex:"
with tables.open_file(DEST, 'a') as hdf5:
    create_index(hdf5, progress=True)
