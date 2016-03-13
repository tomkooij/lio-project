from __future__ import division
import numpy as np
import pylab as plt


def polar_hist(x, ax=None, N=91, normalize=True):
    """ circular (polar) histogram

    :param x: array of values
    :param ax: optional axes of subplot
    :param N: optional number of bins
    :param normalize: set to False to skip normalisation

    """
    if ax is None:
        ax = plt.subplot(111, projection='polar')

    # calc histogram
    n, bins = np.histogram(x, bins=np.linspace(0, 2 * np.pi, N))

    # create histogram line
    theta = 2 * np.pi * np.arange(0, 1., 0.001)
    if normalize:
        scale_factor = max(n)
    else:
        scale_factor = 1

    mapping_factor = len(n) / len(theta)
    idx = [int(i * mapping_factor) for i in range(len(theta))]
    r = [n[i] / scale_factor for i in idx]

    ax.plot(theta, r)
    ax.set_rmax(1.1 * max(n) / scale_factor)


if __name__ == '__main__':
    x = np.random.uniform(0, 2 * np.pi, 10000)
    ax = plt.subplot(121, projection='polar')
    polar_hist(x, ax=ax)
    ax = plt.subplot(122, projection='polar')
    polar_hist(x, ax=ax, normalize=False)
    plt.show()
