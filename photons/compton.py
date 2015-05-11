"""
Photons door scintilator

simulatie van detector response op foton
 "nagedaan" werk van Dorrith/Jos in April 2010

Formules uit
  W.R. Leo, "Techniques for Nucl and Part Ph experiments", Springer (1987)

"""
from __future__ import division

import math
import numpy as np
from matplotlib import pyplot as plt

E_MAX = 1000.e6  # 1000 MeV
E_MIN = 500.e3  # 500 keV
electron_rest_mass_MeV = .5109989  # MeV
electron_rest_mass = electron_rest_mass_MeV * 1e6  # eV

THICKNESS = 2.0  # [cm] scintillator thickness

# number of simulations
N = 10


#
# Compton scattering
# Klein-Nisihina cross section
#    for electrons
#  "Total probabilty per electron for a Compton scattering to occur"
#
# W.R. Leo, Techniques for Nuclear and Particles Physics Expermiments,
#     Springer (1987)
#
# gamma = photon energie / rest mass electron
# returns cross section (1/m^2 per electron)
#
def KN_total_cross_section(gamma):

    r_e = 2.82e-15  # classical electron radius [m]

    _1_g = 1 + gamma
    _1_2g = 1 + 2 * gamma
    _1_3g = 1 + 3 * gamma
    ln_1_2g = math.log(1 + 2*gamma)

    # Gecontroleerd 3nov2014 (Tweede bron: Am J Phys, 71 p38-45)
    return (2.*math.pi*(r_e**2) * ((_1_g/gamma**2) *
                                   ((2.*_1_g/_1_2g) - (ln_1_2g/gamma)) +
                                   (ln_1_2g/2./gamma) - (_1_3g/(_1_2g)**2)))


#
# Compton scattering
# Klein-Nisihina absorption cross section

# W.R. Leo, Techniques for Nuclear and Particles Physics Expermiments,
#     Springer (1987)
#
# gamma = photon energie / rest mass electron
# returns cross section (1/m^2 per electron)
#
def KN_scattering_cross_section(gamma):

    r_e = 2.82e-15  # classical electron radius [m]

    _1_g = 1 + gamma
    _1_2g = 1 + 2 * gamma
    ln_1_2g = math.log(1 + 2*gamma)

    return (math.pi*(r_e**2) * ( (1/gamma**3 * ln_1_2g) +
                                        (2*(_1_g*(2*gamma**2-2*gamma-1))/(gamma**2*_1_2g**2)) +
                                        (8*gamma**2/(3 * (_1_2g)**3)) ) )


# The absorption cross section is just total - scattering.
def KN_absorption_cross_section(gamma):

    return KN_total_cross_section(gamma) - KN_scattering_cross_section(gamma)


# W.R. Leo (1987) p 54
#
# E photon energy [MeV]
# T electron recoil energy [MeV]

def dsigma_dT(E, T):

    r_e = 2.82e-15  # classical electron radius [m]

    gamma = E / electron_rest_mass_MeV

    s = T / E

    return (math.pi*(r_e**2) / (electron_rest_mass_MeV * gamma**2) *
                    (2 + (s**2 / ((gamma**2) * ((1 - s)**2))) +
                     (s/(1 - s))*(s - 2/gamma)))


# W.R. Leo (1987) p 54
# E photon energy [MeV]
# return compton edge [MeV]
def compton_edge(E):

    gamma = E / electron_rest_mass_MeV

    return (E * 2 * gamma / (1 + 2 * gamma))


def plot_compton_cs_versus_E():

    E = np.logspace(-3, 3, 1000)

    # electron rest mass 0.5 MeV
    # cs in barn
    cs = [KN_total_cross_section(energy / electron_rest_mass_MeV) / 1e-28
          for energy in E]

    plt.plot(E, cs)
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

    N_a = 6.022e23  # avogadro
    # vinyltoluene = CH2=CHC6H4CH3 (C9H10)
    rho = 1.032  # g/cm3
    A = 9 * 12. + 10 * 1.

    # number of atoms per unit volume (cm3)
    n = rho / A * N_a

    # Z = atom number (= number of electrons per atom)
    Z = 9 * 6. + 10 * 1.  # C9H10

    # electron rest mass 0.5109989 MeV
    # cross section in [m2] Hence the 1e4 factor!
    # n = number of ELECTRONS per unit volume

    return 1/(n*Z*KN_total_cross_section(energy / electron_rest_mass_MeV)*1e4)


#
# Calculate the probablity of compton scattering in 2cm vinyltoluene scint
#
def interaction_probability(energy):

    l = compton_mean_free_path(energy)  # [cm]

    # P(x) = 1 - exp^(-1/l*x)  (W.R. Leo, 1987, p 20)
    return (1. - math.exp(-1./l*THICKNESS))


#
# Calculate MAXIMUM energy loss for Compton scattering
#
def compton_max_energy_transfer(energy):

    return (energy * (2. * energy / (electron_rest_mass_MeV + 2. * energy)))


def plot_MAX_energy_transfer():

    # log input [MeV]
    E = np.logspace(-3, 3, 1000)

    # maak een lijst met T per energie
    T = [compton_max_energy_transfer(energy) for energy in E]  # in [cm]

    # maak plotje
    plt.figure()
    plt.plot(E, T)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('T [MeV]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Photon max energy loss for Compton scattering')
    # plt.savefig('T.png')


def plot_compton_mean_free_path_versus_E():

    # log input [MeV]
    E = np.logspace(-3, 3, 1000)

    # maak een lijst met vrije weglengtes per energie
    l = [compton_mean_free_path(energy) for energy in E]  # in [cm]

    # maak plotje
    plt.figure()
    plt.plot(E, l)
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('mean free path [cm]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Photon mean free path in vinyltoluene scintilator')
    # plt.savefig('freepath.png')


def plot_compton_full_versus_E():

    # E = np.logspace(-2, 3, 1000)  # figure 2.23 Leo, p 53
    E = np.logspace(-1, 1, 1000)   # HiSPARC relevant energy spectrum

    # electron rest mass 0.5 MeV
    # cs in barn
    cs_total = [KN_total_cross_section(energy / electron_rest_mass_MeV) / 1e-28
                for energy in E]

    cs_scattering = [KN_scattering_cross_section(energy /
                                                 electron_rest_mass_MeV)
                     / 1e-28 for energy in E]

    cs_absorption = [KN_absorption_cross_section(energy /
                     electron_rest_mass_MeV) / 1e-28 for energy in E]

    plt.plot(E, cs_total, label='total cs')
    plt.plot(E, cs_scattering, label='scattering')
    plt.plot(E, cs_absorption, label='absorption')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('cross section [barn]')
    plt.xlabel('photon energy (MeV)')
    plt.title('Klein-Nisihina cross sections for Compton scattering')
#    plt.savefig('kn_cross_sec.png')


if __name__ == '__main__':

    print "This is compton.py!\n"
