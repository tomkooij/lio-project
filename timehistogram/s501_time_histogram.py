"""
Read data from station 501 and plot t1-t2 histogram

Goal: recreate graphs form D.Pennink 2010
t1-t2 from station 501, FULL YEAR 2010

ph1 > TRIGGER = charged particle
ph1 < TRIGGER = gamma

"""

import datetime
import tables
import sapphire.esd
import scipy.stats
from numpy import *
import matplotlib.pyplot as plt
from scipy.optimize import leastsq



STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2010,4,1)
END = datetime.datetime(2010,5,1)
FILENAME = 'station_501_april2010.h5'

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
        sapphire.esd.download_data(data, '/s%d' % station, station, START, END)

    return data

#
# Open existing coincidence table.
# Only check if "/coincidences" are in table, no other checks
def open_existing_event_file(filename):
    data = tables.open_file(FILENAME, 'a')
    return data

#
#
# Least squares fit of histogram data to guassian distribution
#   Includes y-scale factor, ignores y-offset
#
# Source: http://stackoverflow.com/a/15521359
#
# histogram_y = array of y data
# histogram_x = array of middle of bins
#
#
# least squares fit of gaussian distribution
#
fitfunc  = lambda p, x: p[0]*exp(-0.5*((x-p[1])/p[2])**2)
errfunc  = lambda p, x, y: (y - fitfunc(p, x))

def gauss_fit_histogram(histogram_y, histogram_x):


    init  = [1.0, 0.5, 0.5]

    out   = leastsq( errfunc, init, args=(histogram_x, histogram_y))
    c = out[0]

    print "A exp[-0.5((x-mu)/sigma)^2]"
    print "Fit Coefficients:"
    print c[0],c[1],abs(c[2])
    return c

#
# Create a pylab (sub)plot with histogram and guassfit
#
# Usage:
#
# import matplotlib.pyplot as plt
# grafiek = plt.figure()
# dt_data = [ ... datapoints ...]
# bins = arrange( )
# bins_middle = arrange()
# title = "Data histogram"
# plot_histogram_with_gaussfit(dt_data, bins, bins_middle, grafiek, title)
# plt.show()

def plot_histogram_with_gaussfit(dt_data, bins_edges, bins_middle, grafiek, title):

    print "Number of datapoints (events): %d" % dt_data.size
    grafiek.hist(dt_data, bins=bins_edges)

    #
    # Create histogram array
    #
    ydata = histogram(dt_data, bins=bins_edges)
    histogram_y = ydata[0]
    histogram_x = bins_middle
    c = gauss_fit_histogram(histogram_y, histogram_x)

    grafiek.set_title(title)
# dit moet eigenlijk relatief en geen absolute x,y coordinaten in de grafiek zijn
#    grafiek.text(-150,100,r'$\mu=100,\ \sigma=15$')
    grafiek.plot(histogram_x, fitfunc(c, histogram_x))





#data = create_new_event_file(FILENAME, STATIONS, START, END)
#data.close()
data = open_existing_event_file(FILENAME)

events = data.root.s501.events

t1 = events.col('t1')
t2 = events.col('t2')

ph = events.col('pulseheights')

ph1 = ph[:,0]
ph2 = ph[:,1]


#bins2ns5 = arange(-201.25,202.26,2.5)dm
bins2ns5 = arange(-101.25,101.26,2.5)
bins2ns5_midden = arange(-100,100.1,2.5)

#
# Plot pulseheight histogram (usefull for pulseheight limits)
#
#hist(ph1, bins = 200, log=True, histtype='step')
#figure()

#
# 4 subplots to recreate the figure from Pennink 2010
#
grafiek = plt.figure()

#
# Plot histogram for t1-t2 using event selection based on pulseheight
#
#
dt = t1 - t2

# remove -1 and -999
# select events based on pulseheight
dt1 = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 < LOW_PH) & (ph2 < HIGH_PH) ) # old
dt1 = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 < LOW_PH) & (ph2 < HIGH_PH) & (ph2 >0) & (ph1>0)) # new 

print "number of events", dt1.size
plt.hist(dt1, bins=bins2ns5)
plt.show()