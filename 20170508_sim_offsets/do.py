# coding: utf-8
import tables
from sapphire.analysis.reconstructions import ReconstructESDEvents, ReconstructESDCoincidences

FILENAME = 'groundparticle_simulation_detector_boundery_501.h5'
with tables.open_file(FILENAME, 'a') as data:
    rec = ReconstructESDEvents(data, '/cluster_simulations/station_501', 501, verbose=True)
    rec.get_detector_offsets()
    print(rec.offsets)

    rec = ReconstructESDCoincidences(data, verbose=True)
    rec.get_station_timing_offsets()
    print(rec.offsets)


print('ESD:')

FILENAME = 'data1.h5'
with tables.open_file(FILENAME, 'a') as data:
    rec = ReconstructESDEvents(data, '/s4', 501, verbose=True)
    rec.get_detector_offsets()
    print(rec.offsets)

FILENAME = 'data_coinc.h5'
with tables.open_file(FILENAME, 'a') as data:
    rec = ReconstructESDCoincidences(data, verbose=True)
    rec.get_station_timing_offsets()
    print(rec.offsets)
