# ephem
from datetime import datetime
import ephem
import numpy as np

# from 501 events
timestamp = 1264368023
zenith = 0.73978639
azimuth = -2.68735647 % (2*np.pi)


#
# SciencePark
#
SciencePark = ephem.Observer()
SciencePark.lat = '52.355918'
SciencePark.long = '4.9511453'
SciencePark.elevation = 0
SciencePark.date = datetime.utcfromtimestamp(timestamp)

m = ephem.Moon(SciencePark)
print SciencePark
print "m = Moon(SciencePark @ %s) " % datetime.utcfromtimestamp(timestamp)

moon_zenith = np.pi/2 - float(m.alt)
moon_azimuth = float(m.az) % (2*np.pi)

print
print "event (zenith, azimuth): ", zenith, azimuth
print "moon (zenith, azimuth): ", moon_zenith, moon_azimuth
print "separation from (alt,az) = %f" % np.sqrt((zenith-moon_zenith)**2 + (azimuth - moon_azimuth)**2)
