from pylab import *
from numpy import loadtxt
from scipy.optimize import leastsq

fitfunc  = lambda p, x: p[0]*exp(-0.5*((x-p[1])/p[2])**2)+p[3]
errfunc  = lambda p, x, y: (y - fitfunc(p, x))

filename = "gaussdata.csv"
data     = loadtxt(filename,skiprows=1,delimiter=',')
xdata    = data[:,0]
ydata    = data[:,1]

init  = [1.0, 0.5, 0.5, 0.5]

out   = leastsq( errfunc, init, args=(xdata, ydata))
c = out[0]

print "A exp[-0.5((x-mu)/sigma)^2] + k "
print "Parent Coefficients:"
print "1.000, 0.200, 0.300, 0.625"
print "Fit Coefficients:"
print c[0],c[1],abs(c[2]),c[3]

plot(xdata, fitfunc(c, xdata))
plot(xdata, ydata)

title(r'$A = %.3f\  \mu = %.3f\  \sigma = %.3f\ k = %.3f $' %(c[0],c[1],abs(c[2]),c[3]));

show()