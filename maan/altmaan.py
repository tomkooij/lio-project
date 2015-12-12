# coding: utf-8
# maak een lijst van de hoogte (zenithhoek) van de maan per dag
from __future__ import division

import ephem
import numpy as np
import matplotlib.pyplot as plt
import tables

FILENAME = 's501_2010_1.h5'

SciencePark = ephem.Observer()
SciencePark.lon = '4.95'
SciencePark.lat = '52.35'
SciencePark.date = ephem.date('2010/01/01')
end = ephem.date('2011/01/01')

alt = []

moon = ephem.Moon(SciencePark)

while SciencePark.date < end:
    moon.compute(SciencePark)
    #print a
    alt.append(np.degrees(moon.alt))
    SciencePark.date += .1

alt = np.asarray(alt)
zenith = 90. - alt

angle = np.arange(0,90.,5.)
#absorption = [np.sin(a)*(np.cos(a)**6) for a in np.radians(angle)]

data = tables.open_file(FILENAME, 'r')
reconstructed_zenith = data.root.s501.maan.col('zenith')

bins=np.arange(0, 180., 5)

plt.figure()
n_events, b, bla = plt.hist(np.degrees(reconstructed_zenith), bins=bins, normed = 1, histtype='step')
n_moon, b, bla = plt.hist(zenith, bins=bins, normed=1, histtype='step')
plt.ylabel('N (normalised)')
plt.xlabel('zenith angle (degrees)')
plt.legend(['event','moon'])
plt.title('Moon at Science Park in 2010')
plt.xlim([0.,180.])
plt.ylim([0.,0.035])
plt.show()

binsize = 1
bins=np.arange(0, 180., binsize)
n_events, b = np.histogram(np.degrees(reconstructed_zenith), bins=bins, normed=True)
n_moon, b = np.histogram(zenith, bins=bins, normed=True)

plt.figure()
plt.plot(n_events*n_moon)
plt.title('N_normed(moon) * N_normed(event) foreach bin (%d degree bins)' % binsize)
plt.ylabel('N*N')
plt.xlabel('zenith angle (degrees)')
plt.legend(['sum = %.6f' % ((n_events*n_moon).sum())])
plt.show()
#cum_f = [(zenith < a).sum()/zenith.size for a in np.arange(0.,90.,5.)]

# percentage bruikbare events
#gain = [cum_f[i]*absorption[i] for i in range(len(angle))]

print 'declinatie in alt. Zenithoek in zenith. Event zenit hoek in reconstructed_zenith'
