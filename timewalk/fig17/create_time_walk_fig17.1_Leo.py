# recreate figure 17.1 from Leo1987: Time walk
import numpy as np
import matplotlib.pyplot as plt

BASELINE = 700.
THRESHOLD = 650.
# pulseheight curve
t_r = 12. # [ns] rise time
t_f = 24. # [ns] fall time

V1 = lambda t: 1700*(np.exp(-t/t_r) -np.exp(-t/t_f))
V2 = lambda t: 1300*(np.exp(-t/(1.5*t_r)) -np.exp(-t/t_f))

x = np.arange(0,100,1)

y = np.append(np.array(20*[BASELINE]), 100*[BASELINE]+V1(x))
y2 = np.append(np.array(20*[BASELINE]), 100*[BASELINE]+V2(x))
y3 = 120*[THRESHOLD]

plt.figure()
plt.plot(y)
plt.plot(y2)
plt.plot(y3)
plt.ylim([200,750])
plt.axis('off')
plt.legend(['signal A','signal B'])
plt.savefig('fig17_1.svg', transparent=True)

plt.show()
