# pulseheight histogram
import tables
import matplotlib.pyplot as plt
from numpy import *

FILENAME = 's501_filtered_2014.h5'
data = tables.open_file(FILENAME,'r')

events = data.root.events
ph = events.col('pulseheights')

plt.figure()
plt.hist(ph[:,1], bins=arange(0,600,1), histtype='step', log=True)
plt.xlabel('pulseheight [mV]')
plt.ylabel('Counts')
plt.legend(['s501-2014 - pennink2010 filtering'])
plt.savefig('ph_hist_501_2014.png',dpi=200)