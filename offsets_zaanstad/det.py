import tables
from sapphire.analysis.calibration import determine_detector_timing_offsets
from sapphire import HiSPARCStations


sn = 105

FILENAME = '1jan2016_s%d.h5' % sn
node = '/s%d/events' % sn
print('node ', node)

with tables.open_file(FILENAME, 'a') as data:

    events = data.get_node(node)
    print('number of events: ', len(events))

    station = HiSPARCStations([sn]).stations[0]
    o = determine_detector_timing_offsets(events, station)
    print(o)
