import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import tables
from sapphire import Station
import random
import os

PLOT_TRACES = False   # download en plot traces
TXTOUTFILE = 's102_1laag_2hoog.txt'
FILENAME = 's102_heel2015.h5'

MIP = 150 / 0.57  # ADC =  mV/0.57
LOW_PH = 0.5*MIP
HIGH_PH = 1.*MIP


def plot_trace(station_id, ext_timestamp, t1, t2, start=625, end=1250):

    timestamp = int(str(ext_timestamp)[0:10])
    nanosec = int(str(ext_timestamp)[10:])

    print "DL traces: ", station_id, timestamp, nanosec,
    traces = Station(station_id).event_trace(timestamp, nanosec)
    print "Done."

    t = np.arange(0, len(traces[0])*2.5, 2.5)

    plt.figure()
    plt.xlim(start,end)
    plt.plot(t, traces[0])
    plt.plot(t, traces[1])
    plt.ylabel('ph [ADC]')
    plt.xlabel('t [ns]')
    plt.title('event %s_%s t1=%.1f, t2=%.1f' % (timestamp, nanosec, t1, t2))
    plt.savefig('trace%s.png' % ext_timestamp)
    plt.show()
    return traces

if __name__ == '__main__':

    if 'data' not in globals():
        data = tables.open_file(FILENAME, 'a')

    events = data.root.s102.events

    ext_stamp = events.col('ext_timestamp')
    t1 = events.col('t1')
    t2 = events.col('t2')

    ph = events.col('pulseheights')
    ph1 = ph[:, 0]
    ph2 = ph[:, 1]

    bins2ns5 = np.arange(-251.25, 251.26, 5.)

    grafiek = plt.figure()

    # remove -1 and -999
    # select events based on pulseheight
    filter = (t1 >= 0) & (t2 >= 0) & (ph1 > 0) & (ph1 < LOW_PH) & (ph2 > HIGH_PH)
    t1_filtered = t1.compress(filter)
    t2_filtered = t2.compress(filter)
    ph1_filtered = ph1.compress(filter)
    ph2_filtered = ph2.compress(filter)
    timestamp_filtered = ext_stamp.compress(filter)

    dt = t1_filtered - t2_filtered

    print "number of events in hoog/laag filter:", dt.size
    n1, bins1, blaat1 = plt.hist(dt, bins=bins2ns5, histtype='step')
    plt.title('s102, jan-okt 2015, t1-t2 (ph1=hoog, ph2=laag)')
    plt.savefig('t1t2histogram.png', dpi=200)
    plt.show()

    plt.figure()
    plt.hist2d(t1_filtered ,t2_filtered, bins=40, norm=LogNorm())
    plt.colorbar()
    plt.savefig('2dhist.png', dpi=200)
    plt.show()

    dt_filtered = t2_filtered - t1_filtered
    #selection = (t1_ > 1000) & (t2_ < 985)
    selection = (t1_filtered > 1000) & (t1_filtered < 1080) & (dt_filtered < -40) & (dt_filtered > -80)

    selected_stamps = timestamp_filtered.compress(selection)
    t1_selection = t1_filtered.compress(selection)
    t2_selection = t2_filtered.compress(selection)
    print "number of events in selection:", selected_stamps.size

    if (PLOT_TRACES):
        for i in range(10):
            # random.choice and np.random.choice does not work on uint64
            idx = random.randint(0, selected_stamps.size-1)
            event_timestamp = selected_stamps[idx]
            event_t1 = t1_selection[idx]
            event_t2 = t2_selection[idx]
            print i, event_timestamp
            traces = plot_trace(102, event_timestamp, event_t1, event_t2, 900, 1500)
