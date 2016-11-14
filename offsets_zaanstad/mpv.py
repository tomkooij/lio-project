# coding: utf-8
import tables
import numpy as np

from sapphire.analysis.find_mpv import FindMostProbableValueInSpectrum

sn = 105

FILENAME = '1jan2016_s%d.h5' % sn
node = '/s%d/events' % sn

with tables.open_file(FILENAME, 'r') as data:

    events = data.get_node(node)
    print('number of events: ', len(events))

    e = events.read()
    integrals = e['integrals'].T
    print('integrals[0][0:10] = ', integrals[0][0:10])
    n, bins = np.histogram(integrals[0], bins=np.linspace(0,5000, 201))

    find_mpv = FindMostProbableValueInSpectrum(n, bins)
    find_mpv.find_mpv()
