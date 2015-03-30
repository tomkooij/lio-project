# -*- coding: utf-8 -*-
"""
Plot particles at groundlevel
x,y in meters!
"""
import tables
import matplotlib.pyplot as plt
import numpy as np

# particle selection
R_MAX = 100.
R_MIN = 90.

#FILENAME = 'corsika_834927089_144221120.h5'    # 1e14 p theta = 0
FILENAME = 'corsika_713335232_854491062.h5'    # 1e14 p theta = 0
#FILENAME = 'corsika_77102826_200916071.h5'     # 1e14 p theta = 22.5

data = tables.open_file(FILENAME, 'r')
gp = data.root.groundparticles


id = gp.col('particle_id')
t = gp.col('t')
x = gp.col('x')
y = gp.col('y')
r = gp.col('r')
phi = gp.col('phi')

#ax = plt.subplot(111,polar=True)
#ax.scatter(phi,r)
#ax.set_rmax(3500.0)
#plt.show()

bins2ns5 = np.arange(-100,100,2.5)


t_prime = t - min(t) # time from 0

""" deeltjes dichtheid 0<R<10 m """
print "0<R<10m"
n_lepton = t_prime.compress((id>=2) & (id<=6) & (r < 10.) )
print "n = ", len(n_lepton)
print "dichtheid = ", len(n_lepton)/314.

R1 = 30.
R2 = 35.
print "%f < R < %f m" % (R1,R2)
n_lepton = t_prime.compress((id>=2) & (id<=6) & (r > R1) & (r < R2) )
n_gamma = t_prime.compress((id==1) & (r > R1) & (r < R2) )
print "n = ", len(n_lepton), len(n_gamma)
area = 3.14*(R2**2-R1**2)
print "area = %5.f m2. dichtheid_lepton = %1.3f dichtheid_photon = %1.3f " % (area,len(n_lepton)/area,len(n_gamma)/area)

#
# Plot een serie plot tussen 0.8 en 1.2 * R met daarin de aankomstijdhistogrammen voor cp en gamma's
#
Rvalues = [10., 20., 30., 50.]
for Rstep in Rvalues:
    gamma = t_prime.compress((id==1) & (r > .8*Rstep) & (r < 1.2*Rstep) & (phi > 0) & (phi < 0.01))
    electron = t_prime.compress((id==3) & (r > .8*Rstep) & (r < 1.2*Rstep)& (phi > 0) & (phi < 0.01))

    plt.figure()
    plt.hist(electron, bins=50, histtype='step')
    plt.hist(gamma, bins=50, histtype='step')
    plt.legend(['electron', 'gamma'])
    plt.title('R = '+str(Rstep))
    plt.show()

data.close()
