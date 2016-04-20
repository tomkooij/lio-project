from numpy import  *
from pylab import *
import glob


if __name__ == '__main__':
    legenda = []
    figure()
    ion()
    ax1 = subplot(121)
    ax2 = subplot(122)
    ax1.set_xlabel('timestamp')
    ax2.set_xlabel('timestamp')
    ax1.set_title('502-ref501 station timing offsets')
    ax2.set_title('reduced Chi^2')
    for path in glob.glob('*.npy'):
        print path
        x = load(path)
        try:
            ts = x[:,0]
            offsets = x[:,1]
            rchi2 = x[:,2]
        except:
            ts = x['timestamp']
            offsets = x['offset']
            rchi2 = x['rchi2']
        ax1.plot(ts, offsets)
        ax2.plot(ts, rchi2)
        legenda.append(path)
    legend(legenda)
    show()
