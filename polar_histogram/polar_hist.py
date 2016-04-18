from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import tables


def polar_hist(x, ax=None, N=91, normalize=True):
    """ circular (polar) histogram

    data is assumed in [-pi,pi]

    :param x: array of values
    :param ax: optional axes of subplot
    :param N: optional number of bins
    :param normalize: set to False to skip normalisation

    """
    if ax is None:
        ax = plt.subplot(111, projection='polar')

    # calc histogram
    n, bins = np.histogram(x, bins=np.linspace(-np.pi, np.pi, N))

    # create histogram line
    theta = 2 * np.pi * np.arange(0, 1., 0.001)
    if normalize:
        scale_factor = max(n)
    else:
        scale_factor = 1

    mapping_factor = len(n) / len(theta)
    idx = [int(i * mapping_factor) for i in range(len(theta))]
    r = [n[i] / scale_factor for i in idx]

    ax.plot(-theta, r)
    ax.set_rmax(1.1 * max(n) / scale_factor)


if __name__ == '__main__':
    data = tables.open_file('../Datastore/spa_501_503_506.h5', 'r')
    phi = data.root.coincidences.reconstructions.col('azimuth')

    plt.figure()
    plt.title('Azimuth distribution')
    ax = plt.subplot(111, projection='polar')
    polar_hist(phi, ax=ax, normalize=False)
    ax.set_xticklabels(['E', '', 'N', '', 'W', '', 'S', ''])
    plt.show()
