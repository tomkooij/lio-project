"""
plot and fit compton mean free path (from Klein-Nisihina)
for use in sapphire
"""
from compton import compton_mean_free_path
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


def exp_func(x, a, c, d):
    return a * np.exp(-c * x) + d


def polynomial(x, a, b, c):
    return a * x ** 2 + b * x + c


#
# Plot interaction probability for Compton scattering
#
def plot_P_compton_and_fit():

    E = np.logspace(0.001, 0.1, 1000)

    kans = [compton_mean_free_path(energy) for energy in E]

    # maak plotje
    plt.figure()
    plt.plot(E, kans)
    plt.xscale('log')
    # plt.yscale('log')
    plt.ylabel('compton mean free path [cm]')
    plt.xlabel('photon energy (MeV)')

    popt, pcov = curve_fit(polynomial, E, kans, p0=(1, 1, 1))

    fit = polynomial(E, popt[0], popt[1], popt[2])
    plt.plot(E, fit, label="Line 1", linestyle='--')
    plt.legend(['Klein-Nisihina', 'fit'])
    plt.savefig('P_fit.png', dpi=200)
    plt.show()

    return popt


# this is from sapphire! (for testing!)
def _compton_mean_free_path(E):
    """
    Interaction probability based on Klein Nisihina cross section
    W.R. Leo (1987) p 54

    fit from lio-project/photons/mean_free_path.py

    :param E: photon energy [MeV]
    :returns: mean free path [cm]
    """
    if (E < 1.):
        return -0.806 * (E ** 2) + 8.46 * E + 6.36
    elif (E < 30.):
        return -0.109 * (E ** 2) + 6.00 * E + 8.53
    else:
        return 3. * E + 47.  # [cm]


if __name__ == '__main__':
    print 'Kans op foton wisselwerking in scintilator'
    # params = plot_P_compton_and_fit()
    # print '%f * x^2 + %f x + %f' % (params[0], params[1], params[2])
    E_test = [0.01, 0.1, 0.2, 0.5, 1., 5., 10., 20., 30., 40., 100., 1000.]
    for E in E_test:
        print 'test E = %f MeV %f %f' % (E, compton_mean_free_path(E),
                                         _compton_mean_free_path(E))
