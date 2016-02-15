import tables
import numpy as np
from sapphire import ReconstructESDCoincidences

FILENAME = 'oneyear_spa_coinc.h5'
STATIONS = [503, 504, 506]

class DirectionsOnly(ReconstructESDCoincidences):
    def reconstruct_and_store(self, station_numbers=None):
        """Shorthand function to reconstruct coincidences and store results"""

        self.prepare_output()
        self.get_station_timing_offsets()
        self.reconstruct_directions(station_numbers=station_numbers)
        #self.reconstruct_cores(station_numbers=station_numbers)
        self.store_reconstructions()


def CountReconstructedDirections(data):
    """
    Count the number of non-nan zenith angles
    return False on error
    """

    try:
        zenith = data.root.coincidences.reconstructions.col('zenith')
    except:
        return False

    return np.count_nonzero(~np.isnan(zenith))


if __name__ == '__main__':
    with tables.open_file(FILENAME, 'a') as data:
        if not CountReconstructedDirections(data): 
            rec = DirectionsOnly(data, overwrite=True)
            rec.reconstruct_and_store(STATIONS)

        zenith = data.root.coincidences.reconstructions.col('zenith')
        zenith = zenith[~np.isnan(zenith)]


