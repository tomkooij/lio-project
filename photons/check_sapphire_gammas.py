"""
Check sapphire implementation of dsigma/dT versus the plot
in Evans (1955), page 693, figure 5.1
"""

import matplotlib.pyplot as plt
from numpy import append, linspace

from sapphire.simulations.gammas import dsigma_dT, compton_edge

def plot_energy_distribution(gamma_energy):
    """plot transfered energy versus gamma energy"""
    E = linspace(0, compton_edge(gamma_energy), 1000)

    T = [dsigma_dT(gamma_energy, EE) / 1e-28 for EE in E]

    # add line at compton edge
    append(T, [0])
    append(E, [E[-1]])

    plt.plot(E,T)

def Evans_figure():
    """Evans (1955), page 693, figure 5.1"""
    E = [0.511, 1.2, 2.5]
    plt.figure()
    for gamma_energy in E:
        plot_energy_distribution(gamma_energy)
    plt.legend(['0.511 MeV','1.0 MeV','2.5 MeV'])
    plt.ylabel('cross section [barn]')
    plt.xlabel('Electron energy [MeV]')
    plt.title('electron energy distribution')
    plt.savefig('compton_edge.png', dpi=200)


if __name__ == '__main__':
    Evans_figure()
