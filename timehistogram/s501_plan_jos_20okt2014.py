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
START = datetime.datetime(2014,4,1)
END = datetime.datetime(2014,4,8)
#FILENAME = 'station_501_1wk_april2014.h5'
FILENAME = 's501_filtered_2014.h5'
#FILENAME = 'station_501_augustus2014.h5'
#FILENAME = 'station_501_2010_fullyear.h5'
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
    print "Reading existing ESD datafile ", filename
    data = tables.open_file(FILENAME, 'r')
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

   # print "A exp[-0.5((x-mu)/sigma)^2]"
    print "Fit Coefficients:"
    print c[0],c[1],abs(c[2])
    return c

#
# Create a pylab (sub)plot with histogram and guassfit
#
# Usage:
#
# import matplotlib.pyplot as plt
# grafiek = pl((ph1<=LOW_PH) & (ph2>=HIGH_PH) & (ph3 <= LOW_PH) & (ph4 >= HIGH_PH))t.figure()
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

    title += str(" (s= %2.1f ns)" % abs(c[2])) # add sigma to title
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

event_id = events.col('event_id')

ph1 = ph[:,0]
ph2 = ph[:,1]
ph3 = ph[:,2]
ph4 = ph[:,3]


#
# Create a lookup table for events that fit our primary selection criterium:
#    Two e's and two gamma's. Two pulseheight > 200 AND two pulseheights < 120
#
# for row in events:  #WAY too slow
#
_1_g = ((ph1 <= LOW_PH) & (ph1 > 0))
_2_g = ((ph2 <= LOW_PH) & (ph2 > 0))
_3_g = ((ph3 <= LOW_PH) & (ph3 > 0))
_4_g = ((ph4 <= LOW_PH) & (ph4 > 0))

mask_1_gamma = _1_g
mask_2_gamma = _2_g
mask_3_gamma = _3_g
mask_4_gamma = _4_g

_1_e = (ph1 >= HIGH_PH)
_2_e = (ph2 >= HIGH_PH)
_3_e = (ph3 >= HIGH_PH)
_4_e = (ph4 >= HIGH_PH)

mask_1_electron = _1_e
mask_2_electron = _2_e
mask_3_electron = _3_e
mask_4_electron = _4_e

mask_12 = _1_e & _2_e & _3_g & _4_g
mask_13 = _1_e & _2_g & _3_e & _4_g
mask_14 = _1_e & _2_g & _3_g & _4_e
mask_23 = _1_g & _2_e & _3_e & _4_g
mask_24 = _1_g & _2_e & _3_g & _4_e
mask_34 = _1_g & _2_g & _3_e & _4_e

"""
print "Selecting events"
print "Total number of events in dataset:",event_id.size

# selected_id_12 is a list of event_id that fit the criteria
# mask_id is a list "True, False, True, True" (mask) that is the same length as event_id.size
#  the mask is useful for compress() in a later stage
selected_id_12 = event_id.compress((ph1>=HIGH_PH) & (ph2>=HIGH_PH) & (ph3 <= LOW_PH) & (ph4 <= LOW_PH))
#mask_12 = ((ph1>=HIGH_PH) & (ph2>=HIGH_PH) & (ph3 <= LOW_PH) & (ph4 <= LOW_PH))
print "1 2 size: ", selected_id_12.size, mask_12.sum()

selected_id_13 = event_id.compress((ph1>=HIGH_PH) & (ph2<=LOW_PH) & (ph3 >= HIGH_PH) & (ph4 <= LOW_PH))
#mask_13 = ((ph1>=HIGH_PH) & (ph2<=LOW_PH) & (ph3 >= HIGH_PH) & (ph4 <= LOW_PH))
print "1 3 size: ", selected_id_13.size, mask_13.sum()

selected_id_14 = event_id.compress((ph1>=HIGH_PH) & (ph2<=LOW_PH) & (ph3 <= LOW_PH) & (ph4 >= HIGH_PH))
#mask_14 = ((ph1>=HIGH_PH) & (ph2<=LOW_PH) & (ph3 <= LOW_PH) & (ph4 >= HIGH_PH))
print "1 4 size: ", selected_id_14.size, mask_14.sum()

selected_id_23 = event_id.compress((ph1<=LOW_PH) & (ph2>=HIGH_PH) & (ph3 >= HIGH_PH) & (ph4 <= LOW_PH))
mask_23 = ((ph1<=LOW_PH) & (ph2>=HIGH_PH) & (ph3 >= HIGH_PH) & (ph4 <= LOW_PH))
print "2 3 size: ", selected_id_23.size, mask_23.sum()

selected_id_24 = event_id.compress((ph1<=LOW_PH) & (ph2>=HIGH_PH) & (ph3 <= LOW_PH) & (ph4 >= HIGH_PH))
mask_24 = ((ph1<=LOW_PH) & (ph2>=HIGH_PH) & (ph3 <= LOW_PH) & (ph4 >= HIGH_PH))
print "2 4 size: ", selected_id_24.size, mask_24.sum()

selected_id_34 = event_id.compress((ph1<=LOW_PH) & (ph2<=LOW_PH) & (ph3 >= HIGH_PH) & (ph4 >= HIGH_PH))
mask_34 = ((ph1<=LOW_PH) & (ph2<=LOW_PH) & (ph3 >= HIGH_PH) & (ph4 >= HIGH_PH))
print "3 4 size: ", selected_id_34.size, mask_34.sum()
"""

