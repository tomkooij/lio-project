#
# Maak een plot van geselecteerde events (dist < 0.1 radiaal van Maan)
#  plot t.o.v. maanhoogte
#
import tables
import numpy as np
import matplotlib.pyplot as plt
import ephem

YEAR = 2010
STATION = 501

COLUMNS = ['timestamp', 'separation', 'zenith', 'maan_zenith', 'azimuth', 'maan_azimuth']

from configuration import PATH

BASELINE = 1262304000   # datetime(2010,1,1).utc

def hours_since_timestamp(timestamp, base):
    """ return number of hours since baseline (timestamp)

    :param: timestamp = event unixtimestamp (int, float or np.array)
    :param: base = baseline unixtimestamp
    :return: number of minutes since baseline (integer or np.array)
    """

    return np.round((timestamp - base) / (3600.))

def moon_alt():
    SciencePark = ephem.Observer()
    SciencePark.lon = '4.95'
    SciencePark.lat = '52.35'
    SciencePark.date = ephem.date('2010/01/01')
    end = ephem.date('2011/01/01')

    alt = []

    moon = ephem.Moon(SciencePark)

    while SciencePark.date < end:
        moon.compute(SciencePark)
        #print a
        alt.append(np.degrees(moon.alt))
        SciencePark.date += .1

    return np.asarray(alt)
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

    h = hours_since_timestamp(t, BASELINE)

    m_alt = moon_alt()
