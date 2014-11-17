from compton import interaction_probability
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# algemene exponentiele functie voor curve_fit
def exp_func(x, a, c, d):
    return a*np.exp(-c*x)+d

#
# Plot interaction probability for Compton scattering
#
def plot_P_compton_and_fit():


    E = np.logspace(.1, 1, 1000)

    kans = [interaction_probability(energy) for energy in E]

    # maak plotje
    plt.figure()
    plt.plot(E,kans)
#    plt.xscale('log')
#    plt.yscale('log')
    plt.ylabel('Interaction probability')
    plt.xlabel('photon energy (MeV)')
    plt.title('Interaction probability in 2cm VinylToluene scinitilator for Compton scattering')
    #plt.savefig('P_Compton-log.png')

    popt, pcov = curve_fit(exp_func, E, kans, p0=(1, 1, 1))

    fit = exp_func(E, popt[0], popt[1], popt[2])
    plt.plot(E, fit, label="Line 1", linestyle='--')
    #plt.savefig('fit.png')

    return popt

if __name__=='__main__':
    print 'Kans op foton wisselwerking in scintilator'
    params = plot_P_compton_and_fit()
    print '%f * exp (- %f * x) + %f' % (params[0], params[1], params[2])
