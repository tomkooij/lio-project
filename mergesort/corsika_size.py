import numpy as np
import matplotlib.pyplot as plt

# du -a /data/hisparc/corsika/data | grep DAT000000 | grep -v long
FILENAME = 'corsika.size.kbytes.txt'


def get_size(line):
    return int(line.split()[0])


if __name__ == '__main__':
    with open(FILENAME) as f:
        lines = f.readlines()

    # the first int is the size in kilobytes
    sizes = map(get_size, lines)

    for limit in [50, 60, 70, 80, 90, 95]:
        p = np.percentile(sizes, [0, limit])
        print "%d percent under %5.f MegaBytes" % (limit,
                                                   int(p[1] / 1000.))

    plt.figure()
    plt.hist(sizes, bins=np.logspace(2, 8), histtype='step')
    plt.xscale('log')
    plt.xlabel('size on disk (kiloBytes)')
    plt.ylabel('counts')
    plt.title('Sizes of CORSIKA output (DAT000000)')
    plt.savefig('corsika_sizes.png', dpi=200)
    plt.show()
