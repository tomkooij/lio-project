"""
plot and fit compton mean free path (from Klein-Nisihina)
for use in sapphire
"""
from compton import compton_mean_free_path
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

def exp_func(x, a, c, d):
    return a*np.exp(-c*x)+d

def polynomial(x,a,b,c):
    return a*x**2+b*x+c

#
# Plot interaction probability for Compton scattering
#
def plot_P_compton_and_fit():


    E = np.logspace(.1, 1, 1000)

    kans = [compton_mean_free_path(energy) for energy in E]

    # maak plotje
    plt.figure()
    plt.plot(E,kans)
    plt.xscale('log')
    #plt.yscale('log')
    plt.ylabel('compton mean free path [cm]')
    plt.xlabel('photon energy (MeV)')

    popt, pcov = curve_fit(polynomial, E, kans, p0=(1, 1, 1))

    fit = polynomial(E, popt[0], popt[1], popt[2])
    plt.plot(E, fit, label="Line 1", linestyle='--')
    plt.legend(['Klein-Nisihina','fit'])
    plt.savefig('P_fit.png',dpi=200)
    plt.show()

    return popt

if __name__=='__main__':
    print 'Kans op foton wisselwerking in scintilator'
    params = plot_P_compton_and_fit()
    print '%f * exp (- %f * x) + %f' % (params[0], params[1], params[2])
