#
# Fit een histogram met een Gauss verdeling
#
# bron: http://stackoverflow.com/questions/7805552/
#
# Dit is een test file om een robuste manier voor het fitten van een histogram
#  met een Normale verdeling te regelen. norm.fit() bepaald simpelweg het gemiddelde
#  van de data en is dus niet bruikbaar. Ook heeft norm.fit() problemen met
#  niet genormaliseerde data
#
# Deze code leest een CSV met data in,
#  maakt een histogram
#  fit een willekeurige gauss verdeling met kleinste kwaderen (scipy.optimize.leastsq)
#  plot de verdeling in het histogram
# TODO: chi-kwadraten bereken
#
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import leastsq


#
# De normale (gauss) verdeling voor scipy.optimize.leastsq
#
fitfunc  = lambda p, x: p[0]*np.exp(-0.5*((x-p[1])/p[2])**2)
errfunc  = lambda p, x, y: (y - fitfunc(p, x))

#
# In deze file staan "delta-t", "ph_hoog", "ph_laag"
filename = "events_voor_jos.csv"
data     = np.loadtxt(filename,skiprows=1,delimiter=',')
delta_t  = data[:,0]
ph_low   = data[:,2]

#
# Selecteer data
#
PH_MIN = 40.
PH_MAX = 50.
selected_delta_t = delta_t.compress((ph_low > PH_MIN) & (ph_low <= PH_MAX) & (delta_t > -40.) & (delta_t < 20.))

#
# Bins die passen bij de 2.5ns timing van HiSPARC kastjes
#
bins_edges = np.arange(-41.25,21.25,2.5)

# Maak een histogram
#  n is nu een lijst met "counts"
#  bins zijn de bin "randen"
plt.figure()
n,bins,patches = plt.hist(selected_delta_t,bins=bins_edges,histtype='step')

#
# Middens van de bins:
#
middle = [(bins[i]+bins[i+1])/2 for i in range(len(bins)-1)]

# Least squares fit:
init  = [50.0, -10., 10.]

out   = leastsq( errfunc, init, args=(middle, n))
c = out[0]

print "exp[-0.5((x-mu)/sigma)^2]"
print "Fit Coefficients:"
print c[0],c[1],abs(c[2])

plt.plot(bins, fitfunc(c, bins),'r--', linewidth=3)
plt.title(r'$ PH = %3.f - %3.f \ \mu = %.3f\  \sigma = %.3f\ $' %(PH_MIN,PH_MAX,c[1],abs(c[2])));
plt.xlabel('pulseheight [ADC]')
plt.show()
