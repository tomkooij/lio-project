#
# Fit een histogram met een Gauss verdeling
#
# bron: http://stackoverflow.com/questions/7805552/
#
# Dit is een test file om een robuste manier voor het fitten van een histogram
#  met een Normale verdeling te regelen. norm.fit() bepaald simpelweg het gemiddelde
#  van de data en is dus niet bruikbaar. Ook heeft norm.fit() problemen met
#  niet genormaliseerde data
#
# Deze code leest een CSV met data in,
#  maakt een histogram
#  fit een willekeurige gauss verdeling met kleinste kwaderen (scipy.optimize.leastsq)
#  plot de verdeling in het histogram
# TODO: chi-kwadraten bereken
#
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

if __name__=='__main__':
    #
    # De normale (gauss) verdeling voor scipy.optimize.curve_fit
    #
    fit_func  = lambda x,a,b,c: a*np.exp(-0.5*((x-b)/c)**2)

    # random data
    mu, sigma = 5., 10. # mean and standard deviation
    dataset = np.random.normal(mu, sigma, 5000)

    #
    # Bins die passen bij de 2.5ns timing van HiSPARC kastjes
    #
    bins_edges = np.arange(-41.25,41.25,2.5)

    # Maak een histogram
    #  n is nu een lijst met "counts"
    #  bins zijn de bin "randen"
    plt.figure()
    n,bins,patches = plt.hist(dataset,bins=bins_edges,histtype='step')

    #
    # Middens van de bins:
    #
    middle = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]

    # Least squares: scipy.optimize.curve_fit:
    c, cov = curve_fit(fit_func, middle, n)

    print "exp[-0.5((x-mu)/sigma)^2]"
    print "Fit Coefficients:"
    print c[0],c[1],abs(c[2])
    print "Co-variance matrix:"
    print cov


    plt.plot(bins, fit_func(bins, c[0], c[1], abs(c[2])),'r--', linewidth=3)
    plt.title('gauss_fit_histogram.py');
    plt.xlabel('pulseheight [ADC]')
    plt.legend([r'fit: $ \mu = %.3f\  \sigma = %.3f\ $' %(c[1],abs(c[2])), 'random data' ], loc = 3)
    plt.show()

    expected = fit_func(middle,c[0], c[1], abs(c[2]))

    # cov[0][0] is de spreiding^2 op de eerste fit parameter.
    # In dit geval is dat de spreiding op de schaal/normalisatie faktor
    # is dat is de juiste?
    fit_sigma2 = cov[0][0]

    chi2 = sum(np.power((n - expected)/fit_sigma2,2) / (len(n) - len(c)))
    print "Reduced Chi-squared: ", chi2

    pearsson = sum(np.power((n - expected)/expected,2) / (len(n) - len(c)))
    print 'Reduced Pearsons Chi-squared: ', pearsson
