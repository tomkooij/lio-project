#Simulatie van de data voor 1 station en reconstructie van de azimut en zenit hoeken

import tables
import matplotlib.pyplot as plt
import numpy as np

from sapphire import HiSPARCStations
from sapphire import GroundParticlesSimulation, ScienceParkCluster
from sapphire import ReconstructESDEvents
from sapphire.simulations.groundparticles import DetectorBoundarySimulation

FILENAME_SIMULATION = '/Users/gebruiker/Desktop/HiSPARC/Project_3_stations_2/Data/simulation_kasper_501.h5'

STATION = 501
cluster = HiSPARCStations([STATION])
max_core_distance = 10


if __name__ == '__main__':
	#Reconstructie van de events
	with tables.open_file(FILENAME_SIMULATION, 'a') as data:
		station_path = '/cluster_simulations/station_'+str(STATION)
		rec = ReconstructESDEvents(data, station_path, station=STATION, verbose=True, overwrite=True)
		rec.reconstruct_and_store()

	data = tables.open_file(FILENAME_SIMULATION)

	events = data.root.cluster_simulations.station_501.events.read()
	rec = data.root.cluster_simulations.station_501.reconstructions.read()

	ev_azimut = events["azimuth"]
	rec_azimut = rec["azimuth"]

	red_ev_azimut, red_rec_azimut = [], []
	counter = 0

	for phi_ev, phi_rec in zip(ev_azimut, rec_azimut):
		if ~np.isnan(phi_rec):
			red_ev_azimut.append(phi_ev)
			red_rec_azimut.append(phi_rec)

	bins = np.arange(-np.pi, np.pi, np.pi/10.)
	plt.hist(red_ev_azimut, bins, histtype='step', label='events')
	plt.hist(red_rec_azimut, bins, histtype='step', label='reconstructions')
	plt.legend()
	plt.show()