# print alle traces van de events uit FILENAME

import numpy as np
import matplotlib.pyplot as plt

from sapphire import Station
from sapphire.utils import pbar

FILENAME = 'li-sh-10km-0.0002work.csv'


def plot_trace(traces, sn, ts):
    plt.figure()
    for trace in traces:
        time = np.linspace(0, 2.5*(len(trace)-1), num=len(trace))
        plt.plot(time, trace)
    plt.title('Station %d(%d) at %d' % (sn, len(traces), ts))
    plt.xlabel('[ns]')
    plt.ylabel('ADC counts')
    plt.savefig('trace-ts%d-sn%d.png' % (ts, sn), dpi=200)
    plt.close()

bliksem_data = np.genfromtxt(FILENAME)
for bliksem in pbar(bliksem_data):
    sn, ts, ns = map(int, [bliksem[1], bliksem[3], bliksem[4]])

    #print('get trace: ', sn, ts, ns)
    s = Station(sn)
    trace = s.event_trace(ts, ns)
    plot_trace(trace, sn, ts)
