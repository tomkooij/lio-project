from datetime import datetime
from sapphire import Station, datetime_to_gps

from AltitudeCorrectedStation import AltitudeCorrectedStation


start = datetime(2016, 1, 1)
end = datetime(2016, 5, 1)
ts = datetime_to_gps(start)
print('date = ', start)
print('ts = ', ts)

s501 = Station(501, force_stale=True)
s510 = Station(510, force_stale=True)

p501 = AltitudeCorrectedStation(501, force_stale=True)
p510 = AltitudeCorrectedStation(510, force_stale=True)


print('501: offset ref 510 :', s501.station_timing_offset(510, ts))
print('501: patched offset :', p501.station_timing_offset(510, ts))
print('510: offset ref 501 :', s510.station_timing_offset(501, ts))
print('510: patched offset :', p510.station_timing_offset(501, ts))
