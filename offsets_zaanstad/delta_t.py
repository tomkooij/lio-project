import tables
from datetime import datetime
from sapphire.analysis.time_deltas import ProcessTimeDeltas

FILENAME = 'coinc_102_105_jan_2016.h5'
start = datetime(2016, 1, 1)
end = datetime(2016, 2, 1)


data = tables.open_file(FILENAME, 'a')

pd = ProcessTimeDeltas(data, progress=True)
pd.determine_and_store_time_deltas()
