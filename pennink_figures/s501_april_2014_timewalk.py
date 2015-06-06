"""
Read data from station 501 and plot t1-t2 histogram

Goal: recreate graphs form D.Pennink 2010
t1-t2 from station 501, FULL YEAR 2010

ph1 > TRIGGER = charged particle
ph1 < TRIGGER = gamma

"""

import gauss_fit_histogram
import datetime
import tables
import sapphire.esd
import numpy as np
import matplotlib.pyplot as plt
import os.path

# width of histrogram (max time difference [ns])
HIST_WIDTH = 40.

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2014,4,1)
END = datetime.datetime(2014,5,1)
FILENAME = 'station_501_april2014.h5'

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

    print  "creating file: ",filename
    data = tables.open_file(filename,'w')

    print "reading from the ESD"
    for station in stations:
        print "Now reading station %d" % station
        sapphire.esd.download_data(data, '/s%d' % station, station, START, END)

    return data



if __name__=='__main__':

    if 'data' not in globals():
        print "%s not in memory yet " % FILENAME
        if os.path.exists(FILENAME):
            print "%s exists. Opening." % FILENAME
            data = tables.open_file(FILENAME, 'a')
        else:
            print "%s does not exist. Trying to read from ESD"
            data = create_new_event_file(FILENAME, STATIONS, START, END)
    else:
        print "data already in globals."

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

    bins2ns5 = np.arange(-HIST_WIDTH-1.25,HIST_WIDTH+1.26,2.5)

    dt_all = (t1-t2).compress( (t1 >0) & (t2 > 0) )
    dt_t1hoog_t2laag = (t1-t2).compress( (t1 >0) & (t2 > 0) & ( (t1-t2) < 60. ) & (ph1 > HIGH_PH) & (ph2 < LOW_PH) )
    dt_t2laag_t2hoog = (t1-t2).compress( (t1 >0) & (t2 > 0) & ( (t1-t2) < 60. ) & (ph2 > HIGH_PH) & (ph1 < LOW_PH) )
    dt_t2laag_t2laag = (t1-t2).compress( (t1 >0) & (t2 > 0) & (ph1 < LOW_PH) & (ph2 < LOW_PH))

    print "All events", dt_all.size
    n1, bins1, blaat1 = plt.hist(dt_all, bins=bins2ns5, histtype='step')

    sigma_list = np.sqrt(n1)

    c, fitx, fity = gauss_fit_histogram.gauss_fit_histogram(n1, bins1, sigma=sigma_list, initialguess = [100.,10., 10., 0.], verbose=True)
    mu = c[1]
    sigma = abs(c[2])

    plt.plot(fitx, fity ,'r--', linewidth=3)
    plt.title('%s t1-t2: ph1,ph2=hoog' % FILENAME)
    plt.xlabel('pulseheight [ADC]')
    plt.legend([r'fit: $ \mu = %.3f\  \sigma = %.3f\ $' %(mu, sigma), 't1-t2' ], loc = 2, bbox_to_anchor=(1,1))
    plt.show()

    print "ph1 hoog, ph2 laag", dt_t1hoog_t2laag.size
    n1, bins1, blaat1 = plt.hist(dt_t1hoog_t2laag, bins=bins2ns5, histtype='step')
    plt.title('t1-t2: ph1=hoog, ph2=laag')
    plt.show()

    print "ph1 laag, ph1 hoog", dt_t2laag_t2hoog.size
    n1, bins1, blaat1 = plt.hist(dt_t2laag_t2hoog, bins=bins2ns5, histtype='step')
    plt.title('t1-t2: ph1=laag, ph2=hoog')
    plt.show()

    print "ph2 laag, ph2 laag", dt_t2laag_t2laag.size
    n1, bins1, blaat1 = plt.hist(dt_t2laag_t2laag, bins=bins2ns5, histtype='step')

    sigma_list = np.sqrt(n1)

    c, fitx, fity = gauss_fit_histogram.gauss_fit_histogram(n1, bins1, sigma=sigma_list, initialguess = [100.,10., 10., 0.], verbose=True)
    mu = c[1]
    sigma = abs(c[2])

    plt.plot(fitx, fity ,'r--', linewidth=3)
    plt.title('%s t1-t2: ph1,ph2=laag' % FILENAME)
    plt.xlabel('pulseheight [ADC]')
    plt.legend([r'fit: $ \mu = %.3f\  \sigma = %.3f\ $' %(mu, sigma), 't1-t2' ], loc = 2, bbox_to_anchor=(1,1))
    plt.show()

    """
    Time walk correction
    """

    # time walk correction function
    # fit_clas_note_02_2007.py:
    t_walk = lambda x: -3.944 + 22.3 / (x-20.)**0.156

    t1_corr = t1 - t_walk(ph1)
    t2_corr = t2 - t_walk(ph2)
    dt_corr = (t1_corr-t2_corr).compress( (t1 >0) & (t2 > 0) & (ph1 < LOW_PH) & (ph2 < LOW_PH))

    n1, bins1, blaat1 = plt.hist(dt_corr, bins=bins2ns5, histtype='step')

    sigma_list = np.sqrt(n1)

    c, fitx, fity = gauss_fit_histogram.gauss_fit_histogram(n1, bins1, sigma=sigma_list, initialguess = [100.,10., 10., 0.], verbose=True)
    mu = c[1]
    sigma = abs(c[2])

    plt.plot(fitx, fity ,'r--', linewidth=3)
    plt.title('%s t1-t2: ph1,ph2=laag TIMEWALK' % FILENAME)
    plt.xlabel('pulseheight [ADC]')
    plt.legend([r'fit: $ \mu = %.3f\  \sigma = %.3f\ $' %(mu, sigma), 't1-t2' ], loc = 2, bbox_to_anchor=(1,1))
    plt.show()
