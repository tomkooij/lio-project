import tables
import numpy as np
from sapphire import ReconstructESDCoincidences
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

FILENAME = 'zaanstad_102_104_105.h5'
STATIONS = [102, 104, 105]
#FILENAME = 'spa_501_504_506.h5'
#STATIONS = [501, 504, 506]
#FILENAME = 'adam_2_22_23.h5'
#STATIONS =  [2, 22, 23]

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

    # celestial solid angle: dOmega = sin(theta)*dtheta*dphi
    # effective area of detector: dA = cos(theta)*dtheta*dphi
    geometry = np.sin(x)*np.cos(x)
    return A * geometry * np.exp(-B*((1/np.cos(x)) - 1))

def Ciampa(x, A, C, D):
    """ Ciampa 1998: zenith angle distribution """

    # celestial solid angle: dOmega = sin(theta)*dtheta*dphi
    # effective area of detector: dA = cos(theta)*dtheta*dphi
    geometry = np.sin(x)*np.cos(x)
    return A * geometry * np.exp(C *(1/np.cos(x)) - D)

def fit_zenith(zenith, nbins=10, fitfunc=Ciampa):
    """
    fit zenith distribution
    return "B" parameter and reduced Chi-squared error
    """

    zenith = zenith[zenith < 0.8]
    n, bins = np.histogram(zenith, bins=nbins)
    middle = (bins[:-1] + bins[1:])/2.
    sigma = np.sqrt(n)
    try:
        popt, pcov = curve_fit(fitfunc, middle, n)
    except ValueError:
        return None, None

    n_fit = fitfunc(middle, *popt)
    n_dof = len(n)-len(popt)
    reduced_chi_square = np.sum(np.power((n-n_fit)/sigma, 2))/n_dof

    return popt[1], reduced_chi_square

def plot_zenith(zenith, nbins=10, fitfunc=Ciampa):
    """ plot zenith histogram and plot fit """

    zenith = zenith[zenith < 0.8]
    plt.figure()
    n, bins, patches = plt.hist(zenith, bins=nbins, histtype='step', color='b')
    middle = (bins[:-1] + bins[1:])/2.
    sigma = np.sqrt(n)
    popt, pcov = curve_fit(fitfunc, middle, n)
    print popt
    plt.errorbar(middle, n, yerr=sigma, fmt='o',  color= 'b')
    x = np.linspace(0, 1., num=100)
    plt.plot(x,  fitfunc(x, *popt), color='r')

    plt.title('Zenith angle distribution')
    plt.xlabel('zenith angle (rad)')
    plt.legend(['fit: C=%.2f' %(popt[1]),'counts'])
    plt.show()

def get_zenith(filename, stations):
    """ open hdf5 filename. Read or reconstruct directions. Return zenith angles """

    with tables.open_file(filename, 'a') as data:
        try:
            n = len(data.root.coincidences.coincidences)
            if n == 0:
                return None
        except:
            return None

        if not CountReconstructedDirections(data):
            rec = DirectionsOnly(data, overwrite=True)
            rec.reconstruct_and_store(stations)

        zenith = data.root.coincidences.reconstructions.col('zenith')
        zenith = zenith[~np.isnan(zenith)]

    return zenith

if __name__ == '__main__':
    zenith = get_zenith(FILENAME, STATIONS)
    #for nbins in range(5, 50): 
    #    results[nbins] = fit_zenith(zenith, nbins=nbins)
    print fit_zenith(zenith, nbins=20, fitfunc=Ciampa)
    print fit_zenith(zenith, nbins=20, fitfunc=Iyono)

    plot_zenith(zenith)

