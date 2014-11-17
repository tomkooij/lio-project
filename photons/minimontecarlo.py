"""
mini monte carlo

simulatie van detector response op foton
 "nagedaan" werk van Dorrith/Jos in April 2010

Gebaseerd op Am J Phys 71, p38-45
"""

from compton import *
import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

E_MAX = 1000.e6 # 1000 MeV
E_MIN = 500.e3 # 500 keV
electron_rest_mass_MeV = .5109989 # MeV
electron_rest_mass = electron_rest_mass_MeV * 1e6 # eV

THICKNESS = 2.0 # [cm] scintillator thickness

#number of simulations
N = 10


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

    #test_reciprocal_distribution()

    print "This is minimontecarlo!\n"