#
# Create a single mask that contains all events that fit the criteria above
#
above_noise_threshold = ((t1 != -999.) & (t2 != -999.) & (t3 != -999.) & (t4 != -999.))

mask = (mask_12 | mask_13 | mask_14 | mask_23 | mask_24 | mask_34) & above_noise_threshold

print "Total number of events in selection: ",mask.sum()






# middel detector (B) heeft electron



#
# gemengd dus electron-gamma of gamma-electron in A-A       (1-3, 1-4, 3-4) afstand 10 m
#
# Nu doe ik de scheve verdeling! mix is dus eigenlijk eg
#
t34_eg_AA = (t3 - t4).compress(mask_3_electron & mask_4_gamma & mask)
t13_eg_AA = (t1 - t3).compress(mask_1_electron & mask_3_gamma & mask)
t14_eg_AA = (t1 - t4).compress(mask_1_electron & mask_4_gamma & mask)
# gemengd in A-B
t12_eg_AB = (t1 - t2).compress(mask_1_electron & mask_2_gamma & mask)
t23_eg_AB = (t2 - t3).compress(mask_2_electron & mask_3_gamma & mask)
t24_eg_AB = (t2 - t4).compress(mask_2_electron & mask_4_gamma & mask)

#
# elektronen in A-A       (1-3, 1-4, 3-4) afstand 10 m
#
# electronen in A-A betekent B = gamma
t34_ee_AA = (t3 - t4).compress(mask_2_gamma & mask)
t13_ee_AA = (t1 - t3).compress(mask_2_gamma & mask)
t14_ee_AA = (t1 - t4).compress(mask_2_gamma & mask)

#
# gamma's in A-A betekent B = electron
#
t34_gg_AA = (t3 - t4).compress(mask_3_gamma & mask_4_gamma & mask)
t13_gg_AA = (t1 - t3).compress(mask_1_gamma & mask_3_gamma & mask)
t14_gg_AA = (t1 - t4).compress(mask_1_gamma & mask_4_gamma & mask)

#
# electronen in A-B
#
# mask_2_electron  = electron detected in detector 2 (B)
# mask_12 = electron in 1 and 2 but NOT in 3 and 4
#
t12_ee_AB = (t1 - t2).compress(mask_2_electron & mask_2_electron & (t1 > 0) & (t2 > 0))
t23_ee_AB = (t2 - t3).compress(mask_2_electron & mask_3_electron & (t2 > 0) & (t3 > 0))
t24_ee_AB = (t2 - t4).compress(mask_2_electron & mask_4_electron & (t2 > 0) & (t4 > 0))
#
#
# gamma's in A-B
#
# mask_2_electron  = electron detected in detector 2 (B)
# mask_12 = electron in 1 and 2 but NOT in 3 and 4
#
t12_gg_AB = (t1 - t2).compress(mask_2_gamma & mask_1_gamma & (t1 > 0) & (t2 > 0))
t23_gg_AB = (t2 - t3).compress(mask_2_gamma & mask_3_gamma & (t2 > 0) & (t3 > 0))
t24_gg_AB = (t2 - t4).compress(mask_2_gamma & mask_4_gamma & (t2 > 0) & (t4 > 0))
#






