# ephem
from datetime import datetime
import ephem

timestamp = 1264368023

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
