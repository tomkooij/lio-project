"""
Download events from ESD
store in HDF5 /s501/events
Select events with accurate direction reconstruction
Perform direction reconstruction (alt, az, RA, DEC)
Add Moon RA,DEC
Store all data in new HDF5 table /s501/moon
"""

from __future__ import division
import tables

from sapphire.analysis.direction_reconstruction import EventDirectionReconstruction
from sapphire import HiSPARCStations
from sapphire.transformations.celestial import zenithazimuth_to_equatorial
from datetime import datetime

import ephem

import math
import matplotlib.pyplot as plt



FILENAME  = 'station_501_april2010.h5'


def reconstruct_and_store(filename):

    with tables.open_file(filename, 'a') as data:

        timestamp = data.root.s501.events[0]['timestamp']

        s501 = HiSPARCStations([501]).get_station(501)
        s501.cluster.set_timestamp(timestamp)
        rec = EventDirectionReconstruction(s501)

        query = '(n2 > 2.0) & (n3 > 2.0) & (n4 > 2.0)'
        events = data.root.s501.events

        description = events.description._v_colObjects.copy()
        description['zenith'] = tables.Float32Col()
        description['azimuth'] = tables.Float32Col()
        description['ra'] = tables.Float32Col()
        description['dec'] = tables.Float32Col()
        description['maan_alt'] = tables.Float32Col()
        description['maan_az'] = tables.Float32Col()
        description['maan_ra'] = tables.Float32Col()
        description['maan_dec'] = tables.Float32Col()
        description['separation'] = tables.Float32Col()

        try:
            data.remove_node('/s501/maan')
        except:
            pass

        copy = tables.Table(data.root.s501, 'maan', description)

        # Copy the user attributes
        events.attrs._f_copy(copy)

        selected_events = data.root.s501.events.read_where(query)

        teller = 0

        for event in selected_events:

            zenith, azimuth, detectors = rec.reconstruct_event(event)

            if not math.isnan(zenith):

                teller += 1
                if teller % 1000 == 0:
                    print teller

                # break up event
                (id, timestamp, nanoseconds, ext_timestamp, ph, integrals, n1, n2, n3, n4, t1, t2, t3, t4, t_trigger) = event

                row = copy.row

                # copy events info
                row['event_id'] = teller
                row['timestamp'] = int(timestamp)
                row['nanoseconds'] = int(nanoseconds)
                row['ext_timestamp'] = int(timestamp) * int(1e9) + int(nanoseconds)
                row['pulseheights'] = [int(ph[0]), int(ph[1]), int(ph[2]), int(ph[3])]
                row['integrals'] = [int(integrals[0]), int(integrals[1]), int(integrals[2]), int(integrals[3])]
                row['n1'] = float(n1)
                row['n2'] = float(n2)
                row['n3'] = float(n3)
                row['n4'] = float(n4)
                row['t1'] = float(t1)
                row['t2'] = float(t2)
                row['t3'] = float(t3)
                row['t4'] = float(t4)
                row['t_trigger'] = float(t_trigger)

                # store reconstruction
                row['zenith'] = zenith
                row['azimuth'] = azimuth

                longitude, latitude, alt = s501.get_lla_coordinates()

                ra, dec = zenithazimuth_to_equatorial(longitude, latitude, timestamp, zenith, azimuth)

                s = ephem.Observer()
                s.long = longitude
                s.lat = latitude
                s.elevation = 0
                s.date = datetime.fromtimestamp(timestamp)

                m = ephem.Moon(s)

                separation = ephem.separation((m.ra, m.dec), (ra, dec))

                row['maan_ra'] = m.ra
                row['maan_dec'] = m.dec
                row['maan_alt'] = m.alt
                row['maan_az'] = m.az

                row['separation'] = separation

                row.append()

        print "reconstructed %d of %d events, " % (data.root.s501.maan.col('n1').size, selected_events.size)

        return data.root.s501.maan.col('n1').size

if __name__ == '__main__':
    reconstruct_and_store(FILENAME)
