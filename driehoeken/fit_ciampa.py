import tables
import numpy as np
from sapphire import ReconstructESDCoincidences
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

FILENAME = 'oneyear_spa_coinc.h5'
FILENAME = 'test.h5'
STATIONS = [503, 504, 506]

class DirectionsOnly(ReconstructESDCoincidences):
    def reconstruct_and_store(self, station_numbers=None):
        """Shorthand function to reconstruct coincidences and store results"""

        self.prepare_output()
        self.get_station_timing_offsets()
        self.reconstruct_directions(station_numbers=station_numbers)
        #self.reconstruct_cores(station_numbers=station_numbers)
        self.store_reconstructions()


def CountReconstructedDirections(data):
    """
    Count the number of non-nan zenith angles
    return False on error
    """

    try:
        zenith = data.root.coincidences.reconstructions.col('zenith')
    except:
        return False

    return np.count_nonzero(~np.isnan(zenith))

def Iyono(x, A, B):
    """ Iyono 2007: zenith angle distribution """
    
    return A*np.sin(x)*np.exp(-B*((1/np.cos(x)) - 1))

def fit_zenith(zenith, nbins=10):
    """ 
    fit zenith distribution
    return "B" parameter and reduced Chi-squared error
    """

    zenith = zenith[zenith < 0.8]
    n, bins = np.histogram(zenith, bins=nbins)
    middle = (bins[:-1] + bins[1:])/2.
    sigma = np.sqrt(n)
    try:
        popt, pcov = curve_fit(Iyono, middle, n)
    except ValueError:
        return None, None

    n_fit = Iyono(middle, *popt)
    n_dof = len(n)-len(popt)
    reduced_chi_square = np.sum(np.power((n-n_fit)/sigma, 2))/n_dof

    return popt[1], reduced_chi_square

def plot_zenith(zenith, nbins=10):
    """ plot zenith histogram and plot fit """

    zenith = zenith[zenith < 0.8]
    plt.figure()
    n, bins, patches = plt.hist(zenith, bins=nbins, histtype='step', color='b')
    middle = (bins[:-1] + bins[1:])/2.
    sigma = np.sqrt(n)
    popt, pcov = curve_fit(Iyono, middle, n)
    plt.errorbar(middle, n, yerr=sigma, fmt='o',  color= 'b')
    x = np.linspace(0, 1., num=100)
    plt.plot(x,  Iyono(x, *popt), color='r')

    plt.title('Zenith angle distribution')
    plt.xlabel('zenith angle (rad)')
    plt.legend(['fit: B=%.2f' %(popt[1]),'counts'])
    plt.show()


if __name__ == '__main__':
    with tables.open_file(FILENAME, 'a') as data:
        if not CountReconstructedDirections(data): 
            rec = DirectionsOnly(data, overwrite=True)
            rec.reconstruct_and_store(STATIONS)

        zenith = data.root.coincidences.reconstructions.col('zenith')
        azimuth = data.root.coincidences.reconstructions.col('azimuth')
        zenith = zenith[~np.isnan(zenith)]
        azimuth = azimuth[~np.isnan(azimuth)]

    results = {}
    for nbins in range(5, 50): 
        results[nbins] = fit_zenith(zenith, nbins=nbins)
    #results = sorted(results.items(), key=lambda x: x[1][1])   
    nbins, vals = results.items()
    

