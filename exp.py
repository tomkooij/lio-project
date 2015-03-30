# vergelijk exponentiele verdeling
#
#
import numpy as np
import matplotlib.pyplot as plt
import random
#
# Neem een gemiddelde dat niet 0, 1 ofzo iets is
#
AVERAGE = 25.
N = 10000 # number of numbers drawn
BINS = 20
bins = np.arange(0,200,10)

"""random.expovariatE(lamb=1./average) """
x_expovariate = [random.expovariate(1./AVERAGE) for x in range(N)]
""" josst LIBRAN  x = -AVERAGE * ln (random()"""
x_jos = [-1.*AVERAGE*np.log(random.random()) for x in range(N)]


# plot histograms
n1= plt.hist(x_expovariate, bins=bins, histtype='step')
n2=plt.hist(x_jos, bins=bins, histtype='step')
plt.title('random number drawn from exponential distribution lambda=1/25')
plt.legend(['random.expovariate()','josst libran.c -1/lambda*log(random())'])
plt.savefig('compare_exponential.png', dpi=200 )
plt.show()
