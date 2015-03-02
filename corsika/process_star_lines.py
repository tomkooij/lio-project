"""
# process_star_lines.py
#
# lees * regel uit corsika_run_sim.py om photon digitalisatie te analyseren
#
"""
import matplotlib.pyplot as plt
import numpy as np

FILENAME = 'output'

#
# lees * lines uit stdout output van corsika_run_sim.py
#
def read_input(filename):
    photons = []     # array of events
                    # single event = (E, k, kans, mips)

    lines = [line.strip().split(' ') for line in open(filename)]

    for line in lines:
        # regels met TK zijn regels uit "do_compton()"
        if (line[0] == "*"):
            photons.append(line)

    return photons

if __name__=='__main__':
    print 'Dit is process_star_lines.py'
    photons = np.array(read_input(FILENAME))

    E = photons[:,1]
    k = photons[:,2] # random getal
    p = photons[:,3] # interactie kans
    mips = photons[:,4]
