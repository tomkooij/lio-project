import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

rho = 1.03  # g / cm3

def exp_func(x, *therest):

    args = list(therest)
    args.append(0)
    args.append(0)
    print args

    return args[0]*np.exp(args[1]*(x-args[2])) + args[3]


def plot_pair_mean_free_path_versus_E():

    E, l = load_XCOM2()

    # maak plotje
    plt.figure()
    plt.xscale('log')
    plt.yscale('log')

    l1 = l.compress((E > 10) & (E < 300))
    E1 = E.compress((E > 10) & (E < 300))

    plt.plot(E, l, 'bo')

    #popt, pcov = curve_fit(exp_func, E, kans, p0=(75., 410., -1.))
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

    E_list, l_list = load_XCOM2()

    l_max = l_list[-1]
    l_list = l_list.compress(E_list < 10000)
    E_list = E_list.compress(E_list < 10000)

    print "l_pair =  [ \ "

    for E,l in zip(E_list, l_list):
        print "           [%.0f, %3.2f], " % ( E, l )

    print "          ];"
    print "l_max = %3.2f" % l_max

def load_XCOM2():

    data = np.genfromtxt('xcom.txt', skip_header=11)

    E = data[:,0]

    a_nuc = data[:,4].compress(E > 3.0)
    a_elec = data[:,5].compress(E > 3.0)
    E = E.compress(E > 3.0)

    Lpair_nuc = 1./a_nuc
    Lpair_elec = 1./a_elec

    Lpair = 1./(a_nuc+a_elec)

    print "Lpair [cm] E = 1000 MeV", Lpair[-1]

    return E, Lpair

if __name__ == '__main__':
    print "this is nist.py!"

    create_table_for_sapphire()
