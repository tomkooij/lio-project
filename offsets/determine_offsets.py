"""Determine the change in station offsets over time
from topaz/150416_station_offsets
- First determine dt for each station pair coincidence once
- Use detector offsets from API

"""
import itertools
from datetime import datetime, timedelta
import csv
from glob import glob
import re

from numpy import nan, log10, array, isnan, isinf
import tables

from calibration import determine_station_timing_offset

from sapphire import HiSPARCStations, HiSPARCNetwork
from sapphire.transformations.clock import datetime_to_gps, gps_to_datetime
from sapphire.utils import pbar

"""
Reference stations

501 for Science Park stations, data starting at 2010/1.
"""

SPA_STAT = [501, 502, 503, 504, 505, 506, 508, 509, 510, 511]
CLUSTER = HiSPARCStations(SPA_STAT, force_stale=True)
#DATA_PATH = '/data/hisparc/tom/Datastore/station_offsets/offsets_ref%d_s%d.tsv'
DATA_PATH = 'offsets_ref%d_s%d.tsv'
DAYS = 10

DT_DATAPATH_GLOB = '/data/hisparc/tom/Datastore/station_offsets/dt_ref*_*.h5'
DT_DATAPATH = '/data/hisparc/tom/Datastore/station_offsets/dt_ref%d_%d.h5'
#CLUSTER = HiSPARCNetwork(force_stale=True)

PAIR = (501, 509)

def determine_offsets():
    for pair in get_available_station_pairs():
        print pair
        # skip! determine_offsets_for_pair(pair)
    offsets = determine_offsets_for_pair(PAIR)
    return offsets

def get_available_station_pairs():
    paths = glob(DT_DATAPATH_GLOB)
    pairs = [(int(s1), int(s2))
             for s1, s2 in [re.findall(r'\d+', path[:-3])
              for path in paths]]
    return pairs


def determine_offsets_for_pair(stations):
    ref_station, station = stations
    path = DT_DATAPATH % (ref_station, station)
    with tables.open_file(path, 'r') as data:
        table = data.get_node('/s%d' % station)
        offsets = []
        start = datetime(2010, 1, 1)
        end = datetime(2015, 4, 1)
        for dt0 in (start + timedelta(days=x)
                    for x in pbar(xrange(0, (end - start).days, 10))):
            ts0 = datetime_to_gps(dt0)
            CLUSTER.set_timestamp(ts0)
            # dz is z - z_ref
            r, _, dz = CLUSTER.calc_rphiz_for_stations(
                CLUSTER.get_station(ref_station).station_id,
                CLUSTER.get_station(station).station_id)
            ts1 = datetime_to_gps(dt0 + timedelta(days=max(int(r ** 1.12 / DAYS), 7)))
            dt = table.read_where('(timestamp >= ts0) & (timestamp < ts1)',
                                  field='delta')
            if len(dt) < 100:
                s_off, rchi2 = nan, nan
            else:
                s_off, rchi2 = determine_station_timing_offset(dt, dz)
            offsets.append((ts0, s_off, rchi2))
        #write_offets(station, ref_station, offsets)
    return offsets

def write_offets(station, ref_station, offsets):
    path = DATA_PATH % (ref_station, station)
    with open(path, 'wb') as output:
        csvwriter = csv.writer(output, delimiter='\t')
        csvwriter.writerows((ts, offset, rchi2) for ts, offset, rchi2 in offsets)


def determine_offset_at_timestamp(timestamp, stations=(501,502)):
    ref_station, station = stations
    path = DT_DATAPATH % (ref_station, station)
    with tables.open_file(path, 'r') as data:
        table = data.get_node('/s%d' % station)
        ts0=timestamp
        dt0=gps_to_datetime(timestamp)
        print "ts0 = ", ts0
        print "dt0 = ", dt0
        CLUSTER.set_timestamp(ts0)
        # dz is z - z_ref
        r, _, dz = CLUSTER.calc_rphiz_for_stations(
            CLUSTER.get_station(ref_station).station_id,
            CLUSTER.get_station(station).station_id)
        ts1 = datetime_to_gps(dt0 + timedelta(days=max(int(r ** 1.12 / DAYS), 7)))
        dt = table.read_where('(timestamp >= ts0) & (timestamp < ts1)',
                              field='delta')

        print "len(dt)=", len(dt)
        if len(dt) < 100:
            s_off, rchi2 = nan, nan
        else:
            s_off, rchi2 = determine_station_timing_offset(dt, dz, debug=True, plot=True)

        print "result off fit", s_off, rchi2
        #write_offets(station, ref_station, offsets)

if __name__ == '__main__':
    data = array(determine_offsets())
    rchi2 = data[:, 2]
    offsets = data[:, 1]
    ts  = data[:,  0]
    ts = ts.compress(~isnan(rchi2))
    print "data has all the data" 
    print "offsets is an array of offsets"
    print "rchi2 is an array of red chi2s"

    for timestamp in ts[0:10]:
        print timestamp
        determine_offset_at_timestamp(timestamp, stations=PAIR)
