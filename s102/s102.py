import numpy as np
import matplotlib.pyplot as plt
import tables
from sapphire import Station
import random

FILENAME = 's102_heel2015.h5'

LOW_PH = 120
HIGH_PH = 200

def plot_trace(station_id, ext_timestamp, t1, t2):

    START = 250  # 625 ns
    END = 500  # 1250 ns

    timestamp = int(str(ext_timestamp)[0:10])
    nanosec = int(str(ext_timestamp)[10:])

    print "DL traces: ", station_id, timestamp, nanosec,
    traces = Station(station_id).event_trace(timestamp, nanosec)
    print "Done."

    t = np.arange(START*2.5, END*2.5, 2.5)

    plt.figure()
    plt.plot(t, traces[0][START:END])
    plt.plot(t, traces[1][START:END])
    plt.ylabel('ph [ADC]')
    plt.xlabel('t [ns]')
    plt.title('event %s_%s t1=%.1f, t2=%.1f' % (timestamp, nanosec, t1, t2))
    plt.savefig('trace%s.png' % ext_timestamp)
    #plt.show()
    return traces

if __name__=='__main__':

    if 'data' not in globals():
        data = tables.open_file(FILENAME, 'a')

    events = data.root.s102.events

    ext_stamp = events.col('ext_timestamp')
    t1 = events.col('t1')
    t2 = events.col('t2')

    ph = events.col('pulseheights')
    ph1 = ph[:,0]
    ph2 = ph[:,1]

    bins2ns5 = np.arange(-101.25,101.26,2.5)

    grafiek = plt.figure()

    # remove -1 and -999
    # select events based on pulseheight
    filter = (t1 >= 0) & (t2 >= 0) & (ph2 > 0) & (ph2 < LOW_PH) & (ph1 > HIGH_PH)
    dt = (t1-t2).compress(filter)
    t1_ = t1.compress(filter)
    t2_ = t2.compress(filter)
    stamps = ext_stamp.compress(filter)

    selection = (dt > 60) & (dt < 80)
    s40_60 = stamps.compress(selection)
    t1_selection = t1_.compress(selection)
    t2_selection = t2_.compress(selection)

    print "number of events in selection:", dt.size, s40_60.size
    n1, bins1, blaat1 = plt.hist(dt, bins=bins2ns5, histtype='step')
    plt.title('s102, jan-okt 2015, t1-t2 (ph1=hoog, ph2=laag)')
    plt.savefig('t1t2histogram.png', dpi=200)
    plt.show()

    for i in range(20):
        # random.choice and np.random.choice does not work on uint64
        idx = random.randint(0,s40_60.size-1)
        event_timestamp = s40_60[idx]
        event_t1 = t1_selection[idx]
        event_t2 = t2_selection[idx]
        print i, event_timestamp
        traces = plot_trace(102, event_timestamp, event_t1, event_t2)
