""" Determine calibration values for data

This module can be used to determine calibration values from data.

Determine timing offsets for detectors and stations to correct arrival times.
Determine the PMT response curve to correct the detected number of MIPs.

"""

from numpy import (arange, histogram, percentile, linspace, std, nan, isnan,
                   sqrt, diag, sum, power)
from scipy.optimize import curve_fit
from scipy.stats import norm

import matplotlib.pyplot as plt

def determine_station_timing_offset(dt, dz=0, debug=False, plot=False):
    """Determine the timing offset between stations.

    :param dt: a list of time differences between stations (t - t_ref).
    :param dz: height difference between the stations (z - z_ref).
    :return: mean of a gaussian fit to the data corrected for height.

    """
    if not len(dt):
        return nan
    c = .3
    p = percentile(dt, [0.5, 99.5])
    bins = linspace(p[0], p[1], min(int(p[1] - p[0]), 30))
    if debug:
        print "p= ", p
        print "number of bins=", len(bins)
    station_offset, rchi2 = fit_timing_offset(dt, bins, debug=debug, plot=plot) 
    station_offset += dz/c
    if abs(station_offset) > 1000:
        station_offset = nan, nan
    return station_offset, rchi2

def gauss(x, N, mu, sigma, background):

    return N*norm.pdf(x, mu, sigma) + background

def fit_timing_offset(dt, bins, plot=False, debug=False):
    """Fit the time difference distribution.

    :param dt: a list of time differences between stations (t - t_ref).
    :param bins: bins edges to use for the histogram.
    :return: mean of a gaussian fit to the data corrected for height.

    """
    y, bins = histogram(dt, bins=bins)
    x = (bins[:-1] + bins[1:]) / 2
    sigma = sqrt(y)
    if debug and sum(y < 5):
        print "BLECH! warning encountered empty-like bins!", sum(y<5)
        print "empty bins", sum(y==0)
    try:
        popt, pcov = curve_fit(gauss, x, y, p0=(len(dt), 0., std(dt), 0. ),
                               sigma = sigma, absolute_sigma=False)
        offset = popt[1]
        #sigma_fit = sqrt(diag(popt))
        y_fit = gauss(x, *popt)
        n_dof = len(x) - len(popt)
        rchi2 = sum(power((y-y_fit)/sigma, 2)) / n_dof
        if debug:
            print "result of fit: "
            print "offset = %4.2f " % offset
            print "background = %4.2f " % popt[3]
            print "r chi2 = %1.2f " % rchi2
        if plot:
            plt.figure()
            plt.ion()
            plt.hist(dt, bins=bins, histtype='step')
            plt.plot(x, y_fit, 'r--')
            plt.legend(['fit mu=%3.1f' %(popt[1]), 'hist n=%d' % len(dt)])
            plt.show()
    except RuntimeError:
        offset, rchi2 = nan, nan
    return offset, rchi2


