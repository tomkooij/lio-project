import tables
import numpy as np
import matplotlib.pyplot as plt

YEAR = 2010
STATION = 501

COLUMNS = ['timestamp', 'separation', 'zenith', 'maan_zenith', 'azimuth', 'maan_azimuth']

from configuration import PATH

if __name__ == '__main__':

    assert(STATION==501, 'reconstruct_and_store werkt alleen met 501...')

    all_separation = np.array([])

    # initialise results dictionairy
    results = {}
    for column in COLUMNS:
        results[column] = np.array([])

    # for reach results file --> store in results dict
    for month in range(1,13):
        print "maand: ", month,

        filename = PATH+"s501_"+str(YEAR)+"_"+str(month)+".h5"

        with tables.open_file(filename, 'r') as data:

            print "%s : Found %d events with direction reconstruction." % (filename, data.root.s501.maan.col('timestamp').size)
            for column in COLUMNS:
                results[column] = np.concatenate((results[column], data.root.s501.maan.col(column)))

    print "results is a dict of np.arrays with all the data!"

    t = results['timestamp'].compress(results['separation']<0.1)
    print "t = timestamps waarbij sep<0.1. >>>hist(t) en vergelijk met maan altitude!"
