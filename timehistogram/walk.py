# walk.py
#
# Plan Jos 5 januari 2015
# onderzoek correlatie tussen delta-t van cp versus gamma tegen pulshoogte
import tables
import sapphire

import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import matplotlib.mlab as mlab

from math import exp

from matplotlib.colors import LogNorm

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2014,11,1)
END = datetime.datetime(2014,12,1)
#FILENAME = 'station_501_april2010.h5'
#FILENAME = 's501_filtered_2014.h5'
FILENAME = 's501_oktober_214.h5'



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
        sapphire.esd.download_data(data, '/s%d' % station, station, start, end)

    return data


if __name__ == '__main__':
    if 'data' not in globals():
        data = tables.open_file(FILENAME, 'a')

    if '/s501/events' not in data:
		data.close()
		create_new_event_file(FILENAME, STATIONS, START, END)

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

    bins2ns5 = np.arange(-101.25,101.26,2.5)
    bins2ns5_midden = np.arange(-100,100.1,2.5)

    dt = t1 - t2

    # remove -1 and -999
    # select events based on pulseheight t1 HIGH t2 LOW
    selected_dt = dt.compress((t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH) & (ph1 < 2*HIGH_PH) & (ph2 < LOW_PH) & (ph1>20) & (ph1>20) & (abs(t1-t2) < 100))
    selected_ph1 = ph1.compress((t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH) & (ph1 < 2*HIGH_PH) & (ph2 < LOW_PH) & (ph1>20) & (ph1>20)& (abs(t1-t2) < 100))
    selected_ph2 = ph2.compress((t1 >= 0) & (t2 >= 0) & (ph1 > HIGH_PH)& (ph1 < 2*HIGH_PH) & (ph2 < LOW_PH) & (ph1>20) & (ph1>20)& (abs(t1-t2) < 100))

    print "number of events", selected_dt.size

    # maak datafile voor Josst (5 jan 2014)
    #with open('events_voor_jos.csv', 'w') as csvfile:
    #    lijst = csv.writer(csvfile, dialect='excel')
    #    for k in range(len(selected_dt)):
    #        lijst.writerow([selected_dt[k], selected_ph1[k], selected_ph2[k]])

    plt.figure()
    plt.hist(selected_dt, bins=bins2ns5)
    plt.show()

    #plt.figure()
    #plt.hist2d(selected_dt, selected_ph2,bins=30, norm=LogNorm())
    #plt.title('Walk: Delta-t between HIGH (plate 1) and LOW (plate 2)')
    #plt.xlabel('delta-t (ns)')
    #plt.ylabel('pulseheight plate 2')
    #plt.colorbar()
    #plt.savefig('correlatie ph en delta-t.png',dpi=200)
    #plt.show()


    # uit de mail van josst 7jan2015
    """at ik heb gedaan:

ik heb jouw file met dt, ph(low), en ph(high) data gebruikt, en plots
gemaakt van de t2-t1 verdeling met ph(low) in de volgende elf gebieden

20-25; 25-30; 30-40; 40-50; 50-60; 60-70; 70-80; 80-90; 90-100;
100-110; en 110-120

in ieder van die gebieden zie je een piek met een lage staart, die kleiner
wordt als de pulshoogte toeneemt. De piek wordt goed beschrevn door een
normaal verdeling. In alle elf gevallen wordt in hetzelfde gebied (-40 tot 20 ns) een normaalkurve gefit. Chikwadraten zijn gemiddeld 1.07534 met een
spreiding van 0.3563. Plaatje 1 showt de positie van de piek,plaatje 2 de
breedte ervan.
"""

    selection = [ [20,25], [25,30], [30,40], [40,50], [50,60], [60,70],
                    [70,80], [80,90], [90,100], [100,110], [110,120]]

    middle_of_selection = [(s[0]+s[1])/2. for s in selection]

    # Jos: -40 tot -20, rekeninghoudende met stapgrootte 2.5ns
    bins_edges = np.arange(-41.25,21.25,2.5)
    bins_middle = np.arange(-40,20,2.5)
    mu_list = []
    sigma_list = []

    for r in selection:
      t_ph = selected_dt.compress((selected_ph2 > r[0]) & (selected_ph2 <= r[1]) & (selected_dt >= -40.) & (selected_dt <= 20.) )
      plt.figure()
      n, bins, troep = plt.hist(t_ph,bins=bins_edges, histtype='step', normed=True)
      plt.title(str(r[0])+' < ph <= '+str(r[1]))
      plt.xlabel('delta-t [ns]')


      (mu, sigma) = norm.fit(t_ph)

      mu_list.append(mu) # save fitted mu, sigma
      sigma_list.append(sigma)

      y = mlab.normpdf( bins, mu, sigma)
      plt.plot(bins, y, 'r--', linewidth=2)

      plt.show()


    print mu_list

    plt.figure()
    plt.plot(middle_of_selection, mu_list, 'o')
    plt.show()

    #data.close()
