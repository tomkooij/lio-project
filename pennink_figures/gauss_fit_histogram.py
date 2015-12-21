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


def gauss_fit_histogram(n, bins, sigma=None, initialguess = [1., 1., 1., 0.], verbose=False):
    """
    Fit a histogram with a gaussian distribution

    Can fit non-normalised histogram with vertical "noise" offsets
    Fit = a*np.exp(-0.5*((x-b)/c)**2)+d

    Parameters
    ----------

    n: a list with histogram data
    bins: list with bin-edges [left, left, ... , right]
    sigma:  None or list with uncertaincies in the histrogram_y data
    initialguess : None initial guess

    Returns
    -------
    c : a list of parameters
    fitx, fity : two lists with (x,y) pairs of the fit for plotting
    verbose : Boolean: True prints fit info (parameters, co-variance matrix, chi2 )

    Example
    -------
    plt.figure()
    n,bins,patches = plt.hist(dataset,bins=bins_edges,histtype='step')
    c, fitx, fity = gauss_fit_histogram(n, bins, sigma=sigma_list)
    plt.plot(fitx, fity ,'r--', linewidth=3)
    plt.show()
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
    c, cov = curve_fit(fit_func, middle, n, p0=initialguess, sigma=sigma, absolute_sigma=True)

    if (verbose):
        print "exp[-0.5((x-mu)/sigma)^2]"
        print "Fit Coefficients:"
        print "A %.2f, mu %.2f,sigma %.2f, bg %.2f" % (c[0],c[1],abs(c[2]),c[3])
        #print "Co-variance matrix:"
        #print cov

    fit =  fit_func(middle, c[0], c[1], abs(c[2]), c[3])

    # cov[0][0] is de spreiding^2 op de eerste fit parameter.
    # In dit geval is dat de spreiding op de schaal/normalisatie faktor
    # is dat is de juiste?

    if (verbose):
        chi2 = sum(np.power((n - fit)/sigma,2)) / (len(n) - len(c))
        print "Reduced Chi-squared: ", chi2

        pearsson = sum(np.power((n - fit),2)/fit) / (len(n) - len(c))
        print 'Reduced Pearsons Chi-squared: ', pearsson

    return c, middle, fit

if __name__=='__main__':
    # random data
    dataset = np.random.normal(5., 10., 5000)

    # Maak een histogram
    #  n is nu een lijst met "counts"
    #  bins zijn de bin "randen"
    plt.figure()
    n,bins,patches = plt.hist(dataset,bins=np.arange(-20., 30., 1.),histtype='step')

    #
    # sigma: standaard deviatie van de meetwaarden (=wortel(aantal per bin))
    #
    sigma_list = np.sqrt(n)

    c, fitx, fity = gauss_fit_histogram(n, bins, sigma=sigma_list, verbose=True)
    mu = c[1]
    sigma = abs(c[2])

    fitx = middle
    fity = fit_func(fitx, c[0], c[1], abs(c[2]), c[3])


    plt.plot(fitx, fity ,'r--', linewidth=3)
    plt.title('gauss_fit_histogram.py');
    plt.xlabel('pulseheight [ADC]')
    plt.legend([r'fit: $ \mu = %.3f\  \sigma = %.3f\ $' %(mu, sigma), 'random data' ], loc = 2, bbox_to_anchor=(1,1))
    plt.show()
