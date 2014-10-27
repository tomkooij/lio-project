import datetime
import tables
from sapphire import esd


if __name__ == '__main__':
    if 'data' not in globals():
        data = tables.open_file('copy_data.h5', 'a')
    if '/s501/events' not in data:
        esd.download_data(data, '/s501', 501,
                          datetime.datetime(2014, 1, 1),
                          datetime.datetime(2014, 1, 2))

    if 'out' in globals():
        out.close()
    out = tables.open_file('data_out.h5', 'w')
    # Using private function!!
    out_events = esd._get_or_create_events_table(out, '/test1')
    out_events2 = esd._get_or_create_events_table(out, '/test2')
    out_events3 = esd._get_or_create_events_table(out, '/test3')
   
    ## THIS IS IT!

    # method 1: use read_where() to build an array of selected events
    sel_events = data.root.s501.events.read_where('n1 > 5.')
    out_events.append(sel_events)

    # method 2: use a slice of the events table
    sel_events2 = data.root.s501.events[:100]
    out_events2.append(sel_events2)

    # method 3: working with single events can get a bit ugly.
    # The idea is that append() expects an array of rows.  If you only
    # have one row, you must build an array out of it.  However, the array
    # should be 2-dimensional: append() expects a list of rows, each row
    # containing a list of columns.  We only have a list of columns.  So
    # make a list of events like so: [event].  Then, use array() to build
    # an array out of that.
    ids_events3 = [14, 28, 57, 3, 300, 301, 302, 303]
    for event_id in ids_events3:
        event = data.root.s501.events[event_id]
        out_events3.append(array([event]))
