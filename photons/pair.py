"""
Photons door scintilator

simulatie van detector response op foton
 "nagedaan" werk van Dorrith/Jos in April 2010

Formules uit W.R. Leo, "Techniques for Nucl and Part Ph experiments", Springer (1987)

"""

from __future__ import division

import math
import numpy as np
from matplotlib import pyplot as plt

electron_rest_mass_MeV = .5109989 # MeV
electron_rest_mass = electron_rest_mass_MeV * 1e6 # eV

THICKNESS = 2.0 # [cm] scintillator thickness


def f(Z):
    a = Z / 137.

    return a ** 2 * (1/(1 + a ** 2) + 0.20206 - 0.03699 * a ** 2 + 0.0083 * a ** 4 - 0.002 * a ** 6)


def pair_cross_section(gamma):
    """ Bron: Leo 1987 blz 55 """

    r_e = 2.82e-15  # classical electron radius [m]

    # Z = charge of an average atom  H : C = 1.104 : 1 (vinyltoluene)
    Z = (1.104+6)/2

    alpha = 1/137.

    _ln_fZ = math.log(2*gamma) - f(Z)

    return 4 * Z * (Z+1) * alpha * r_e ** 2 * ((7. / 9.) * _ln_fZ - (109. / 54.))


def pair_mean_free_path(energy):

    N_a = 6.022e23 # avogadro
    # vinyltoluene = CH2=CHC6H4CH3 (C9H10)
    rho = 1.032 # g/cm3
    A = 13.1 / 2.

    # number of atoms per unit volume (cm3)
    n = rho * N_a / A

    # electron rest mass 0.5109989 MeV
    # cross section in [m2] Hence the 1e-4 factor
    # n = number of atoms per unit volume [cm3]

    return 1/(n*(pair_cross_section(energy / electron_rest_mass_MeV)*1e4)) # in [cm]


def plot_pair_mean_free_path_versus_E():

    # log input [MeV]
    E = np.logspace(0, 3, 1000)

    # maak een lijst met vrije weglengtes per energie
    l = [pair_mean_free_path(energy) for energy in E] # in [cm]

    # maak plotje
    plt.figure()
    plt.plot(E,l)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('mean free path - pair production [cm]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Pair - mean free path in vinyltoluene scintilator')
    plt.show()
    #plt.savefig('pair_freepath.png')


def plot_cross_section_versus_E():

    # Z = atom number
    Z = 9 * 6. + 10 * 1. # C9H10

    # log input [MeV]
    E = np.logspace(0, 3, 1000)

    # maak een lijst met vrije weglengtes per energie
    sigma = [pair_cross_section(energy/ electron_rest_mass_MeV)/1e-28 for energy in E] # in [barn/atom]

    # maak plotje
    plt.figure()
    plt.plot(E,sigma)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('cross section - pair production [barn/atom]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Pair production in vinyltoluene scintilator')
    plt.show()
    #plt.savefig('pair_freepath.png')


if __name__== '__main__':

    print "This is pair.py!\n"
    plot_cross_section_versus_E()
    plot_pair_mean_free_path_versus_E()
