"""
to be moved from sapphire:groundparticle_gamma branch
to new refractored_groundparticles_gamma branch
"""

@classmethod
def simulate_detector_mips_leptons(cls, n, theta):
    """Simulate the detector signal for leptons

    Simulation of convoluted distribution of electron and
    muon energy losses with the scintillator response

    The detector response (energy loss and detector efficiency) is derived
    in Montanus2014.

    The energy loss is taken from the Bethe-Bloch equation. The detector
    response is statistically modelled. The effect of particle angle of
    incidence is accounted for. The resulting probability
    distribution is used below.

    The statistics can be simulated by taking a random number y between
    0 and 1, and convert it to a signal s in MIP using the probablity
    distribution.

    Montanus2014: J.C.M. Montanus, The Landau distribution, \
                      Internal note (Nikhef), 22 may 2014+


    Be careful when editting this function, be sure to check both
    the single and vectorized part.

    :param n: number of particles.
    :param theta: angle of incidence of the particles, as float or array.

    """
    costheta = np.cos(theta)
    y = np.random.random(n)

    if n == 1:
        if y < 0.3394:
            mips = (0.48 + 0.8583 * sqrt(y)) / costheta
        elif y < 0.4344:
            mips = (0.73 + 0.7366 * y) / costheta
        elif y < 0.9041:
            mips = (1.7752 - 1.0336 * sqrt(0.9267 - y)) / costheta
        else:
            mips = (2.28 - 2.1316 * sqrt(1 - y)) / costheta
    else:
        mips = np.where(y < 0.3394,
                        (0.48 + 0.8583 * np.sqrt(y)) / costheta,
                        (0.73 + 0.7366 * y) / costheta)
        mips = np.where(y < 0.4344, mips,
                        (1.7752 - 1.0336 * np.sqrt(0.9267 - y)) / costheta)
        mips = np.where(y < 0.9041, mips,
                        (2.28 - 2.1316 * np.sqrt(1 - y)) / costheta)
        mips = sum(mips)
    return mips

@classmethod
def simulate_detector_mips_gammas(cls, n, p, theta):
    """
    :param n: number of gammas.
    :param p: the momentum of the gammas as float or array
    :param theta: angle of incidence of the gammas, as float or array.
    """

    max_E = 4.0 # 2 MeV per cm * 2cm scintilator depth
    MIP = 3.38 # MeV
    P_pair_production = 0.015 # interaction probability for pair production

    # W.R. Leo (1987) p 54
    # E photon energy [MeV]
    # return compton edge [MeV]
    def _compton_edge(E):

        electron_rest_mass_MeV = .5109989 # MeV

        gamma = E / electron_rest_mass_MeV

        return (E * 2 * gamma / (1 + 2*gamma) )

    def _compton_energy_transfer(E):
        # from lio-project/photons/electron_energy_distribution.py

        # cumulative energy distribution implemented as table
        #   Energy, np.poly1d() fit
        #    from lio_project/photons/electron_energy_distribution.py
        Energy_table = np.array([\
                 0.100000 ,\
                 0.127427 ,\
                 0.162378 ,\
                 0.206914 ,\
                 0.263665 ,\
                 0.335982 ,\
                 0.428133 ,\
                 0.545559 ,\
                 0.695193 ,\
                 0.885867 ,\
                 1.128838 ,\
                 1.438450 ,\
                 1.832981 ,\
                 2.335721 ,\
                 2.976351 ,\
                 3.792690 ,\
                 4.832930 ,\
                 6.158482 ,\
                 7.847600 ,\
                 10.000000])

        transfer_function_table = [\
                [-0.095663 , 0.998190 , 0.042602],\
                [-0.104635 , 1.008633 , 0.040506],\
                [-0.109294 , 1.015132 , 0.038090],\
                [-0.107136 , 1.015115 , 0.035430],\
                [-0.095551 , 1.005781 , 0.032673],\
                [-0.072295 , 0.984547 , 0.030032],\
                [-0.036015 , 0.949579 , 0.027764],\
                [0.013328 , 0.900254 , 0.026124],\
                [0.074324 , 0.837384 , 0.025313],\
                [0.144294 , 0.763123 , 0.025434],\
                [0.219738 , 0.680594 , 0.026476],\
                [0.296884 , 0.593392 , 0.028324],\
                [0.372186 , 0.505081 , 0.030787],\
                [0.442678 , 0.418822 , 0.033635],\
                [0.506156 , 0.337141 , 0.036638],\
                [0.561214 , 0.261844 , 0.039593],\
                [0.607175 , 0.194044 , 0.042338],\
                [0.643960 , 0.134252 , 0.044755],\
                [0.671940 , 0.082499 , 0.046776],\
                [0.691794 , 0.038463 , 0.048368],
                [0.691794 , 0.038463 , 0.048368]]  # extra item E > 10

        idx = Energy_table.searchsorted(E, side='left')
        p = np.poly1d(transfer_function_table[idx])
        return p(np.random.random())*_compton_edge(E)

    def _compton_interaction_probability(E):
        return 0.134198 * np.exp(-0.392398*E) + 0.034156

    #p [eV]
    #E [MeV]
    E = p / 1.e6

    mips = 0
    for energy in E:

        # proces each foton
        """
        Dit moet beter: trek interactieplel uit een Emacht.
        """
        depth_compton = np.random.random()/_compton_interaction_probability(energy) # unit: scintilator depth
        depth_pair = np.random.random()/P_pair_production # 0.015 = P(pair production)
        #print "E, depth compton, pair = ", energy, depth_compton, depth_pair

        if ((depth_pair > 1.0) & (depth_compton > 1.0)):
            # no interaction
            continue

        #  interaction in scintilator
        if (depth_compton < depth_pair):
            """
            compton scattering
            """
            maximum_energy_deposit_in_MIPS = (1-depth_compton)*max_E/MIP
            energy_deposit_in_MIPS = _compton_energy_transfer(energy)/MIP
            extra_mips = np.minimum(maximum_energy_deposit_in_MIPS, energy_deposit_in_MIPS)  # maximise energy transfer per photon to 1 MIP/cm * depth

            # stdout output: Energy, k, interaction_probability, transfered_energy [mips]
            # print '*', photon[0], photon[1], photon[2], extra_mips

            mips += extra_mips

        elif (energy > 1.022):
            """
            pair production: Two "electrons"
            """
            maximum_energy_deposit_in_MIPS = (1-depth_pair)*max_E/MIP
            energy_deposit_in_MIPS = (energy - 1.022) / MIP # 1.022 MeV used for creation of two particles
            extra_mips = np.minimum(maximum_energy_deposit_in_MIPS, energy_deposit_in_MIPS)
            mips += extra_mips

    return mips
