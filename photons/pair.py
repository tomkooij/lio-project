"""
Pair production door photon in scintillator

Formules uit:
W.R. Leo, "Techniques for Nucl and Part Ph experiments", Springer (1987)

"""

from __future__ import division

import math
import numpy as np
from matplotlib import pyplot as plt

import warnings

r_e = 2.82e-15  # classical electron radius [m]
alpha = 1/137.
electron_rest_mass_MeV = .5109989  # MeV
electron_rest_mass = electron_rest_mass_MeV * 1e6  # eV

THICKNESS = 2.0  # [cm] scintillator thickness



def f(Z):

    """ f(Z) Davies et. al.
    f(Z) is a small correction to the Born approximation which takes
    Coulomb interaction of the emitting electron in the electric field of the
    Nucleus into account

    Bron: Leo 1987 blz 36 eq. 2.67 """

    a = Z / 137.

    return a ** 2 * (1/(1 + a ** 2) + 0.20206 - 0.03699 * a ** 2 +
                     0.0083 * a ** 4 - 0.002 * a ** 6)


def pair_cross_section_no_screening(gamma):
    """ Cross section [m2/atom] for pair forming in nucleus electric field
        no-screening.

    valid if E_photon > 3.5
    valid if gamma << 137

    Bron: Leo 1987 blz 55 eq. 2.116 """

    # throw a warning if gamma > 200
    if gamma > 200:
        warnings.warn('pair_cross_section_no_screening called with gamma > 200')
    if gamma/electron_rest_mass_MeV < 3.5:
        warnings.warn('pair_cross_section_no_screening called with Egamma < 3.5')

    # Z = charge of an average scintilator atom
    Z = (1.104 * 1. + 1. * 6.) / 2

    _ln_fZ = math.log(2*gamma) - f(Z)

    return 4 * Z * (Z+1) * alpha * r_e ** 2 * (7. / 9 * _ln_fZ - 109. / 54)

def pair_cross_section_full_screening(gamma):
    """ Cross section [m2/atom] for pair forming in nucleus electric field
        full screening.

    valid if gamma >> 137 (warn below 100)

    Bron: Leo 1987 blz 55 eq. 2.117 """

    # throw a warning if gamma > 200
    if gamma < 100:
        warnings.warn('pair_cross_section_full_screening called with gamma < 100')

    # Z = charge of an average scintilator atom
    Z = (1.104 * 1. + 1. * 6.) / 2

    _ln_fZ = math.log(183*Z**(1./3)) - f(Z)

    return 4 * Z * (Z+1) * alpha * r_e ** 2 * (7. / 9 * _ln_fZ - 1. / 54)

def radiation_length():

    N_a = 6.022e23  # avogadro
    # vinyltoluene = CH2=CHC6H4CH3 (C9H10)
    rho = 1.032 * 1e6  # g/m3

    Aeff = 9 * 12. + 10 * 1.  # gemmidelde atoommassa per molecuul
    A = Aeff / 19  # per atoom

    Zeff = (9 * 6. + 10 * 1.)  # C9H10
    Z = Zeff / 19  # per atoom
    #A = Z / 0.54141

    _ln_fZ = math.log(183*Z**(1./3)) - f(Z)

    return 1. / ( 4 * Z * (Z+1) * (rho * N_a / A) * alpha * r_e ** 2 * (7. / 9 * _ln_fZ - 1. / 54) )

def pair_cross_section(gamma):
    if gamma > 800:
        return pair_cross_section_full_screening(gamma)
    else:
        return pair_cross_section_no_screening(gamma)

def pair_mean_free_path(energy):
    """ mean free path [m] in vinyltoluene scintilator  """

    N_a = 6.022e23  # avogadro
    # vinyltoluene = CH2=CHC6H4CH3 (C9H10)
    rho = 1.032 * 1e6  # g/m3
    A = 9 * 12. + 10 * 1.  # gemmidelde atoommassa per ATOOM
    A_per_atoom = A / 19.

    # number of atoms per unit volume (m3)
    n = rho / A_per_atoom * N_a  # n  = 1e23 atomen/cm3 = 1e29 atomen/m3

    # electron rest mass 0.5109989 MeV
    # cross section in [m2]
    # n = average number of atoms per unit volume [m3]

    return 1/(n*(pair_cross_section(energy /
                                    electron_rest_mass_MeV))) # [m]


def plot_pair_mean_free_path_versus_E():

    # log input [MeV]
    E = np.logspace(0, 3, 1000)

    # maak een lijst met vrije weglengtes per energie
    l = [100*pair_mean_free_path(energy) for energy in E]  # in [cm]

    # maak plotje
    plt.figure()
    plt.plot(E, l)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('mean free path - pair production [cm]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Pair - mean free path in vinyltoluene scintilator')
    plt.show()
    # plt.savefig('pair_freepath.png')


def plot_cross_section_versus_E():

    # log input [MeV]
    E = np.logspace(0, 3, 1000)

    # maak een lijst met vrije weglengtes per energie
    sigma = [pair_cross_section(energy /
                                electron_rest_mass_MeV)/1e-28 for energy in E]
    # sigma in [barn/atom]

    # maak plotje
    plt.figure()
    plt.plot(E, sigma)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('cross section - pair production [barn/atom]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Pair production in vinyltoluene scintilator')
    plt.show()
    # plt.savefig('pair_freepath.png')


if __name__ == '__main__':

    print "This is pair.py!\n"
    #plot_cross_section_versus_E()
    #plot_pair_mean_free_path_versus_E()
