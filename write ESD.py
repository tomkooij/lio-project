# -*- coding: utf-8 -*-
"""
Read data from ESD and write filtered data to new "ESD-like" table

Filter events based on Pulseheight

Only for 4 detector stations!

Two plates = 1 MIP (200mV)
Other two detectors < .6 MIP (120mV)

REASON: Smaller datafiles = less memory issues

Tom Kooij, 27 oct 2010
"""
import tables
import sapphire

from progressbar import ProgressBar, ETA, Bar, Percentage
import sys

STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2014,4,1)
END = datetime.datetime(2014,5,1)
#FILENAME = 'station_501_1wk_april2014.h5'
FILENAME = 'timehistogram\station_501_april2010.h5'
OUT = "s501filtered.h5"
#FILENAME = 'station_501_augustus2014.h5'
#FILENAME = 'station_501_2010_fullyear.h5'

# Pennink, 2010 p32 specifies these cutoff ADC counts
# >200 ADC count = charged particle
# <120 ADC counts = gamma
# These values are consistent with a pulseheight histogram
#
HIGH_PH = 200
LOW_PH = 120
CUT_OFF_PH = 0

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
        #
        # Flush output of print to screen (before progressbar)
        #
        sys.stdout.flush()    
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
    print "WRITING (not appending) filtered data to ", filename
    data = tables.open_file(filename, 'w')
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


#
# Open data files
#
    
data = open_existing_event_file('tempmagweg.h5')   
#data = create_new_event_file('tempmagweg.h5', STATIONS, START, END)
#data = open_existing_event_file('test.h5')
out, outevents = setup_h5_file(OUT)


#
# Setup selection
#
events = data.root.s501.events

t1 = events.col('t1')
t2 = events.col('t2')
t3 = events.col('t3')
t4 = events.col('t4')

ph = events.col('pulseheights')

event_id = events.col('event_id')

ph1 = ph[:,0]
ph2 = ph[:,1]
ph3 = ph[:,2]
ph4 = ph[:,3]

_1_g = ((ph1 <= LOW_PH) & (ph1 > CUT_OFF_PH))
_2_g = ((ph2 <= LOW_PH) & (ph2 > CUT_OFF_PH))
_3_g = ((ph3 <= LOW_PH) & (ph3 > CUT_OFF_PH))
_4_g = ((ph4 <= LOW_PH) & (ph4 > CUT_OFF_PH))

mask_1_gamma = _1_g
mask_2_gamma = _2_g
mask_3_gamma = _3_g
mask_4_gamma = _4_g

_1_e = (ph1 >= HIGH_PH)
_2_e = (ph2 >= HIGH_PH)
_3_e = (ph3 >= HIGH_PH)
_4_e = (ph4 >= HIGH_PH)

mask_1_electron = _1_e
mask_2_electron = _2_e
mask_3_electron = _3_e
mask_4_electron = _4_e

mask_12 = _1_e & _2_e & _3_g & _4_g
mask_13 = _1_e & _2_g & _3_e & _4_g
mask_14 = _1_e & _2_g & _3_g & _4_e
mask_23 = _1_g & _2_e & _3_e & _4_g
mask_24 = _1_g & _2_e & _3_g & _4_e
mask_34 = _1_g & _2_g & _3_e & _4_e

above_noise_threshold = ((t1 != -999.) & (t2 != -999.) & (t3 != -999.) & (t4 != -999.))

mask = mask_12 | mask_13 | mask_14 | mask_23 | mask_24 | mask_34 | above_noise_threshold

#
# This is a list of events that fit above criteria
#  We are doing "if event_id in filtered_events"
#  so this needs to be a set() for FAST search.
#  For selectiong 1 million events out of 2 million (one month)
#  the runtime difference is 5 mins to 9hours. (x100)
#
filtered_events = set(event_id.compress(mask))

#
# Flush output of print to screen
#
sys.stdout.flush()

print "Total events in dataset", event_id.size
print "Selected number of events", len(filtered_events)

progress = ProgressBar(widgets=[ETA(), Bar(), Percentage()])

print "Selecting rows and writing..."

#
# Flush output of print to screen
#
sys.stdout.flush()

for row in progress(events):

    if ( row['event_id'] in filtered_events ) :
        #print row
        append_event(row, outevents)    
        
data.close()
outevents.close()
