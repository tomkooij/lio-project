# walk.py - time-walk
#
# Plan Jos 5 en 7 januari 2015
# onderzoek correlatie tussen delta-t tegen pulshoogte
#
# zie /mailjos/ voor de mail en plaatjes van Jos
#
# Deze file maakt csv-files met "t1-t2, ph1, ph2" voor events waarbij plaat 1 = HOOG (>200 ADC) en plaat 2 = LAAG (<120 ADC)
# Ik heb van Oktober 2014 (station 501) een datafiles gemaakt "events_voor_jos.csv" waar de plaatjes van Josst uit de mail
# mee gemaakt zijn.
# Deze file kan die plaatjes namaken.
#
# (read_ESD.py) Van Jan-Mei zijn de events van s501 gedownload en in een CSV (dt_s501_jan_mei_2014.csv) opgeslagen
# deze file leest de CSV en maakt:
#   in bins (20-25, 25-30, 30-40, 40-50 enzo) histogrammen van delta-t
#   fit een normale verdeling voor elke histogram
#   maakt een plot van de gemiddelde dt versus pulshoogte
#   fit w1 + w2/sqrt(pulshoogte)
#
# fit.py curvefitting verplaatst naar fit.py


import tables
import sapphire

import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chisquare

#INPUTFILE = 'events_voor_jos.csv'
INPUTFILE = 'dt_output.csv'
OUTPUTFILE = 'data.txt'

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
#
# De normale (gauss) verdeling voor scipy.optimize.leastsq
#
fit_func  = lambda x,a,b,c: a*np.exp(-0.5*((x-b)/c)**2)

def gauss_fit_histogram(histogram_y, histogram_x):
    # Least squares fit:
    init  = [50.0, -5., 10.]

    #sigma_list = np.sqrt(histogram_y) # sqrt(n) = sigma
    sigma_list = np.sqrt(histogram_y)
    sigma_list[sigma_list == 0] = max(sigma_list)
    print "sigma_list", sigma_list

    c, cov = curve_fit(fit_func, histogram_x, histogram_y, sigma=sigma_list, absolute_sigma=True)

    print "A exp[-0.5((x-mu)/sigma)^2]"
    print "Fit Coefficients:"
    print c[0],c[1],abs(c[2])

    expected = fit_func(histogram_x, c[0], c[1], abs(c[2]))
    chi2 = sum(np.power((histogram_y - expected)/sigma_list, 2)) / (len(histogram_y) - len(c))
    print "Reduced Chi-squared: ", chi2

    pearsson = sum(np.power((histogram_y - expected)/expected,2)) / (len(histogram_y) - len(c))
    print 'Reduced Pearsons Chi-squared: ', pearsson

    return c, chi2




def main():
    read_dt = []
    read_ph2 = []
    # lees csv
    print "walk.py - inputfile: ", INPUTFILE
    with open(INPUTFILE, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            read_dt.append(float(row[0]))
            read_ph2.append(float(row[2]))

    print "number of events: ", len(read_dt)
    # convert to numpy
    selected_dt = np.array(read_dt)
    selected_ph2 = np.array(read_ph2)

    bins2ns5 = np.arange(-101.25,101.26,2.5)
    bins2ns5_midden = np.arange(-100,100.1,2.5)

    plt.figure()
    plt.hist(selected_dt, bins=bins2ns5)
    plt.show()


    # uit de mail van josst 7jan2015
    """wat ik heb gedaan:

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
    # bins van jos
    selection = [ [20,25], [25,30], [30,40], [40,50], [50,60], [60,70],[70,80], [80,90], [90,100], [100,110], [110,120]]

#left_bin = np.arange(20.,120, 2.5)
#    selection = [ [k,k+2.5] for k in left_bin]

    middle_of_selection = [(s[0]+s[1])/2. for s in selection]

    # Jos: -40 tot -20, rekeninghoudende met stapgrootte 2.5ns
    bins_edges = np.arange(-41.25,21.25,2.5)
    bins_middle = np.arange(-40,20,2.5)
    chi2_list = []

    # sla de analyse over als de data al in geheugen staat.
    if 'mu_list' not in globals():
        print "First run. Doing analysis."
        # bepaal de gemiddelde t_walk per bin
        global mu_list
        mu_list = []
        sigma_list = []

        for r in selection:
          t_ph = selected_dt.compress((selected_ph2 > r[0]) & (selected_ph2 <= r[1]) & (selected_dt >= -40.) & (selected_dt <= 20.) )
          plt.figure()
          n, bins, troep = plt.hist(t_ph,bins=bins_edges, histtype='step')
          plt.xlabel('delta-t [ns]')

          # fit a gaussian (see lio_project/gauss_fit_histogram/)
          c, chi2 = gauss_fit_histogram(n, bins_middle)
          chi2_list.append(chi2)

          mu = c[1]
          sigma = abs(c[2])

          # stor fitted mu, sigma
          mu_list.append(mu)
          sigma_list.append(sigma)

          # plot the fit
          plt.plot(bins, fit_func(bins, c[0], mu, sigma),'r--', linewidth=3)

          # state the ph selection and fitted mu, sigma in title
          plt.title(r'%2.1f < ph <= %2.1f fit: $\ \mu = %2.2f\ \sigma = %2.1f$' % (r[0],r[1],mu, sigma))

          plt.show()


    print "list of averages: \n",mu_list
    print "std deviations avg: ", np.mean(sigma_list), np.std(sigma_list)
    print "chi2:", chi2_list
    print "chi2-mean:", np.mean(chi2_list), np.std(chi2_list)
    # save data.txt for analysis
    np.savetxt(OUTPUTFILE,[middle_of_selection, mu_list])
    print "walk.py - outputfile:", OUTPUTFILE

if __name__ == '__main__':
    main()
