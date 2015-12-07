import tables
import sapphire
import os
import datetime

stations = [501]
year = 2010

if __name__ == '__main__':

    for month in range(1,13):
        print "maand: ", month
        start = datetime.datetime(year,month,1)
        if month < 12:
            eind = datetime.datetime(year,(month+1),1)
        else:
            eind = datetime.datetime(year+1,1,1)

        filename = "s501_2010_"+str(month)+".h5"

        if os.path.exists(filename):
            print "Gedaan. Skip."
        else:
            data = tables.open_file(filename, 'w')

            for station in stations:
                if '/s%d' % station in data:
                    print "dataset already in the datafile. Skipping ESD download."
                else:
                    print "Reading ESD data. Station %d" % station, start, eind
                    sapphire.esd.download_data(data, '/s%d' % station, station, start, eind)
