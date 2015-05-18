"""
read gamma photon digitisation output

from sapphire:test_groundparticles_gamma branch
groundparticles.py

    In this branch intermediate results of gamma digitisation are
    written to stdout, to be analysed using a separate script.

    legend:
    * E angle depth_pair depth_pair
    foton "processed" energy = E [MeV] and angle of incidence angle [rad]
        interaction depth for each mechanism
    C energy depth_pair maximum_energy_deposit_in_MIPS
                                                energy_deposit_in_MIPS mips
    P energy depth_pair maximum_energy_deposit_in_MIPS
                                                energy_deposit_in_MIPS mips
    C = compton scattering
    P = pair production
"""

import matplotlib.pyplot as plt
import numpy as np

FILENAME = 'output'

if __name__ == '__main__':

    photon_counter = 0
    pair_counter = 0
    compton_counter = 0
    unrecogised_line = 0

    photon_spectrum = []
    compton_spectrum = []
    pair_spectrum = []

    with open(FILENAME) as f:
        # lees de hele file. Verwijder \n en splits op spaties
        lines = [line.strip().split(' ') for line in f]

        for line in lines:
            if (line[0] == '*'):
                photon_counter += 1
                photon_spectrum.append(float(line[1]))

            elif (line[0] == 'C'):
                compton_counter += 1
                compton_spectrum.append(float(line[1]))

            elif (line[0] == 'P'):
                pair_counter += 1
                pair_spectrum.append(float(line[1]))

            else:
                unrecogised_line += 1

    print "#photons = ", photon_counter
    print "#compton = ", compton_counter
    print "#pair = ", pair_counter
    print "#unrecogised_line", unrecogised_line

    plt.figure()
    plt.hist(photon_spectrum, histtype='step', bins = np.linspace(1, 102, 20))
    plt.hist(pair_spectrum, histtype='step', bins = np.linspace(1, 102, 20))
    plt.hist(compton_spectrum, histtype='step', bins = np.linspace(1, 102, 20))
    plt.yscale('log')
    plt.legend(['total generated','pair', 'compton'])
    plt.title('(detected) photons')
    plt.savefig('detected_photons.png', dpi=200)
    plt.show()
