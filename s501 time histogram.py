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



filename = "gaussdata.csv"
#data     = loadtxt(filename,skiprows=1,delimiter=',')
#xdata    = data[:,0]
#ydata    = data[:,1]


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
def plot_dt_histogram(tA,tB,bins):
    dt = tA - tB
    
    # remove -1 and -999
    fixed_dt = dt.compress((tA >= 0) & (tB >= 0))

    hist(fixed_dt, bins=bins)


    return True

def fit_norm(tA,tB): 
    dt = tA - tB
    fixed_dt = dt.compress((tA>=0) & (tB>=0))
    (mu, sigma) = scipy.stats.norm.fit(fixed_dt)
#    print (mu, sigma)
    return (mu, sigma)
    


 
    
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

dt = t1 - t2       
#
# Plot histogram for t1-t2 using hardcoded event selection based on pulseheight
#    
    
# remove -1 and -999
# select events based on pulseheight    
fixed_dt = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 < LOW_PH) & (ph2 < LOW_PH))
print "number of events: %d" % len (fixed_dt)

#
# Plot pulseheight histogram (usefull for pulseheight limits)
#
#hist(ph1, bins = 200, log=True, histtype='step')
#figure()    


#
# Plot histogram
#
hist(fixed_dt, bins=bins2ns5)

#
# THIS IS BULLSHIT!!! We are guassfitting the data NOT THE HISTOGRAM
#
(mu, sigma) = scipy.stats.norm.fit(fixed_dt)
        
print "avg: %f, sigma: %f" % (mu,sigma**0.5)

#fitted_pdf = scipy.stats.norm.pdf(bins2ns5, mu, sigma)
#plot(bins2ns5, fitted_pdf)

#y = matplotlib.mlab.normpdf(bins2ns5, mu, sigma)
#plot(bins2ns5, y, 'r--', linewidth=2)
#plot(fit(bins2ns5)) 



ydata = histogram(fixed_dt, bins=bins2ns5)
#
# least squares fit of gaussian distribution 
#
fitfunc  = lambda p, x: p[0]*exp(-0.5*((x-p[1])/p[2])**2)
errfunc  = lambda p, x, y: (y - fitfunc(p, x))
init  = [1.0, 0.5, 0.5]

histogram_y = ydata[0]
histogram_x = bins2ns5_midden 

out   = leastsq( errfunc, init, args=(histogram_x, histogram_y))
c = out[0]

print "A exp[-0.5((x-mu)/sigma)^2]"
print "Fit Coefficients:"
print c[0],c[1],abs(c[2])


title(r'$A = %.3f\  \mu = %.3f\  \sigma = %.3f\ $' %(c[0],c[1],abs(c[2])));
plot(histogram_x, fitfunc(c, histogram_x))
#plot(histogram_x, histogram_y)
show()


#data.close()
