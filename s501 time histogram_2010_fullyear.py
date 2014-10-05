"""
Read data from station 501 and plot t1-t2 histogram

Goal: recreate graphs form D.Pennink 2010
t1-t2 from station 501, during April 2010

29sep: created
29sep: TODO consider dt = t1-t2; select events based on ph2 and/or ph2 (cp-gamma, gamma-cp and/or gamma-gamma) plot histogram and fit gaussian

ph1 > TRIGGER = charged particle
ph1 < TRIGGER = gamma

Find out value of TRIGGER (<120 and >200 ADC counts volgens LIO verslag)
Zelf uitgetest: sigma=9ns volgt bij HIGH_PH = 800.
PROBLEEM: Hoe hoger HIGH_PH hoe smaller de verdeling!!!!
"""

import tables
import sapphire.esd
import scipy.stats

from scipy.optimize import leastsq



STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2010,4,1)
END = datetime.datetime(2010,5,1)
FILENAME = 'station_501_2010_fullyear.h5'

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
t3 = events.col('t3')
t4 = events.col('t4')
ph = events.col('pulseheights')

ph1 = ph[:,0]
ph2 = ph[:,1]
ph3 = ph[:,2]
ph4 = ph[:,3]

#bins2ns5 = arange(-201.25,202.26,2.5)
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
grafiek = figure()
grafiek11 = grafiek.add_subplot(221)
grafiek12 = grafiek.add_subplot(222)
grafiek21 = grafiek.add_subplot(223)
grafiek22 = grafiek.add_subplot(224)

#
# Plot histogram for t1-t2 using event selection based on pulseheight
# 
#
dt = t1 - t2

# remove -1 and -999
# select events based on pulseheight
dt1 = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 < LOW_PH) & (ph2 > HIGH_PH))
grafiek11.hist(dt1, bins=bins2ns5)
grafiek11.set_title("ph1 < 120, ph2 > 200")

dt2 = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH) & (ph2 < LOW_PH))
grafiek12.hist(dt2, bins=bins2ns5)
grafiek12.set_title("ph1 > 200, ph2 < 120")


print "Figure 21\n"
dt3 = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 < LOW_PH) & (ph2 < LOW_PH))
plot_histogram_with_gaussfit(dt3, bins2ns5, bins2ns5_midden, grafiek21, "ph1,ph2<120")

print "Figure 22\n"
dt4 = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH) & (ph2 > HIGH_PH))
plot_histogram_with_gaussfit(dt4,bins2ns5, bins2ns5_midden, grafiek22, "ph1,ph2>200")

# Adjust x-axes, has to be done after plotting
grafiek11.set_xlim([-50,50])
grafiek12.set_xlim([-50,50])
grafiek22.set_xlim([-50,50])
grafiek21.set_xlim([-50,50])


show()

data.close()
