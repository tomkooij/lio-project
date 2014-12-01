#
# Process "minimontecarlo" by josst output
#   code in aparte github repo
#   zie "uitleg output.txt" in die repo voor uitleg outputfile
#
import matplotlib.pyplot as plt
import numpy as np

#FILENAME = 'output_10k_photons.txt' # 10k photons 1/E distributed
#FILENAME = 'output_100k_ZONDER_FE.txt' # no photo electric effect
#FILENAME = 'output_100k_photons.txt' # 100k photons 1/E distributed
#FILENAME = 'output_1M_photons.txt' # 500MEGS! 1M photons 1/E distributed
#FILENAME = 'output_10k_1MeV.txt' # 10k electronen met extra nfo zie process_electron.c
FILENAME = 'output_10k_electron_info.txt' # 10k electronen 1/E distr met extra nfo van process_electron.c

def plot_Eloss_vs_Eprim(input_list):
    # maak een x,y scatter plot
    x = [event[0] for event in input_list] # E primair foton
    y = [event[3] for event in input_list] # E loss in detecor

    plt.figure()
    plt.plot(x,y,'ob')
    plt.title('Energy loss in detector vs photon primaire energy')
    plt.xlabel('Eprimair [Mev]')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Eloss [MeV]')


#
# TK output lines (toegevoegd TK, 17nob2014)
# analyseer welke Eelec e.d. gekozen worden uit een dsigma/dT verdeling
#
def analyse_do_compton():

    compton_array = np.array(do_compton_output)

    # TK output line:
    # TK, channel, NCHAN, edge, Egamma, Eelec
    channel = compton_array[:,1].astype(np.float32)
    edge = compton_array[:,3].astype(np.float32)
    Egamma = compton_array[:,4].astype(np.float32)
    Eelec = compton_array[:,5].astype(np.float32)

    #hist(Egamma/Eelec,bins=100)
    plt.hist(Eelec/edge,bins=100)

#
# Eerste plotjes om te zien "wat er in output.txt zit"
#
def plot_output():
    # Plot alle data
    plot_Eloss_vs_Eprim(events)

    # selecteer op mechanisme
    event_array = np.array(events)
    mechanism = event_array[:,1] # tweede kolom = mechanisme

    FE_events = event_array.compress(mechanism=='0', axis=0) # select photo electric
    compton_events = event_array.compress(mechanism=='1',axis=0) # selecteer compton
    pair_events = event_array.compress(mechanism=='2',axis=0) # selecteer paar creatie

    plot_Eloss_vs_Eprim(pair_events)

# recreate figure 8 Josst june 2010

def Eloss_histogram():
    Egamma = event_array[:,0].astype(np.float32)
    Eloss = event_array[:,3].astype(np.float32)

    plt.figure()
    plt.hist(Eloss, bins=100, log=True, histtype='step')
    plt.title('Photon energy loss histogram')
    plt.xlabel('Eloss [Mev]')

#
# Plot the fraction of energy loss per foton
#
def plot_T():
    Egamma = event_array[:,0].astype(np.float32)
    Eloss = event_array[:,3].astype(np.float32)

    T = Eloss/Egamma

    plt.figure()
    plt.scatter(Egamma, T)
    plt.title('T vs Egamma')
    plt.ylabel('fraction of primary photon energy')
    plt.xlabel('Egamma [Mev]')
#    plt.xscale('log')

def E_histogram(Energy):

    kolom4 = Energy[:,3]

    plt.figure()
    plt.hist(kolom4, bins=100, histtype='step')
    plt.title('Photon energy loss histogram')
    plt.xlabel('Eloss [Mev]')

if __name__ == '__main__':

    global events
    events = []     # array of events
                    # single event = (Eprime, mechanism, x, Eloss)
    global do_compton_output
    global electron_output
    do_compton_output = [] # TK output of do_compton()
    electron_output = [] # T output of process_electron()

    # lees de hele file. Verwijder \n en splits op spaties
    lines = [line.strip().split(' ') for line in open(FILENAME)]

    for line in lines:
        # regels met TK zijn regels uit "do_compton()"
        if (line[0][0:2] == "TK"):
            do_compton_output.append(line)

        elif (line[0][0] == 'T'):
            electron_output.append(line[1:4]) # mechanisme, x*LOSS, T

        # selecteer de regels zonder + of #
        # (dan zijn de resultaten per primair foton over)
        # sla die op in events lijst
        elif ((line[0][0] != "+") & (line[0][0] != '#') & (line[0][0] != 'T')): # datalne
            events.append(line)# selecteer op mechanisme

    event_array = np.array(events).astype(np.float32)
    mechanism = event_array[:,1] # tweede kolom = mechanisme

    Egamma = event_array[:,0]

    E_100k_1MeV = event_array.compress(((Egamma > .1) & (Egamma < 1.)),axis=0)
    E_1MeV_2MeV = event_array.compress(((Egamma > 1.) & (Egamma < 2.)),axis=0)
    E_2MeV_5MeV = event_array.compress(((Egamma > 2.) & (Egamma < 5.)),axis=0)
    E_5MeV_10MeV = event_array.compress(((Egamma > 5.) & (Egamma < 10.)),axis=0)

    print 'ga je gang!\n'