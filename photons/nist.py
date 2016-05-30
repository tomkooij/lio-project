"""
Create lookup tables for:
    mean free path (compton scattering)
    mean free path (pair production)

    based on data from NIST XCOM
    http://www.nist.gov/pml/data/xcom/

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


rho = 1.03  # g / cm3


def exp_func(x, A=0, l=0, x0=0, background=0):
    """ exponential function for curve fitting """

    return A * np.exp(l * (x - x0)) + background


def plot_pair_mean_free_path_versus_E():
    """ plot mean free path """
    E, l = load_XCOM2()

    plt.figure()
    plt.xscale('log')
    plt.yscale('log')

    plt.plot(E, l, 'bo')

    # popt, pcov = curve_fit(exp_func, E, kans, p0=(75., 410., -1.))
    popt = [27, 400, -.002, 47.]
    fit = exp_func(E, popt[0], popt[1], popt[2], popt[3])
    plt.plot(E, fit, label="Line 1", linestyle='--')
    plt.legend(['Leo1987', 'fit'])

    plt.legend(['Nist COMX', 'polyfit'])
    plt.ylabel('mean free path - pair production [cm]')
    plt.xlabel('photon energy (MeV)')
    plt.title('NIST XCOM2 - pair production mean free path in vinyltoluene scintilator')
    plt.show()
    # plt.savefig('pair_freepath.png')


def create_table_for_sapphire():
    """
    output a lookup table to stdout to be include in sapphire

    usage:
    >>> from sapphire.utils import get_active_index
    >>> l_pair = np.array([E0, l0], [E1, l1], ... )  # generated table
    >>> E = l_pair[:, 0]
    >>> l= l_ pair[:, 1]
    >>> idx = get_active_index(E, gamma_energy)
    >>> l[idx]

    """
    E_list, l_list, c_list = load_XCOM2()

    print "l_pair =  np.array([ \ \n\t\t"
    for idx, (E, l) in enumerate(zip(E_list, l_list)):
        if not idx % 3:
            print "\n\t\t",
        print "[%.0f, %3.2f]," % (E, l),
    print "\n\t\t])"

    print "l_compton =  np.array([\ "
    for idx, (E, c) in enumerate(zip(E_list, c_list)):
        if not idx % 3:
            print "\n\t\t",
        print "[%.0f, %3.2f]," % (E, c),
    print "\n\t\t])"


def load_XCOM2():
    """
    load NIST XCOM Data

    http://www.nist.gov/pml/data/xcom/
    Vinyltoluene: C9H10

    """
    data = np.genfromtxt('xcom.txt', skip_header=11)

    print data[0]
    E = data[:, 0]

    a_compton_incoherent = data[:, 2].compress(E > 3.0)

    a_nuc = data[:, 4].compress(E > 3.0)
    a_elec = data[:, 5].compress(E > 3.0)
    E = E.compress(E > 3.0)

    Lpair = 1. / (a_nuc + a_elec)
    Lcompton = 1. / a_compton_incoherent

    print "Lpair [cm] E = 1000 MeV", Lpair[-1]
    print "Lcompton [cm] E = 1000 MeV", Lcompton[-1]

    return E, Lpair, Lcompton


if __name__ == '__main__':
    print "this is nist.py!"

    create_table_for_sapphire()
