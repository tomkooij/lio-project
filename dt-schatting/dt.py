#
# maak een histogram van mogelijke aankomsttijd verschillen voor alle zenith
#  en azimuth hoeken
#

from __future__ import division

import numpy as np
import progressbar as pb
progress = pb.ProgressBar(widgets=[pb.Percentage(),pb.Bar(), pb.ETA()])
STAPPEN = 200

a = 10.  # m  Distance between detectors
c = 3.e-1  # m/ns speed of light

if __name__ == '__main__':

    dt_list = []

    for zenith in progress(np.arange(0,np.pi/2,np.pi/(2*STAPPEN))):

        # distributie van zenith hoeken BRON!?
        weging = 100.*np.sin(zenith)*(np.cos(zenith))**7.

        for azimuth in np.arange(0,2*np.pi,np.pi/(STAPPEN/2)):

            # tijdverschil behorende bij deze hoek combinatie (in ns)
            delta_t = a / c * np.sin(zenith)*np.cos(azimuth)

            # maak lijst met tijdsverschillen,
            # waarbij de tijdsverschillen met grote kans vaker voorkomen
            # en random "versmering" met sigma = 3.5ns
            for item in np.arange(0, weging, 1.):
                dt_list.append(delta_t + np.random.normal(0,2.0))

    print "gem, stddev = ",np.mean(dt_list), np.std(dt_list)
