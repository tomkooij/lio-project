# s501_delta_t.py
# Maak t1-t2 histogram voor timewalk.tex

import tables
import sapphire

import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

INPUTFILE = 'dt_s501_jan_mei_2014.csv'


if __name__ == '__main__':

    read_dt = []
    read_ph2 = []
    # lees csv
    with open(INPUTFILE, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            read_dt.append(float(row[0]))
            read_ph2.append(float(row[2]))

    print "number of events: ", len(read_dt)
    # convert to numpy
    selected_dt = np.array(read_dt)
    selected_ph2 = np.array(read_ph2)

    bins2ns5 = np.arange(-50.25,50.26,2.5)

    plt.figure()
    plt.hist(selected_dt, bins=bins2ns5, histtype='step')
    plt.xlabel('t1 - t2 [ns]')
    plt.ylabel('counts')
    plt.savefig('fig_delta_t.png', dpi=200)
    plt.show()
