# coding: utf-8
import tables
import matplotlib.pyplot as plt
import numpy as np
data = tables.open_file('n_hist.h5','r')
events = data.root.simrun.cluster_simulations.station_0.events
n1 = events.col('n1')
n2 = events.col('n2')
n3 = events.col('n3')
n4 = events.col('n4')

plt.hist(n1,bins=np.arange(0.1,4,0.1), histtype='step')
plt.hist(n2,bins=np.arange(0.1,4,0.1), histtype='step')
plt.hist(n3,bins=np.arange(0.1,4,0.1), histtype='step')
plt.hist(n4,bins=np.arange(0.1,4,0.1), histtype='step')
plt.legend(['n1','n2','n3','n4'])
plt.title('Simulated number of mips per detector (histogram)' )

plt.show()

"""
plt.hist(n1,bins=np.arange(0.1,4,0.1), histtype='step')
plt.show()
plt.hist(n2,bins=np.arange(0.1,4,0.1), histtype='step')
plt.show()
plt.hist(n3,bins=np.arange(0.1,4,0.1), histtype='step')
plt.show()
plt.hist(n4,bins=np.arange(0.1,4,0.1), histtype='step')
plt.show()
"""
