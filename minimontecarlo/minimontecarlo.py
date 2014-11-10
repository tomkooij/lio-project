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
electron_rest_mass_MeV = .5109989 # MeV
electron_rest_mass = electron_rest_mass_MeV * 1e6 # eV

THICKNESS = 2.0 # [cm] scintillator thickness

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



def plot_compton_cs_versus_E():

    E = np.logspace(-3, 3, 1000)

    # electron rest mass 0.5 MeV
    # cs in barn
    cs = [KN_cross_section(energy / electron_rest_mass_MeV) / 1e-28 for energy in E]

    plt.plot(E,cs)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Compton scattering cross section [barn]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Klein-Nisihina cross section for compton scattering')
#    plt.savefig('kn_cross_sec.png')

#
# Calculate mean free path for photon in Vinyltoluene scintillator
#   energy = photon energy in [MeV]
#   returns mean free path in [cm]
#
def compton_mean_free_path(energy):

    N_a = 6.022e23 # avogadro
    # vinyltoluene = CH2=CHC6H4CH3 (C9H10)
    rho = 1.032 # g/cm3
    M = 9 * 12. + 10 * 1.

    # number of atoms per unit volume (cm3)
    n = rho * N_a / M

    # Z = atom number
    Z = 9 * 6. + 10 * 1. # C9H10

    # electron rest mass 0.5109989 MeV
    # cross section in [m2]
    # n = number of atoms per unit volume

    return 1/(n*Z*KN_cross_section(energy / electron_rest_mass_MeV)*1e4) # in [cm]

#
# Calculate MAXIMUM energy loss for Compton scattering
#
def compton_max_energy_transfer(energy):

    return (energy * (2. * energy / (electron_rest_mass_MeV+2.*energy) ) )
#
# Calculate energy loss for Compton scattering for scattering angle theta
#
def compton_energy_transfer(energy, theta):

    return (energy * (2. * energy / (electron_rest_mass_MeV+2.*energy) ) )


def plot_MAX_energy_transfer():

    # log input [MeV]
    E = np.logspace(-3, 3, 1000)

    # maak een lijst met T per energie
    T = [compton_max_energy_transfer(energy) for energy in E] # in [cm]

    # maak plotje
    plt.figure()
    plt.plot(E,T)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('T [MeV]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Photon max energy loss for Compton scattering')
    #plt.savefig('T.png')

def plot_compton_mean_free_path_versus_E():

    # log input [MeV]
    E = np.logspace(-3, 3, 1000)

    # maak een lijst met vrije weglengtes per energie
    l = [compton_mean_free_path(energy) for energy in E] # in [cm]

    # maak plotje
    plt.figure()
    plt.plot(E,l)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('mean free path [cm]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Photon mean free path in vinyltoluene scintilator')
#    plt.savefig('freepath.png')

def test_reciprocal_distribution():
    #
    # gamma photon energy is distributed as 1/E
    #  (reciprocal distribution)
    #
    from scipy.stats import reciprocal

    # get "size" random numbers from the reciprocal distribution
    Espectrum = reciprocal.rvs(E_MIN, E_MAX, size=10000)

    # plot histogram to check generated numbers
    plt.figure()
    plt.hist(Espectrum,bins=50,histtype='step')



def montecarlo():
    #
    # Trek een energie uit de verdeling 1/E
    #
    Espectrum = reciprocal.rvs(E_MIN, E_MAX, size=10000)


    for Egamma in Espectrum:

        x = 0  # coordinate
        #
        # Nog in de scintilator?
        #
        while (x < THICKNESS):

            #
            # Bereken vrije weglengte (per interactie type)
            #
            compton_mfp = compton_mean_free_path(Egamma)

            #
            # Selecteer kleinste weglengte  = plaats van volgende interactie
            #
            x = compton_mfp

            #
            # Bereken energie verlies voor deze interactie
            #






if __name__=='__main__':
    plot_compton_cs_versus_E()
    plot_compton_mean_free_path_versus_E()
    test_reciprocal_distribution()
    plot_MAX_energy_transfer()