#bins2ns5 = arange(-201.25,202.26,2.5)dm
bins2ns5 = arange(-101.25,101.26,2.5)
bins2ns5_midden = arange(-100,100.1,2.5)

#
# Plot histograms
#
def plot_ee_AA():
    #
    # 4 subplots to recreate the figure from Pennink 2010
    #
    grafiek = figure()
    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal_ee_AA = np.concatenate((t34_ee_AA,t13_ee_AA,t14_ee_AA),axis=0)
    plot_histogram_with_gaussfit(t34_ee_AA,bins2ns5, bins2ns5_midden, grafiek11, "3-4 ee AA")
    plot_histogram_with_gaussfit(t13_ee_AA,bins2ns5, bins2ns5_midden, grafiek21, "1-3 ee AA")
    plot_histogram_with_gaussfit(t14_ee_AA,bins2ns5, bins2ns5_midden, grafiek12, "1-4 ee AA")
    plot_histogram_with_gaussfit(totaal_ee_AA,bins2ns5, bins2ns5_midden, grafiek22, "totaal")

def plot_gg_AA():
    grafiek = figure()
    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal_gg_AA = np.concatenate((t34_gg_AA,t13_gg_AA,t14_gg_AA),axis=0)
    plot_histogram_with_gaussfit(t34_gg_AA,bins2ns5, bins2ns5_midden, grafiek11, "3-4 gg AA")
    plot_histogram_with_gaussfit(t13_gg_AA,bins2ns5, bins2ns5_midden, grafiek21, "1-3 gg AA")
    plot_histogram_with_gaussfit(t14_gg_AA,bins2ns5, bins2ns5_midden, grafiek12, "1-4 gg AA")
    plot_histogram_with_gaussfit(totaal_gg_AA,bins2ns5, bins2ns5_midden, grafiek22, "totaal")



def plot_ee_AB():
    grafiek = figure()
    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal_ee_AB = np.concatenate((t12_ee_AB, t23_ee_AB, t24_ee_AB), axis=0)
    plot_histogram_with_gaussfit(t12_ee_AB,bins2ns5, bins2ns5_midden, grafiek11, "1-2 ee AB")
    plot_histogram_with_gaussfit(t23_ee_AB,bins2ns5, bins2ns5_midden, grafiek21, "2-3 ee AB")
    plot_histogram_with_gaussfit(t24_ee_AB,bins2ns5, bins2ns5_midden, grafiek12, "2-4 ee AB")
    plot_histogram_with_gaussfit(totaal_ee_AB,bins2ns5, bins2ns5_midden, grafiek22, "totaal")


def plot_gg_AB():
    grafiek = figure()

    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal_gg_AB = np.concatenate((t12_gg_AB, t23_gg_AB, t24_gg_AB), axis=0)
    plot_histogram_with_gaussfit(t12_gg_AB,bins2ns5, bins2ns5_midden, grafiek11, "1-2 gg AB")
    plot_histogram_with_gaussfit(t23_gg_AB,bins2ns5, bins2ns5_midden, grafiek21, "2-3 gg AB")
    plot_histogram_with_gaussfit(t24_gg_AB,bins2ns5, bins2ns5_midden, grafiek12, "2-4 gg AB")
    plot_histogram_with_gaussfit(totaal_gg_AB,bins2ns5, bins2ns5_midden, grafiek22, "totaal")



def plot_mix_AA():
    grafiek = figure()
    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal_mix_AA = np.concatenate((t34_mix_AA,t13_mix_AA,t14_mix_AA),axis=0)

    plot_histogram_with_gaussfit(t34_mix_AA,bins2ns5, bins2ns5_midden, grafiek11, "3-4 mix AA")
    plot_histogram_with_gaussfit(t13_mix_AA,bins2ns5, bins2ns5_midden, grafiek21, "1-3 mix AA")
    plot_histogram_with_gaussfit(t14_mix_AA,bins2ns5, bins2ns5_midden, grafiek12, "1-4 mix AA")
    plot_histogram_with_gaussfit(totaal_mix_AA,bins2ns5, bins2ns5_midden, grafiek22, "totaal")


