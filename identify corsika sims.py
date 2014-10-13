# -*- coding: utf-8 -
"""
Importeer de inhoudsopgave van de CORSIKA sims op /data/hisparc
Inventariseer wat beschikbaar is

LOGBOEK: 13 okt 2014

"""
#
#
import tables
import sapphire.corsika

#
# minimum particles (gamma, electron) at groundlevel
#
E_LOWER_LIMIT = 0.9e14
E_UPPER_LIMIT = 1.1e14
N_LIMIT = 100
THETA = radians(22.5)

FILENAME_SIMULATION_OVERVIEW = 'simulation_overview.h5'

data = tables.open_file(FILENAME_SIMULATION_OVERVIEW,'r')

sim = data.root.simulations

sim_id = sim.col('seed1')
energy = sim.col('energy')
zenith = sim.col('zenith')
particle_id = sim.col('particle_id')
n_photon = sim.col('n_photon')
n_electron = sim.col('n_electron')
# selecteer op energy<10e15, particle id (proton), zenith=0

#
# haal het proton_id nummertje uit sapphire, zodat we op protonprimaries kunnen selecteren
#
proton_id = sapphire.corsika.particles.particle_id('proton')



selected_sims = sim_id.compress( (energy > E_LOWER_LIMIT) & (energy<E_UPPER_LIMIT) & (zenith==THETA) & (particle_id==proton_id) & (n_photon > N_LIMIT) & (n_electron > N_LIMIT))

print "E<10e14, zenith = 0"
print "number of selected simulations (with grounparticles > LIMIT)", selected_sims.size

#
# Investigate the number of particles (photon/electron) at groundlevel in selected sims
#
#n_electrons = n_electron.compress((energy<10e14) & (zenith==0) & (n_electron > 0) & (particle_id==proton_id))
n_photons =     n_photon.compress((energy > E_LOWER_LIMIT) & (energy < E_UPPER_LIMIT) & (zenith==THETA) & (particle_id==proton_id) )
#energys = energy.compress((energy< E_UPPER_LIMIT) & (zenith==0))
n_electrons = n_electron.compress((energy > E_LOWER_LIMIT) & (energy < E_UPPER_LIMIT) & (zenith==THETA) & (particle_id==proton_id) )

#
# Plot een histogram voor het aantal elektronen en photonen dat (per sim) de grond bereikt
#
#
hist(n_photons, bins=100)
hist(n_electrons, bins=100)

#data.close()
