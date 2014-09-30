"""
Read data from station 501 and plot t1-t2 histogram

Goal: recreate graphs form D.Pennink 2010

29sep: created
29sep: TODO consider dt = t1-t2; select events based on ph2 and/or ph2 (cp-gamma, gamma-cp and/or gamma-gamma) plot histogram and fit gaussian

ph1 > TRIGGER = charged particle
ph1 < TRIGGER = gamma

Find out value of TRIGGER (<120 and >200 volgens LIO verslag)
"""

import tables
import sapphire.esd
import scipy.stats 

STATIONS = [501]
START = datetime.datetime(2014,8,1)
END = datetime.datetime(2014,9,1)
FILENAME = 'station_501_augustus2014.h5'

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
def open_existing_events_file(filename):
    data = tables.open_file(FILENAME, 'a')
    return data

#
def plot_dt_histogram(tA,tB,bins):
    dt = tA - tB
    
    # remove -1 and -999
    fixed_dt = dt.compress((tA >= 0) & (tB >= 0) & (ph1 < 120) & (ph2 < 120))

    hist(fixed_dt, bins=bins)


    return True

def fit_norm(tA,tB): 
    dt = tA - tB
    fixed_dt = dt.compress((tA>=0) & (tB>=0))
    (mu, sigma) = scipy.stats.norm.fit(fixed_dt)
#    print (mu, sigma)
    return (mu, sigma)
    



#
def plot_dt_histogram_ph(tA,tB):

    
    
    return True

   
    
data = open_existing_events_file(FILENAME)
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
    
bins2ns5 = arange(-101.25,101.26,2.5)
    
#
# Plot histogram for tA-tB using hardcoded event selection based on pulseheight
#
    
dt = t1 - t2    
    
# remove -1 and -999
# select events based on pulseheight    
fixed_dt = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 < 120) & (ph2 < 120))
print "number of events: %d" % len (fixed_dt)
    
hist(fixed_dt, bins=bins2ns5, normed=1)
(mu, sigma) = scipy.stats.norm.fit(fixed_dt)
        
print "avg: %f, sigma: %f" % (mu,sigma)

fitted_pdf = scipy.stats.norm.pdf(bins2ns5, mu, sigma)
plot(bins2ns5, fitted_pdf)

#data.close()
