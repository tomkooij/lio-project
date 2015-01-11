# walk -- ESD lees event, selecteer een schrijf naar CSV
# De CSV wordt ingelezen in walk.py

import tables
import numpy as np
import csv

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2014,4,1)
END = datetime.datetime(2014,6,1)
#FILENAME = 'station_501_april2010.h5'
#FILENAME = 's501_filtered_2014.h5'
FILENAME = 's501_apr_mei.h5'


#
# Pennink, 2010 p32 specifies these cutoff ADC counts
# >200 ADC count = charged particle
# <120 ADC counts = gamma
# These values are consistent with a pulseheight histogram
#
HIGH_PH = 200
LOW_PH = 120

#
# Read event data from the ESD
#  store in table `/sSTATION' for example: /s501
#
def create_new_event_file(filename, stations, start, end):

    print   "creating file: ",filename
    data = tables.open_file(filename,'w')

    print "reading from the ESD"
    for station in stations:
        print "Now reading station %d" % station
        sapphire.esd.download_data(data, '/s%d' % station, station, start, end)

    return data


if __name__=='__main__':
    if 'data' not in globals():
        data = tables.open_file(FILENAME, 'a')

    if '/s501/events' not in data:
        data.close()
        data = create_new_event_file(FILENAME, STATIONS, START, END)

    events = data.root.s501.events

    t1 = events.col('t1')
    t2 = events.col('t2')
    t3 = events.col('t3')
    t4 = events.col('t4')
    ph = events.col('pulseheights')

    ph1 = ph[:,0]
    ph2 = ph[:,1]
    ph3 = ph[:,2]
    ph4 = ph[:,3]

    bins2ns5 = np.arange(-101.25,101.26,2.5)
    bins2ns5_midden = np.arange(-100,100.1,2.5)

    dt = t1 - t2

    # remove -1 and -999
    # select events based on pulseheight t1 HIGH t2 LOW
    selected_dt = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH) & (ph1 < 2*HIGH_PH) & (ph2 < LOW_PH) & (ph1>20) & (ph1>20) & (abs(t1-t2) < 100))
    selected_ph1 = ph1.compress((t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH) & (ph1 < 2*HIGH_PH) & (ph2 < LOW_PH) & (ph1>20) & (ph1>20)& (abs(t1-t2) < 100))
    selected_ph2 = ph2.compress((t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH)& (ph1 < 2*HIGH_PH) & (ph2 < LOW_PH) & (ph1>20) & (ph1>20)& (abs(t1-t2) < 100))

    print "number of events", selected_dt.size

    #maak datafile CSV --> input voor walk.py
    with open('dt_s501_aprmei_2014.csv', 'w') as csvfile:
        lijst = csv.writer(csvfile, dialect='excel')
        for k in range(len(selected_dt)):
            lijst.writerow([selected_dt[k], selected_ph1[k], selected_ph2[k]])