def plot_mix_AB():
    grafiek = figure()
    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal_mix_AB = np.concatenate((t12_mix_AB, t23_mix_AB, t24_mix_AB), axis=0)

    plot_histogram_with_gaussfit(t12_mix_AB,bins2ns5, bins2ns5_midden, grafiek11, "1-2 mix AB")
    plot_histogram_with_gaussfit(t23_mix_AB,bins2ns5, bins2ns5_midden, grafiek21, "2-3 mix AB")
    plot_histogram_with_gaussfit(t24_mix_AB,bins2ns5, bins2ns5_midden, grafiek12, "2-4 mix AB")
    plot_histogram_with_gaussfit(totaal_mix_AB,bins2ns5, bins2ns5_midden, grafiek22, "totaal")

def plot_mix():
    plot_mix_AA()
    plot_mix_AB()

def plot_eg_AA():
    grafiek = figure()
    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal_eg_AA = np.concatenate((t34_eg_AA,t13_eg_AA,t14_eg_AA),axis=0)

    plot_histogram_with_gaussfit(t34_eg_AA,bins2ns5, bins2ns5_midden, grafiek11, "3-4 eg AA")
    plot_histogram_with_gaussfit(t13_eg_AA,bins2ns5, bins2ns5_midden, grafiek21, "1-3 eg AA")
    plot_histogram_with_gaussfit(t14_eg_AA,bins2ns5, bins2ns5_midden, grafiek12, "1-4 eg AA")
    plot_histogram_with_gaussfit(totaal_eg_AA,bins2ns5, bins2ns5_midden, grafiek22, "totaal")


def plot_eg_AB():
    grafiek = figure()
    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal_eg_AB = np.concatenate((t12_eg_AB, t23_eg_AB, t24_eg_AB), axis=0)

    plot_histogram_with_gaussfit(t12_eg_AB,bins2ns5, bins2ns5_midden, grafiek11, "1-2 eg AB")
    plot_histogram_with_gaussfit(t23_eg_AB,bins2ns5, bins2ns5_midden, grafiek21, "2-3 eg AB")
    plot_histogram_with_gaussfit(t24_eg_AB,bins2ns5, bins2ns5_midden, grafiek12, "2-4 eg AB")
    plot_histogram_with_gaussfit(totaal_eg_AB,bins2ns5, bins2ns5_midden, grafiek22, "totaal")

#
# Maak een grafiek met 4 subplots
#
# serie1, serie2, serie3 zijn lijsten met tijdsverschillen
#  de vierde plot is het totaal van de drie
#
def plot_4(serie1, serie2, serie3, titel):

    grafiek = figure()


    grafiek11 = grafiek.add_subplot(221)
    grafiek12 = grafiek.add_subplot(222)
    grafiek21 = grafiek.add_subplot(223)
    grafiek22 = grafiek.add_subplot(224)

    totaal = np.concatenate((serie1, serie2, serie3), axis=0)

    plot_histogram_with_gaussfit(serie1,bins2ns5, bins2ns5_midden, grafiek11, titel)
    plot_histogram_with_gaussfit(serie2,bins2ns5, bins2ns5_midden, grafiek21, titel)
    plot_histogram_with_gaussfit(serie3,bins2ns5, bins2ns5_midden, grafiek12, titel)
    plot_histogram_with_gaussfit(totaal,bins2ns5, bins2ns5_midden, grafiek22, "totaal")

def plot_eg():
    plot_eg_AA()
    plot_eg_AB()

def plot_ee():
    plot_ee_AA()
    plot_ee_AB()

def plot_gg():
    plot_gg_AA()
    plot_gg_AB()

def plot_AB():
    plot_gg_AB()
    plot_ee_AB()

def plot_AA():
    plot_ee_AA()
    plot_gg_AA()

#plot_AB()
#plot_AA()
plot_ee_AA()


#plot_4(t12_eg_AB, t23_eg_AB, t24_eg_AB, "eg AB")


"""
figure()
hist(t34_ee_AA, bins=bins2ns5)
hist(t13_ee_AA, bins=bins2ns5)
hist(t14_ee_AA, bins=bins2ns5)
figure()
hist(t34_gg_AA, bins=bins2ns5)
hist(t13_gg_AA, bins=bins2ns5)
hist(t14_gg_AA, bins=bins2ns5)
"""
