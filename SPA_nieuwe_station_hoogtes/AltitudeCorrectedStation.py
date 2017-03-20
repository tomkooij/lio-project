"""
sapphire.api.Station

with "new" altitudes -> lla coordinates and gps timing offsets are adjusted.
"""

from sapphire import Station
from sapphire.utils import c, get_active_index
from lazy import lazy


new_altitudes = {501: 55.240, 502: 55.240, 503: 49.240, 504: 54.300,
                 505: 47.950, 506: 44.900, 507: 55.240, 508: 49.905,
                 510: 55.240, 511: 54.465}


class AltitudeCorrectedStation(Station):
    """Station object that returns corrected altitudes
        and corrected GPS timing offsets"""

    @lazy
    def gps_locations(self):
        """Get the GPS location data
        :return: array of timestamps and values.
        """
        tsv = self._get_lla_tsv(self.station)
        try:
            tsv['altitude'] = new_altitudes[self.station]
        except KeyError:
            pass
        return tsv

    def _get_lla_tsv(self, station):
        """Get the GPS location data
        :return: array of timestamps and values.
        """
        columns = ('timestamp', 'latitude', 'longitude', 'altitude')
        path = self.src_urls['gps'].format(station_number=station)
        return self._get_tsv(path, names=columns)

    def station_timing_offset(self, reference_station, timestamp=None):

        assert timestamp is not None, "Give me a timestamp!"

        offset, error = \
            super(AltitudeCorrectedStation,
                  self).station_timing_offset(reference_station, timestamp)

        try:
            dz = new_altitudes[reference_station] - new_altitudes[self.station]
            lla_ref = self._get_lla_tsv(reference_station)
            lla = self._get_lla_tsv(self.station)

            idx_ref = get_active_index(lla_ref['timestamp'], timestamp)
            idx = get_active_index(lla['timestamp'], timestamp)
            dz_old = lla_ref['altitude'][idx_ref] - lla['altitude'][idx]

            offset += (dz_old - dz) / c
        except KeyError:
            pass

        return (offset, error)
