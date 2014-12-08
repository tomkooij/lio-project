#
# Bereken (gemiddelde) T uit scattering en absorptie cross sections
#
# Compton scattering
# Egamma = energie invallende photon [MeV]
# T = energie overgedragen aan het verstrooide electron [MeV]

electron_rest_mass_MeV = .5109989 # MeV

import math
from matplotlib import pyplot as plt
import numpy as np
from compton import KN_total_cross_section, KN_scattering_cross_section, dsigma_dT, edge

def calc_AVERAGE_fraction(Egamma):

    g  = Egamma / electron_rest_mass_MeV

    return 1. - (KN_scattering_cross_section(g)/KN_total_cross_section(g))

def plot_T_vs_E():

    E = np.logspace(-1,2,100)

    T = [calc_AVERGE_fraction(Egamma) for Egamma in E]

    plt.figure()
    plt.plot(E,T)
    plt.xscale('log')
#    plt.yscale('log')
    plt.ylabel('electron energy fraction')
    plt.xlabel('photon energy (MeV)')
    plt.title('AVERAGE energy transfer in compton scattering')

def plot_energy_distribution(Egamma):

    E = np.linspace(0, edge(Egamma),1000)

    T = [dsigma_dT(Egamma, EE)/1e-28 for EE in E]

    plt.plot(E,T)
    plt.ylabel('cross section [barn]')
    plt.xlabel('Electron energy [MeV]')
    plt.title('electron energy distribution')

if __name__=='__main__':

    print "This is calc_T_from_cross_section.py!\n"
    E = [0.511, 1.0, 2.5]
    plt.figure()
    for Energy in E:
        plot_energy_distribution(Energy)
