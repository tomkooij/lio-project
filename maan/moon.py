# ephem
from datetime import datetime
import ephem
import numpy as np

from sapphire.transformations.celestial import zenithazimuth_to_equatorial
from sapphire.transformations.base import decimal_to_sexagesimal as decdeg2dms
from sapphire.utils import norm_angle, angle_between


# event
timestamp = 1264368023
# Gecontroleerd met heavens-above.com en stellarium en USNO tabellen:
# bij deze timestamp hoort (@SciencePark) de maan alt = 46 graden, azi = 242 graden
# ra,dec = 3h12min, 26d08min

zenith = 0.73978639
azimuth = -2.68735647

# SciencePark
latitude = 52.355918
longitude = 4.9511453

#
SciencePark = ephem.Observer()
SciencePark.lat = np.radians(latitude)
SciencePark.long = np.radians(longitude)
SciencePark.elevation = 0
SciencePark.date = datetime.utcfromtimestamp(timestamp)

m = ephem.Moon(SciencePark)
print SciencePark
print "m = Moon(SciencePark @ %s) " % datetime.utcfromtimestamp(timestamp)

moon_zenith = np.pi/2 - float(m.alt)
moon_azimuth = float(m.az) % (2*np.pi)
moon_ra = float(m.ra)  # m.ra is WITH atmospheric abberations, m.g_ra without
moon_dec = float(m.dec)

zenith = moon_zenith
#
# PyEphem azimuth: North=0°, East=90°, South=180°, West=270°
# Sapphire azimuth: E=0°, N=90°, W=180°, S=-90°
#
azimuth = norm_angle(-(moon_azimuth - np.pi/2))

print zenith, azimuth
# zenithazimuth_to_equatorial really uses (lon, lat)
ra, dec = zenithazimuth_to_equatorial(longitude, latitude, timestamp, zenith, azimuth)

print
print "moon (alt, azi) [degrees]", 90. - np.degrees(moon_zenith), np.degrees(moon_azimuth)
print "event (zenith, azimuth): ", zenith, azimuth
print "moon (zenith, azimuth): ", moon_zenith, moon_azimuth
print "separation from (alt,az) = %f" % angle_between(zenith, moon_zenith, azimuth, moon_azimuth)
print
print "moon (ra [graden] , dec [uren])", decdeg2dms(moon_ra/(2*np.pi)*24), decdeg2dms(np.degrees(moon_dec))
print "event (ra,dec) calculated from zen,az,position", decdeg2dms(ra/(2*np.pi)*24), decdeg2dms(np.degrees(dec))
print "seperation from ephem.separation((ra,dec),(moon_ra,moon_dec))", float(ephem.separation((ra,dec),(moon_ra,moon_dec)))
