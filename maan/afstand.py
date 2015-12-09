import tables
import numpy as np
import matplotlib.pyplot as plt

YEAR = 2010
STATION = 501

from configuration import PATH

if __name__ == '__main__':

    assert(STATION==501, 'reconstruct_and_store werkt alleen met 501...')

    dist = np.array([])

    for month in range(1,13):
        print "maand: ", month,

        filename = PATH+"s501_"+str(YEAR)+"_"+str(month)+".h5"

        with tables.open_file(filename, 'r') as data:

            sep = data.root.s501.maan.col('separation')
            print " Found %d reconstructions." % sep.size
            dist = np.concatenate((dist, sep))

    print "dist has all the data!"
