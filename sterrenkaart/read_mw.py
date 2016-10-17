# read milkyway.sol
# http://www.skymap.com/smp_overlays.htm#milky
import matplotlib.pyplot as plt
import numpy as np


def read_line(f):
    """ decode a line:
        DRAW 09 47 01, -47 24
        return action ('MOVE, DRAW, STOP'), ra, dec
    """
    l = f.readline().strip('\n')
    if len(l) == 0:
        return 'STOP', 0., 0.
    if l[0] == ';':  # comment
        return 'COMMENT', 0., 0.
    else:
        action, h, d, m, dec, decm = l.split()
        ra = float(h)+float(d)/60+float(m[:-1])/3600
        dec = float(dec)+float(decm)/60
        return action, ra, dec


def read_block(f):
    """ READ block:

        MOVE RA, DEC
        LINE RA, DEC
        ...
        DRAW RA, DEC
        <newline>
    """
    ra, dec = [], []
    action, readra, readdec = read_line(f)

    print('reading...')
    while action != 'STOP':
        ra.append(readra)
        dec.append(readdec)
        action, readra, readdec = read_line(f)
    return ra, dec


def read_blocks(f):
    ra, dec = read_block(f)
    while len(ra) > 0:
        yield ra, dec
        ra, dec = read_block(f)

with open('Milkyway.sol', 'r') as f:

    ax = plt.subplot(111, projection='mollweide')
    for ra, dec in read_blocks(f):
        ra_ = np.radians([(x / 24 * 360) - 180. for x in ra])
        dec_ = np.radians(dec)
        ax.set_xticklabels(['14h', '16h', '18h', '20h', '22h', '0h',
                            '2h', '4h', '6h', '8h', '10h'])
        ax.grid(True)
        ax.plot(ra_, dec_, color='grey')
    plt.show()
