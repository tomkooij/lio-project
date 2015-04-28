"""
to be moved from sapphire:groundparticle_gamma branch
to new refractored_groundparticles_gamma branch
"""

def simulate_detector_response(self, detector, shower_parameters):
    """Simulate detector response to a shower.

    Checks if particles have passed a detector. If so, it returns the number
    of particles in the detector and the arrival time of the first particle
    passing the detector.

    :param detector: :class:`~sapphire.clusters.Detector` for which
                     the observables will be determined.
    :param shower_parameters: dictionary with the shower parameters.

    """

    leptons, gammas = self.get_particles_in_detector(detector)
    n_leptons = len(leptons)
    n_gammas = len(gammas)

    if not n_leptons+n_gammas:
        return {'n': 0, 't': -999}

    if n_leptons:
        mips_lepton = self.simulate_detector_mips_for_leptons(leptons)
        leptons['t'] += self.simulate_signal_transport_time(n_leptons)
        first_signal = leptons['t'].min() + detector.offset
    else:
        mips_lepton = 0

    if n_gammas:
        mips_gamma = self.simulate_detector_mips_for_gammas(gammas)
        gammas['t'] += self.simulate_signal_transport_time(n_gammas)
        first_signal = gammas['t'].min() + detector.offset
    else:
        mips_gamma = 0

    return {'n': mips_lepton+mips_gamma, 't': self.simulate_adc_sampling(first_signal) }


def simulate_detector_mips_for_leptons(self, particles):
    """Simulate the detector signal for leptons

    :param particles: particle rows with the p_[x, y, z]
                      components of the particle momenta.

    """
    # determination of lepton angle of incidence
    theta = np.arccos(abs(particles['p_z']) /
                      np.sqrt(particles['p_x'] ** 2 +
                              particles['p_y'] ** 2 +
                              particles['p_z'] ** 2))
    n = len(particles)
    mips = self.simulate_detector_mips_leptons(n, theta)

    return mips

def simulate_detector_mips_for_gammas(self, particles):
    """Simulate the detector signal for gammas

    :param particles: particle rows with the p_[x, y, z]
                      components of the particle momenta.

    """

    p_gamma = np.sqrt(particles['p_x'] ** 2 + particles['p_y'] ** 2 +
            particles['p_z'] ** 2)

    # determination of lepton angle of incidence
    theta = np.arccos(abs(particles['p_z']) /
                      p_gamma)

    n = len(particles)
    mips = self.simulate_detector_mips_gammas(n, p_gamma, theta)

    return mips
