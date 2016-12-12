# print alle traces van de events uit FILENAME
import csv

import numpy as np
import matplotlib.pyplot as plt

from sapphire import Station
from sapphire.utils import pbar

FILENAME = 'dec12.csv'
# dec12.csv -> gemaakt met Reno o.b.v. 'coincidences_10km_120sec_bver7.txt'
#
# In excel zijn header en de eerste 371 regels verwijderd. 
# Daarna in excel: text->kolommen met spaties
# uit excel komt:
# 2994;/s22;(12670L,;1278789234;520638897L,;1278789234520638897L,;;;;;;;;;;;;


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


def get_station_from_group(s):
    """ '/s202' --> int(202) """
    return int(s.split('s')[1])


def fix(s):
    """ '520638897L,' --> int(520638897)"""
    return int(s[:-2])




with open(FILENAME, 'r') as f:
    csvfile = csv.reader(f, delimiter=';')
    bliksem_data = [(get_station_from_group(line[1]), int(line[3]),
                     fix(line[4])) for line in csvfile]


for bliksem in pbar(bliksem_data):
    sn, ts, ns = bliksem

    #print('get trace: ', sn, ts, ns)
    s = Station(sn)
    trace = s.event_trace(ts, ns)
    plot_trace(trace, sn, ts)
