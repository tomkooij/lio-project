import sapphire
import datetime
import tables


STATION = 501
STATIONS = [STATION]
START = datetime.datetime(2010, 4, 1)
END = datetime.datetime(2010, 4, 2)
FILENAME = 'station_501_1dag.h5'


#
# Read event data from the ESD
#  store in table `/sSTATION' for example: /s501
#
def create_new_event_file(filename, stations, start, end):

    print  "creating file: ", filename
    data = tables.open_file(filename, 'w')

    print "reading from the ESD"
    for station in stations:
        print "Now reading station %d" % station
        sapphire.esd.download_data(data, '/s%d' % station, station, START, END)

    return data


if __name__ == '__main__':
    data = create_new_event_file(FILENAME, STATIONS, START, END)
