# coding: utf-8
# maak een lijst van de hoogte (zenithhoek) van de maan per dag
from __future__ import division

import ephem
import numpy as np

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

angle = np.arange(0,90.,1.)
cum_f = [(zenith < a).sum()/zenith.size for a in angle]
absorption = [np.sin(a)*(np.cos(a)**6) for a in np.radians(angle)]

# percentage bruikbare events
gain = [cum_f[i]*absorption[i] for i in range(len(angle))]

print 'declinatie in alt. Zenithoek in zenith'
