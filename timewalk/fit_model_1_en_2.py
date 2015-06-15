# fit.py - time-walk fit functies bij data
#
# Plan Jos 5 en 7 januari 2015
# onderzoek correlatie tussen delta-t tegen pulshoogte
#
# zie /mailjos/ voor de mail en plaatjes van Jos
#
# Deze file leest "data.txt" (output van walk.py) en is / wordt gebruikt om functies te fitten



import tables
import sapphire

import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq

if __name__=='__main__':


    # load analysis from walk.py
    fit_bins, mu_list = np.loadtxt('data.txt')
    print "list of averages: \n",mu_list

    # time-walk correction function
    # fit c/sqrt(x)
    #  c een constante is per PMT verschillend
    #   x is eigenlijk de lading van de PMT (q, Q) hier nemen we pulshoogte
    # Ref: Brown et al, Nucl.Instrum.Meth. A221 (1984) 503
    #
    # De fit is matig. Beter is:
    # w1+w2/sqrt(x)
    # Ref: Smith, Nasseripour, Systematic Study of time walk corrections for the TOF counters, CLAS NOTE 2002-007.
    # t = 0 at 20 ADC counts -> fit = w1 + w2 / sqrt(x-20)
    #
    # op logschaal punten niet op een rechte! Het is geen pure exponentiele functie.
    # daarom gefit met exponent EN verschuiving. Is dat het lineaire deel uit CLAS NOTE 2002-007?
    fitfunc1 = lambda p,x: p[0]+p[1]/np.sqrt(x - 20.)
    errfunc1  = lambda p, x, y: (y - fitfunc1(p, x))
    fitfunc2  = lambda p, x: p[0]+p[1]/(x - 20.)**p[2]
    errfunc2  = lambda p, x, y: (y - fitfunc2(p, x))

    #
    # calculate middle of bins for fitting and plotting
    #
    # loaded from 'data.txt'
    #fit_bins = np.array([(s[0]+s[1])/2. for s in selection])

    mu = -1*np.array(mu_list) # all values positive for logscale

    # leastsquares fit
    init = [1.,10.]
    model1 = leastsq(errfunc1, init, args=(fit_bins, mu))
    print "fit1: ",model1

    init = [5.,1.,1.]
    model2 = leastsq(errfunc2, init, args=(fit_bins, mu))
    print "fit2: ",model2


    # plot and plot fit

    plt.figure()
    plt.plot(fit_bins, mu, 'bo')
    #    plt.errorbar(fit_bins,  mu_list, yerr=sigma_list, fmt='bo')
    plt.grid(b=True, which='major', color='b', linestyle='-')
    plt.xlabel('Pulshoogte [ADC]')
    plt.ylabel(r' < $\Delta t$ > [ns]')
    #plt.yscale('log')

    fit1 = model1[0]
    fit2 = model2[0]

    print "fit1: ", fit1
    print "fit2: ", fit2
    plt.plot(np.arange(20,120,1), fitfunc1(fit1, np.arange(20,120,1)),'c--', linewidth=2)
    plt.plot(np.arange(20,120,1), fitfunc2(fit2, np.arange(20,120,1)),'r--', linewidth=2)

    plt.title('Time walk, s501 t1-t2, jan-mei 2014 (n=77k)' )
    plt.legend(['gemiddelde per bin','model 1: t = %2.2f + %2.2f / sqrt (x-20))' % (fit1[0], fit1[1]),
    'model 2: t = %2.3f + %2.3f /(x-20.)^%2.3f  ' % (fit2[0], fit2[1], fit2[2])])
    plt.xlim((0,120))
    plt.savefig('time_walk_model_1_en_2.png',dpi=200)
    plt.show()
