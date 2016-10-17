# test influence of the C parameter

from fit_ciampa import Ciampa
import matplotlib.pyplot as plt
import numpy as np
def plot_C(C = -5.5, A = 1):
    """ plot Ciampa distribution """

    x = np.linspace(0,0.8,100)

    plt.plot(x,  Ciampa(x, A, C, 1.))

    plt.title('Zenith angle distribution')
    plt.xlabel('zenith angle (rad)')

if __name__ == '__main__':
    plt.figure() 
    plot_C()
    plt.show()
