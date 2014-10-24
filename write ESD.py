# -*- coding: utf-8 -*-
"""
Read data from ESD and write filtered data to new "ESD-like" table
"""
import tables
import sapphire

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2014,4,1)
END = datetime.datetime(2014,4,8)
#FILENAME = 'station_501_1wk_april2014.h5'
FILENAME = 'timehistogram\station_501_april2010.h5'
OUT = "esdout.h5"
#FILENAME = 'station_501_augustus2014.h5'
#FILENAME = 'station_501_2010_fullyear.h5'

#
# Read event data from the ESD
#  store in table `/sSTATION' for example: /s501
#
def create_new_event_file(filename, stations, start, end):

    print   "creating file: ",filename
    data = tables.open_file(filename,'w')

    print "reading from the ESD"
    for station in stations:
        print "Now reading station %d" % station
        sapphire.esd.download_data(data, '/s%d' % station, station, START, END)

    return data

#
# Open existing coincidence table.
# Only check if "/coincidences" are in table, no other checks
def open_existing_event_file(filename):
    print "Reading existing ESD datafile ", filename 
    data = tables.open_file(filename, 'r')
    return data

#
# Open (existing) h5 file for output
#
def open_new_h5(filename):
    print "Appending filtered data to ", filename
    data = tables.open_file(filename, 'a')
    return data

#
# Setup output h5 file
#  returns fileinstance "data" and eventstable "events"
#
def setup_h5_file(filename):
    
    data = open_new_h5(filename)
    events = sapphire.esd._get_or_create_events_table(data, '/')
    return data, events

def append_event(event, out_event_table):
    
    # mysterious cleanup needs to be done to prevent all values == 0
    # event[1] needs to be int() but is numpy.int32
    #  when data is read using esd.download_data()

    clean_event = [event[0], int(event[1]), event[2], event[3], event[4],
                   event[5], event[6], event[7], event[8], event[9],
                    event[10], event[11], event[12], event[13], event[14]]
    
    out_event_table.append([clean_event])
    
data = open_existing_event_file(FILENAME)   
events = data.root.s501.events

out, outevents = setup_h5_file(OUT)

for k in range(10):
    print events[k]
    append_event(events[k], outevents)