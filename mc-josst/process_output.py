#
# Process "minimontecarlo" by josst output
#   code in aparte github repo
#   zie "uitleg output.txt" in die repo voor uitleg outputfile
#
import matplotlib.pyplot as plt
import numpy as np

FILENAME = 'output_10k_photons.txt' # 10k photons 1/E distributed

def plot_Eloss_vs_Eprim(input_list):
    # maak een x,y scatter plot
    x = [event[0] for event in input_list] # E primair foton
    y = [event[3] for event in input_list] # E loss in detecor

    plt.figure()
    plt.scatter(x,y)
    plt.title('Energy loss in detector vs photon primaire energy')
    plt.xlabel('Eprimair [Mev]')
    plt.ylabel('Eloss [MeV]')


if __name__ == '__main__':

    events = []  # array of events
                    # single event = (Eprime, mechanism, x, Eloss)

    # lees de hele file. Verwijder \n en splits op spaties
    lines = [line.strip().split(' ') for line in open(FILENAME)]

    for line in lines:
        # selecteer de regels zonder + of #
        # (dan zijn de resultaten per primair foton over)
        # sla die op in events lijst
        if ((line[0][0] != "+") & (line[0][0] != '#')): # first char not + of #
            events.append(line)

    # Plot alle data
    plot_Eloss_vs_Eprim(events)

    # selecteer op mechanisme
    event_array = np.array(events)
    mechanism = event_array[:,1] # tweede kolom = mechanisme

    compton_events = event_array.compress(mechanism=='1',axis=0) # selecteer compton
    pair_events = event_array.compress(mechanism=='2',axis=0) # selecteer paar creatie


    plot_Eloss_vs_Eprim(pair_events)
