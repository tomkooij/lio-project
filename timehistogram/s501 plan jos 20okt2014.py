"""
Plan van Jos Steiger: 




Tom,

je zou 4 stations kunnen kiezen: 2 'standaard stations'
(niet 507 -staat binnen-, niet 502 en 508 -diamant vorm-
en niet 505 -een vierkant-) en 2 diamant-vormige (502 en 508).
Beide soorten hebben twee verschillende posities:
standaard: A (een hoekpunt) en B (het zwaartepunt)

     A                1


     B                2

A         A      3         4

en (voor de diamanten)  A (de korte diagnaal) en B (de lange)

         A

   B           B

         A

Let op door situaties met kabels (of onoplettendheid) zijn de detectors
nummers in 502 en 508 verschillend:

502:        1          508:        1

      4           2          3           2

            3                      4          (dus 3 en 4 verwisseld)

Kies nu events met twee elektronen en twee gamma's.
Met 4 detektoren kun je 6 paren maken (de volgorde in een paar maakt niet uit
m.a.w. paar 1-2 is hetzelfde als paar 2-1)

Dus voor het standaard station:

elektronen in A-A       (1-3, 1-4, 3-4) afstand 10 m
gamma's in A-A          (1-3, 1-4, 3-4)
elektronen in A-B       (1-2, 3-2, 4-2) afstand 5.8 m
gamma's in A-B          (1-2, 3-2, 4-2)
gemengd in A-A          (1-3, 1-4, 3-4) afstand 10 m
gemengd in A-B          (1-2, 3-2, 4-2) afstand 5.8 m

en voor de diamanten station 502 (voor 508 verwissel 3 en 4):

elektronen in A-A       (1-3) afstand 10 m
gamma's in A-A          (1-3) elektronen in B-B (2-4) afstand 17 m
gamma's in B-B          (2-4) elektronen in A-B (1-2, 1-4, 3-2, 3-4) afstand 10 m
gamma's in A-B          (1-2, 1-4, 3-2, 3-4)
gemengd in A-A          (1-3) afstand 10 m
gemengd in B-B          (2-4) afstand 17 m
gemengd in A-B          (1-2, 1-4, 3-2, 3-4) afstand 10 m

totaal 18 stellen (6 paren, 3 soorten: e-e, g-g, e-g) per station, en
dus 72 metingen in 4 stations

Je krijgt dan resultaten voor

        5.8m    10m     17m     tot
e-e     6       16      2       24
g-g     6       16      2       24
e-g     6       16      2       24
totaal                          72

m.a.w.eveveel data (elk 33%) voor e-e, e-g en g-g paren, en 67% van de data
voor een aftand van 10m, 25% voor een afstand van 5.8m en 8% voor 17m.
Voor elk soort paren zijn 6, 16 en 2 onafhankelijke meting per afstand
(rep. 5.8, 10 en 17m) beschikbaar voor systematische studies.

Zou een dergelijke keuze gemaakt kunnen worden met bijv 1 jaar data (508 heeft
maar ongeveer 1 jaar)?

Wat dacht je van zo'n verdeling? 3 afstanden, enige redundantie om
systematische studies te faciliteren, niet al te verschillende stations

ph1 > TRIGGER = charged particle
ph1 < TRIGGER = gamma

"""

import tables
import sapphire.esd
import scipy.stats

from scipy.optimize import leastsq



STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2010,4,1)
END = datetime.datetime(2010,5,1)
FILENAME = 'station_501_2010_april.h5'

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
grafiek = figure()

#
# Plot histogram for t1-t2 using event selection based on pulseheight
# 
#
dt = t1 - t2

# remove -1 and -999
# select events based on pulseheight
dt1 = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 < LOW_PH) & (ph2 < HIGH_PH))
print "number of events", dt1.size
hist(dt1, bins=bins2ns5)
