import numpy as np
import matplotlib.pyplot as plt

# du -a /data/hisparc/corsika/data | grep DAT000000 | grep -v long
# du -a /data/hisparc/corsika/data | grep corsika.h5
DATASETS = [('corsika.h5.size.kbytes.txt', 'corsika.h5'),
            ('corsika.size.kbytes.txt', 'DAT0000000')]


def get_size(line):
    """ return size in MegaBytes """
    return int(line.split()[0]) // 1000


def make_plot(filename, description):
    with open(filename) as f:
        lines = f.readlines()

    # the first int is the size in kilobytes
    sizes = map(get_size, lines)

    print 32 * "-"
    print "dataset: ", description
    for limit in [50, 60, 70, 80, 90, 95]:
        p = np.percentile(sizes, [0, limit])
        print "%d percent under %d MegaBytes" % (limit, int(p[1]))

    plt.figure()
    plt.hist(sizes, bins=np.logspace(1, 5), histtype='step')
    plt.axvline(1000, color='r', linestyle='dashed', linewidth=2)
    plt.xscale('log')
    plt.xlabel('size on disk (MBytes)')
    plt.ylabel('counts')
    plt.title('Sizes of outputfiles (%s)\nVertical line = 1GB' % description)
    plt.savefig('corsika_sizes_%s.png' % description, dpi=200)
    plt.show()


if __name__ == '__main__':
    for dataset in DATASETS:
        filename, description = dataset
        make_plot(filename, description)
