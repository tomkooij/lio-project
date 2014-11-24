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
from scipy.optimize import leastsq
from compton import KN_total_cross_section, KN_scattering_cross_section, dsigma_dT, compton_edge

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

    E = np.linspace(0, compton_edge(Egamma),1000)

    T = [dsigma_dT(Egamma, EE)/1e-28 for EE in E]

    plt.plot(E,T)
    plt.ylabel('cross section [barn]')
    plt.xlabel('Electron energy [MeV]')
    plt.title('electron energy distribution')

#
# calculates a normalised, cumulative energy distribution for energy Egamma
#  returns a list of size STEPS
#
def cumulative_energy_distribution(Egamma):

    edge = compton_edge(Egamma)

    cumul = []
    STEPS = 1000

    T = np.linspace(0, edge, STEPS)

    # electron energy distribution
    electron_energy = [dsigma_dT(Egamma, EE) for EE in T]

    cumulative_energy = np.cumsum(electron_energy)

    normalised_energy_distribution = cumulative_energy / cumulative_energy[-1] # divide by last item in list

    return normalised_energy_distribution

#
# Plot a series of cumulative energy distributions to investigate difference
#
def plot_series_cum_distr():

    E = np.logspace(-1,1,15)

    plt.figure()
    y = np.linspace(0,1000,10)
    plt.plot(y,y/1000)  # ploy y = x (normalised)
    for Energy in E:
        n = cumulative_energy_distribution(Energy)
        plt.plot(n)

    plt.title('cum energy distr for compton scattering')
    plt.ylabel('normalised cum energy => electron energy fraction')
    plt.xlabel('bin')

# normalize x-value from 0..1
# distribution is a list [] with y-values
def y_value(x, distribution):

    steps = len(distribution)

    counter = int(x*(steps-1))

    return distribution[counter]

# least squares fit of polynomial of order 2 with c[2] = 0
# y = c[0] * x**2 + c[1] * x  + 0
#
fitfunc  = lambda p, x: p[0]*x**2+p[1]*x
errfunc  = lambda p, x, y: (y - fitfunc(p, x))

def leastsq_fit_polynomial(x_values, y_values):

    init  = [0.5, 0.5, 0.]

    out   = leastsq( errfunc, init, args=(x_values, y_values))

    return out[0]

if __name__=='__main__':

    print "This is calc_T_from_cross_section.py!\n"
#    E = [0.511, 1.0, 2.5]
#    plt.figure()
#    for Energy in E:
#        plot_energy_distribution(Energy)

#    plot_series_cum_distr()

    E = np.logspace(-1,1,20)
    x = np.linspace(0.,1.,1000)
    z_list = []

    # als E een grote lijst is dan is een progressbar nodig!!!!
    for energy in E:
        dist = cumulative_energy_distribution(energy)   # create x,y pairs
        y = [y_value(xx, dist) for xx in x]
        z = np.polyfit(x,y,2)               # fit order 2 polynomial
        print "polyfit z:", energy, z
        z2 = leastsq_fit_polynomial(x, y)  # own fit to set z[0]==0

        z_list.append([energy, z[0], z[1], z[2], z2[0], z2[1], z2[2]])

    z = np.array(z_list)
    z_kwadraat_term = z[:,1]
    z_lin_term = z[:,2]
    z_constante = z[:,3]

    # these can be fitted!!!!!
    plt.figure()
    plt.plot(E,z_kwadraat_term)
    plt.plot(E,z_lin_term)
    plt.figure()
    plt.plot(E,z_constante)
