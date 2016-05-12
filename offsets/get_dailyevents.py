from datetime import date
from dateutil import rrule
import tables
import os
from sapphire import download_data

ESD_PATH = '/data/hisparc/tom/Datastore/dailyevents/'

START = (2015,1,1)
END = (2015,12,31)

if __name__ == '__main__':
    start = date(*START)
    end = date(*END)

    dates = rrule.rrule(rrule.DAILY, dtstart=start, until=end)
    dates = list(dates)
    for idx,dt in enumerate(dates[:-1]):
        #path = ESD_PATH + dt.strftime('%Y/%-m/')
        filename = ESD_PATH + dt.strftime('%Y_%-m_%-d.h5')
        print filename
        #if not os.path.exists(path):
        #    os.mkdir(path)
        with tables.open_file(filename, 'w') as data:
            download_data(data, '/s501', 501, start=dt, end=dates[idx+1])
            download_data(data, '/s502', 502, start=dt, end=dates[idx+1])

