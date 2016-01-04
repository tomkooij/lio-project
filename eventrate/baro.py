import pandas as pd
import sapphire
import datetime

STATION = 501
FILENAME = 'eventtime-s501-20040326-20151123.csv'


def get_barometeric_pressure_from_api(station, timestamp):
    """
    download entire day of barometric pressure data from API
    select and return the value that most closely matches timestamp

    :param station: station id
    :param timestamp: unix event timestamp
    :return: barometric pressure (float) at timestamp
    """

    api = sapphire.api.Station(station)

    d = datetime.datetime.fromtimestamp(timestamp)

    try:
        baro = api.barometer(d.year, d.month, d.day)
    except:
        print "api failure at timestamp = ", timestamp, d
        return 0

    idx = sapphire.utils.get_active_index(baro['timestamp'], timestamp)
    return baro[idx][1]


if __name__ == '__main__':
    df = pd.read_csv(FILENAME, delimiter='\t', skiprows=18)
    df.info()

    # verwijder eventrate = 0
    df = df[df['value'] > 0]

    # maak col pressure
    df['pressure'] = 0

    for timestamp in df['timestamp']:
        if timestamp > 1420000000:
            print timestamp,
            pressure = get_barometeric_pressure_from_api(STATION, timestamp)
            print pressure
            df.loc[df['timestamp']==timestamp, 'pressure'] = pressure

    # hier alles met pressure==0 verwijderen

    df.to_csv('output.csv')
