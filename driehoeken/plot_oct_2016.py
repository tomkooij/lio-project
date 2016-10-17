"""
Plots voor Lio verslag

Dit script leest 'driehoeken-fits.csv' (uitvoer van fit_triangles.py)
en maakt plots (evt gebaseerd op selectie van data)
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_d_vs_n(d, n, filename=None):
    """Plot het aantal coincidenties vs afstand"""
    plt.figure()
    plt.yscale('log')
    plt.title('Aantal coincidenties vs afstand')
    plt.ylim((100, 1000000))
    #plt.xlim(0, 1000)
    plt.ylabel('aantal coincidenties')
    plt.xlabel('afstand [m]')
    plt.scatter(d, n)
    if filename:
        plt.savefig(filename, dpi=200)
    plt.show()

def plot_opp_vs_n(d, n, filename=None):
    """Plot het aantal coincidenties vs oppervlak = afstand**2"""

    plt.figure()
    plt.yscale('log')
    plt.title('Aantal coincidenties vs oppervlakte')
    plt.ylim((100, 1000000))
    plt.ylabel('aantal coincidenties')
    plt.xlabel('kwadraat afstand [m**2]')
    d2 = [x**2 for x in d]
    plt.scatter(d2, n)
    if filename:
        plt.savefig(filename, dpi=200)
    plt.show()
    plt.show()

def plot_d_vs_C(d, C, filename=None):
    """Plot C vs afstand"""
    plt.figure()
    plt.title('C vs afstand')
    #plt.xlim(0, 1000)
    plt.ylabel('C')
    plt.xlabel('afstand [m]')
    plt.scatter(d, C)
    if filename:
        plt.savefig(filename, dpi=200)
    plt.show()


df = pd.read_csv('driehoeken-fits.csv')

#select n > 1000
df = df.loc[df['n'] > 1000]
d = df['max distance']
n = df['n']
C = df['C']

plot_d_vs_n(d, n, filename='d_vs_n.png')
plot_d_vs_C(d, C, filename='opp_vs_n.png')
