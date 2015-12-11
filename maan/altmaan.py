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
zenith = np.where(alt > 0, 90. - alt, 90.)

angle = np.arange(0,90.,5.)
#absorption = [np.sin(a)*(np.cos(a)**6) for a in np.radians(angle)]

data = tables.open_file(FILENAME, 'r')
reconstructed_zenith = data.root.s501.maan.col('zenith')

bins=np.arange(0, 100., 5)

plt.figure()
n1, b, bla = plt.hist(np.degrees(reconstructed_zenith), bins=bins, normed = 1, histtype='step')
n2, b, bla = plt.hist(zenith, bins=np.arange(0, 100., 5.), normed=1, histtype='step')
plt.ylabel('N (normalised)')
plt.xlabel('zenith angle (degrees)')
plt.legend(['event','moon'])
plt.title('Moon @ SciencePark 2010')
plt.xlim([0.,90.])
plt.ylim([0.,0.05])
plt.show()

plt.figure()
plt.plot(n1*n2)
plt.title('sum = %f percent' % ((n1*n2).sum()*100.))
plt.show()
cum_f = [(zenith < a).sum()/zenith.size for a in np.arange(0.,90.,5.)]

# percentage bruikbare events
#gain = [cum_f[i]*absorption[i] for i in range(len(angle))]

print 'declinatie in alt. Zenithoek in zenith. Event zenit hoek in reconstructed_zenith'
