"""
from topaz/151013_cluster efficiency

Throw multiple showers on full Science Park Cluster
"""

from __future__ import division

from sapphire.qsub import check_queue, submit_job
from sapphire.utils import pbar


SCRIPT = """\
#!/usr/bin/env bash

python << END
import tables
from sapphire import HiSPARCStations, MultipleGroundParticlesSimulation

cluster = HiSPARCStations([501, 502, 503, 504, 505, 506, 508, 509])

result_path = '/data/hisparc/tom/science_park/multiple_showers_{job_id}.h5'
overview = '/data/hisparc/corsika/corsika_overview.h5'

with tables.open_file(result_path, 'w') as data:
    sim = MultipleGroundParticlesSimulation(overview, 600, 1e16, 10**17.5, cluster=cluster,
                                            data=data, N=100, progress=False)
    sim.run()
    sim.finish()
END
"""


def perform_simulations():
    for id in pbar(range(10)):
        script = SCRIPT.format(job_id=id)
        submit_job(script, 'spa_sim_%d' % id, 'long')


if __name__ == "__main__":
    perform_simulations()
