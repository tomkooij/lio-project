#
# maak een histogram van mogelijke aankomsttijd verschillen voor alle zenith
#  en azimuth hoeken
#

from __future__ import division

import numpy as np
import progressbar as pb
import matplotlib.pyplot as plt
import gauss_fit_histogram

FOKKEMA = 2.5  # spreiding op een tijdmeting uit Fokkema2012 H4.
RESOLUTIE = FOKKEMA*np.sqrt(2)  # tijdverschil dus sigma * srt(2)

progress = pb.ProgressBar(widgets=[pb.Percentage(),pb.Bar(), pb.ETA()])
STAPPEN =  187

a = 10.  # m  Distance between detectors
c = 3.e-1  # m/ns speed of light

if __name__ == '__main__':

    dt_list = []

    if 1:
        for zenith in progress(np.arange(0,np.pi/4,np.pi/(2*STAPPEN))):

            # distributie van zenith hoeken

            # sin(theta)*cos^n(theta) , n = 6
            weging = 100.*np.sin(zenith)*(np.cos(zenith))**6.

            # Ciampa, 1998 => sin(x)*exp(C*sec(theta)-D)
            #  Ciampa -> C=4
            #weging = 10000*np.sin(zenith)*np.exp(-1.*(4./np.cos(zenith))-1)

            for azimuth in np.arange(0,2*np.pi,np.pi/(STAPPEN/2)):

                # tijdverschil behorende bij deze hoek combinatie (in ns)
                delta_t = a / c * np.sin(zenith)*np.cos(azimuth)

                # maak lijst met tijdsverschillen,
                # waarbij de tijdsverschillen met grote kans vaker voorkomen
                # en random "versmering" met sigma = 2.5ns
                for item in np.arange(0, weging, 1.):
                    dt_list.append((delta_t) + np.random.normal(0,RESOLUTIE))

    print "gem, stddev = ",np.mean(dt_list), np.std(dt_list)


    plt.figure()
    n1, bins1, blaat = plt.hist(dt_list, histtype='step', bins=np.arange(-30,30,1.))

    sigma_list = np.sqrt(dt_list)
    c, fitx, fity = gauss_fit_histogram.gauss_fit_histogram(n1, bins1, sigma=np.sqrt(n1))
    mu = c[1]
    sigma = abs(c[2])
    print "fitted mu, sigma =", mu, sigma

    plt.plot(fitx, fity ,'r--', linewidth=3)
    plt.title('gesimuleerde dt verdeling. N = %.1e (..dt-schatting/dt.py)' % float(len(dt_list)))
    plt.xlabel('dt [ns]')
    plt.legend([r'fit: $ \mu = %.1f\  \sigma = %.1f\ $' %(mu, sigma), 'dt' ],loc=3)
    plt.savefig('dt-schatting.png', dpi=200)
    plt.show()
