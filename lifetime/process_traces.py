import datetime
import os
import zlib
from collections import defaultdict

import numpy as np
import tables
from sapphire.utils import pbar
from sapphire.publicdb import datetimerange

from find_peaks import find_peaks


START = datetime.datetime(2018, 1, 1)
END = datetime.datetime(2018, 1, 1)
STATION = 102

ADC_THRESHOLD = 20  # ADC over baseline for first arrival time


def make_filename(station, start, end):
    sd = start.strftime('%b%y')
    ed = end.strftime('%b%y')
    return f'dts-{station}-{sd}-{ed}'


def get_data_path(date):
    return '2019_7_8_station102.h5'
    rootdir = '/databases/frome/'
    filepath = date.strftime('%Y/%-m/%Y_%-m_%-d.h5')
    return os.path.join(rootdir, filepath)


def process(station, start, end):
    peaks_in_event = defaultdict(list)
    for date, _ in datetimerange(start, end):
        print(date)
        path = get_data_path(date)
        with tables.open_file(path, 'r') as file:
            try:
                node = file.get_node(f'/hisparc/cluster_amsterdam/station_{station}')
                events = node.events.read()
                blobs = node.blobs.read()
            except tables.NoSuchNodeError:
                print('skip: no data for: ', date)
                continue
            print('n events = ', len(events))
            for event in pbar(events):
                ext_timestamp = event['ext_timestamp']
                traces_idx = event['traces']
                baselines = event['baseline']
                traces_str = [zlib.decompress(blobs[trace_idx]).decode('utf-8')
                              for trace_idx in traces_idx if trace_idx != -1]

                for idx, trace_str in enumerate(traces_str):
                    baseline = baselines[idx]
                    if baseline == -999:
                        continue
                    trace = np.fromstring(trace_str, dtype=int, sep=',') - baseline
                    peaks_in_trace = find_peaks(trace, threshold=ADC_THRESHOLD)
                    if len(peaks_in_trace):
                        peaks_in_event[ext_timestamp].append(peaks_in_trace)

    return peaks_in_event


def main():
    FILENAME = make_filename(STATION, START, END)
    print(FILENAME)

    peaks_in_event = process(STATION, START, END)

    with open(FILENAME+'.csv', 'w') as f:
        f.write(f'# station={STATION}\n')
        for ext_timestamp, traces in peaks_in_event.items():
            for peaks in traces:
                for t, ph, pint in peaks:
                    f.write(f'{t}, {ph}, {pint}, {ext_timestamp}\n')


if __name__ == '__main__':
    main()
