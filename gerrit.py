import datetime
import tables
import sapphire
from sapphire import esd, ReconstructESDEvents, CoincidenceQuery
from sapphire.transformations.clock import datetime_to_gps
from math import isnan

START = datetime.datetime(2015, 10, 28)
END = datetime.datetime(2015, 11, 27)
STATIONS = [501, 507, 510]

if  __name__ == '__main__':
    if 'data' not in globals():
        data = tables.open_file ('trioeventcoinc_2mnd.h5', 'a')

    for station in STATIONS:
        if '/s%d' % station not in data:
            esd.download_data(data, '/s%d' % station, station, start=START, end=END)
        if '/s%d/reconstructions' % station not in data:
            rec = ReconstructESDEvents(data, '/s%d' % station, station)
            rec.reconstruct_and_store()
        if '/hisparc/cluster_amsterdam/station_%d/reconstructions' % station not in data:
            rec = ReconstructESDEvents(data, '/hisparc/cluster_amsterdam/station_%d' % station, station)
            rec.reconstruct_and_store()

    if '/coincidences' not in data:
        sapphire.download_coincidences (data, stations = STATIONS, start=START, end=END)

    print data

cq = CoincidenceQuery(data)

start = datetime_to_gps(datetime.date(2015, 10, 28))
stop = datetime_to_gps(datetime.date(2015, 11, 10))
coincidences = cq.all([507, 510], start=start, stop=stop, iterator=True)

#specific_events = cq.events_from_stations(coincidences,[507, 510])

reconstructions_iterator = (cq._get_reconstructions(coincidence)
                   for coincidence in coincidences)
coincidences_events = (cq._events_from_stations(reconstructions, [507, 510])
                       for reconstructions in reconstructions_iterator)
specific_reconstructions = cq.minimum_events_for_coincidence(coincidences_events, n=2)

z507 = []
z510 = []

for s in specific_reconstructions:
    if len(s) == 2:
        s1, s2 = s
        if s1[0] == 507:
            zenith507, azimuth507 = s1[1]['zenith'], s1[1]['azimuth']
            zenith510, azimuth510 = s2[1]['zenith'], s2[1]['azimuth']
        else:
            zenith507, azimuth507 = s2[1]['zenith'], s2[1]['azimuth']
            zenith510, azimuth510 = s1[1]['zenith'], s1[1]['azimuth']
        if not isnan(zenith507) and not isnan(zenith510):
            z507.append(zenith507)
            z510.append(zenith510)
