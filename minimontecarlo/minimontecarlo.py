"""
mini monte carlo

simulatie van detector response op foton
 "nagedaan" werk van Dorrith/Jos in April 2010

Gebaseerd op Am J Phys 71, p38-45
"""

import math
import numpy as np
from matplotlib import pyplot as plt

E_MAX = 1000.e6 # 1000 MeV
E_MIN = 500.e3 # 500 keV

#number of simulations
N = 10

#
# calculate the Klein-Nisihina cross section
#
# gamma = photon energie / rest mass electron

def KN_cross_section(gamma):

    r_e = 2.82e-15 # classical electron radius [m]

    _1_g = 1 + gamma
    _1_2g = 1 + 2 * gamma
    _1_3g = 1 + 3 * gamma
    ln_1_2g = math.log(1 + 2*gamma)

    # Bron: Am J Phys, 71 p38-45
    # Gecontroleerd 3nov2014
    return (2.*math.pi*(r_e**2) * ((_1_g/gamma**2) *
                                   ((2.*_1_g/_1_2g) - (ln_1_2g/gamma)) +
                                   (ln_1_2g/2./gamma) - (_1_3g/(_1_2g)**2)))


electron_rest_mass = .5e6 # .5 MeV

def plot_compton_cs_versus_E():

    E = np.logspace(-3, 3, 1000)

    # electron rest mass 0.5 MeV
    # cs in barn
    cs = [KN_cross_section(energy / .5) / 1e-28 for energy in E]

    plt.plot(E,cs)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Compton scattering cross section [barn]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Klein-Nisihina cross section for compton scattering')
    plt.savefig('kn_cross_sec.png')

def plot_compton_mean_free_path_versus_E():

    E = np.logspace(-3, 3, 1000)


    N_a = 6.022e23 # avogadro
    # vinyltoluene = CH2=CHC6H4CH3 (C9H10)
    rho = 1.032 # g/cm3
    M = 9 * 12. + 10 * 1.

    # number of atoms per unit volume (cm3)
    n = rho * N_a / M

    # electron rest mass 0.5 MeV
    # cross section in [m2]
    # n = number of atoms per unit volume
    # Z = atom number
    Z = 9 * 6. + 10 * 1. # C9H10

    l = [1/(n*Z*KN_cross_section(energy / .5)*1e4) for energy in E] # in [cm]


    plt.figure()
    plt.plot(E,l)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('mean free path [cm]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Photon mean free path in vinyltoluene scintilator')
    plt.savefig('freepath.png')

if __name__=='__main__':
    plot_compton_cs_versus_E()
    plot_compton_mean_free_path_versus_E()

# def some_other_things():
#     #
#     # Trek een energie uit de verdeling 1/E
#     #
#     #
#     # 1/E heb ik nog niet onder de knie dus eerst maars een uniform:
#     #
#     Espectrum = numpy.random.uniform(low=100.e3, high=1000.e6, size=10000)
#
#     cs_list = []
#
#     for Egamma in Espectrum:
#         gamma = Egamma/electron_rest_mass
#         print "energy, gamma ",Egamma, gamma
#
#         cs = KN_cross_section(gamma) / 1e-28 # barn
#
#         cs_list.append(cs)
