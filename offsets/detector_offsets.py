import glob
import re
from sapphire.analysis.calibration import determine_detector_timing_offsets
import tables
from sapphire.transformations.clock import datetime_to_gps
from datetime import datetime
import csv
from sapphire.utils import pbar, round_in_base

PATH = '/data/hisparc/tom/Datastore/dailyevents/*h5'
STATION = 501

if __name__ == '__main__':
    offsets = []
    for path in pbar(glob.glob(PATH)):
        #print path
        y,m,d,_ = map(int, re.findall(r'\d+', path))
        ts = datetime_to_gps(datetime(y,m,d))
        with tables.open_file(path, 'r') as data:
            table = data.get_node('/s%d/events' % STATION)
            offset = [round_in_base(o, 0.25) for o in determine_detector_timing_offsets(table)]
            offsets.append([ts]+offset)
    with open('detector_offsets_%d.tsv' % STATION, 'wb') as output:
        csvwriter = csv.writer(output, delimiter='\t')
        for o in offsets:
            csvwriter.writerow(o)
