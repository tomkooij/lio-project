# coding: utf-8
# maak een lijst van de declinatie van de maan per dag
import ephem
import numpy as np

utrecht = ephem.Observer()
utrecht.lon = '5.'
utrecht.lat = '52.'
utrecht.date = ephem.date('2010/01/01')
moon = ephem.Moon(utrecht)
end = ephem.date('2011/01/01')
declist = []

while utrecht.date < end:
    moon.compute(utrecht)
    a = np.degrees(moon.dec)
    #print a
    declist.append(a)
    utrecht.date += 1

print 'declinatie in declist'
