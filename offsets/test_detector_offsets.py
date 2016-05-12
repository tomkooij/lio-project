from numpy import *
from pylab import *
from sapphire.api import Station
from sapphire.analysis.calibration  import determine_detector_timing_offsets
from sapphire.utils import get_active_index
import tables

STATION = 501
START = 1420070400 # 2015,1,1
END   = 1451520000 # 2015,12,31

if __name__ == '__main__':

    apioffsets = Station(STATION, force_stale=True).detector_timing_offsets

    t = apioffsets['timestamp']

    idx1 = get_active_index(t, START)
    idx2 = get_active_index(t, END)

    t = t[idx1:idx2]
    o1 = apioffsets[idx1:idx2]['offset1']
    o2 = apioffsets[idx1:idx2]['offset2']
    o3 = apioffsets[idx1:idx2]['offset3']
    o4 = apioffsets[idx1:idx2]['offset4']

    calcoffsets = genfromtxt('detector_offsets_%d.tsv' % STATION) 

    ct = calcoffsets[:,0]
    co1 = calcoffsets[:,1]
    co2 = calcoffsets[:,2]
    co3 = calcoffsets[:,3]
    co4 = calcoffsets[:,4]


    figure()
    title('detector offsets old / new')
    ax1 = subplot(221)
    ax2 = subplot(222)
    ax3 = subplot(223)
    ax4 = subplot(224)

    ax1.plot(t, o1)
    ax1.plot(ct, co1)

    ax2.plot(t, o2)
    ax2.plot(ct, co2)
    ax2.legend(['api','curve_fit with sigma'])

    ax3.plot(t, o3)
    ax3.plot(ct, co3)

    ax4.plot(t, o4)
    ax4.plot(ct, co4)
    savefig('compare_det_offsets.png', dpi=200)
    show()


    figure()
    plot(t, o1)
    plot(ct, co1)
    legend(['api','curve_fit with sigma'])
    title('detector offsets, detector 1, ts = 1.435e9 - 1.440e9')
    ylabel('offset [ns]')
    xlabel('timestamp')
    xlim((1.435e9, 1.44e9))
    savefig('zoom.png', dpi=200)
    show()
