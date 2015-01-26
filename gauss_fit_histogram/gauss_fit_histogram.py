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
#
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def gauss_fit_histogram(histogram_y, bins, sigma_list):
    """
    Fit a histogram with a gaussian distribution

    Can fit non-normalised histogram with vertical "noise" offsets
    Fit = a*np.exp(-0.5*((x-b)/c)**2)+d

    :param histogram_y: a list with histogram data
    :param bins: list with bin-edges [left, left, ... , right]
    :sigma_list: list with standard deviation sigma per bin
    """

    #
    # De normale (gauss) verdeling
    #
    fit_func  = lambda x,a,b,c,d : a*np.exp(-0.5*((x-b)/c)**2)+d

    #
    # Middens van de bins:
    #
    middle = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]

    # Least squares: scipy.optimize.curve_fit:
    c, cov = curve_fit(fit_func, middle, n, sigma=sigma_list, absolute_sigma=True)

    print "exp[-0.5((x-mu)/sigma)^2]"
    print "Fit Coefficients:"
    print c[0],c[1],abs(c[2]),c[3]
    print "Co-variance matrix:"
    print cov

    fit =  fit_func(middle, c[0], c[1], abs(c[2]), c[3])

    # cov[0][0] is de spreiding^2 op de eerste fit parameter.
    # In dit geval is dat de spreiding op de schaal/normalisatie faktor
    # is dat is de juiste?

    chi2 = sum(np.power((n - fit)/sigma_list,2)) / (len(n) - len(c))
    print "Reduced Chi-squared: ", chi2

    pearsson = sum(np.power((n - fit),2)/fit) / (len(n) - len(c))
    print 'Reduced Pearsons Chi-squared: ', pearsson

    return c, middle, fit

if __name__=='__main__':
    # random data
    mu, sigma = 5., 10. # mean and standard deviation
    dataset = np.random.normal(mu, sigma, 5000)

    #
    # Bins die passen bij de 2.5ns timing van HiSPARC kastjes
    #
    bins_edges = np.arange(-21.25,21.25,1)

    # Maak een histogram
    #  n is nu een lijst met "counts"
    #  bins zijn de bin "randen"
    plt.figure()
    n,bins,patches = plt.hist(dataset,bins=bins_edges,histtype='step')

    #
    # sigma: standaard deviatie van de meetwaarden (=wortel(aantal per bin))
    #
    sigma_list = np.sqrt(n)

    c, fitx, fity = gauss_fit_histogram(n, bins, sigma_list)
    mu = c[1]
    simga = abs(c[2])

    plt.plot(fitx, fity ,'r--', linewidth=3)
    plt.title('gauss_fit_histogram.py');
    plt.xlabel('pulseheight [ADC]')
    plt.legend([r'fit: $ \mu = %.3f\  \sigma = %.3f\ $' %(mu, sigma), 'random data' ], loc = 2)
    plt.show()
