#
# Process "minimontecarlo" by josst output
#   code in aparte github repo
#   zie "uitleg output.txt" in die repo voor uitleg outputfile
#
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import latexify

#FILENAME = 'output_10k_photons.txt' # 10k photons 1/E distributed
#FILENAME = 'output_100k_ZONDER_FE.txt' # no photo electric effect
FILENAME = 'output_100k_photons.txt' # 100k photons 1/E distributed
#FILENAME = 'output_1M_photons.txt' # 500MEGS! 1M photons 1/E distributed
#FILENAME = 'output_10k_1MeV.txt' # 10k electronen met extra nfo zie process_electron.c
#FILENAME = 'output_10k_electron_info.txt' # 10k electronen 1/E distr met extra nfo van process_electron.c


def percentage(part, whole):
    return 100 * float(part)/float(whole)

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
# 2D histogram voor E *per interactie type*
#
def plot_Eloss_vs_Eprim(input_list, figtitle, figname):
    # maak een x,y scatter plot
    x = np.array([event[0] for event in input_list]).astype(np.float32) # E primair foton
    y = np.array([event[3] for event in input_list]).astype(np.float32) # E loss in detecor


    plt.figure()
    plt.plot(x,y,'ob')
    plt.title(figtitle)
    plt.xlabel('Photon energy [Mev]')
    plt.xscale('log')
    plt.ylabel('Energy transferd to detector [MeV]')
    plt.savefig(figname)

#
# 2D histogram voor Eloss *per interactie type*
#
def hist2d_Eloss_vs_Eprim(input_list, figtitle, figname):
    x = np.array([event[0] for event in input_list]).astype(np.float32) # E primair foton
    y = np.array([event[3] for event in input_list]).astype(np.float32) # E loss in detecor

    plt.figure()
#    plt.xscale('log') # DIT WERKT NIET!!??!!
    plt.hist2d(x,y,bins=30, norm=LogNorm())
    plt.title(figtitle)
    plt.xlabel('Photon energy [Mev]')
    plt.ylabel('Energy transferd to detector [MeV]')
    plt.colorbar()
    plt.savefig(figname, rasterized=True)


#
# Maak plots per mechanisme
#
def plots_per_mechanism():


    # selecteer op mechanisme
    event_array = np.array(events)
    mechanism = event_array[:,1] # tweede kolom = mechanisme

    FE_events = event_array.compress(mechanism=='0', axis=0) # select photo electric
    compton_events = event_array.compress(mechanism=='1',axis=0) # selecteer compton
    pair_events = event_array.compress(mechanism=='2',axis=0) # selecteer paar creatie


    print "Ik maak grafieken (duurt even..)"

    # FE-effect
    plot_Eloss_vs_Eprim(FE_events, 'FE', 'fig-fe-scatter.pdf')
    hist2d_Eloss_vs_Eprim(FE_events, 'FE', 'fig-fe-hist2d.pdf')
    #compton
    plot_Eloss_vs_Eprim(compton_events, 'Compton', 'fig-compton-scatter.jpg') # jpg wegens te langzaam en groot als vector object
    hist2d_Eloss_vs_Eprim(compton_events, 'Compton', 'fig-compton-hist2d.pdf')
    #paarvormign
    plot_Eloss_vs_Eprim(pair_events, 'Paarvorming', 'fig-pair-scatter.jpg') # jpg wegens te groot als vector object
    hist2d_Eloss_vs_Eprim(pair_events, 'Paarvorming', 'fig-pair-hist2d.pdf')



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



def foton_percentages():
    # alle data voor "photons.tex"
    #  Simulatie van photon detectie in hisparc

    # zorg voor de juiste inputfile
    #TOTAAL_GENERATED = 65348 # in 10k photon run
    TOTAAL_GENERATED = 651075 # 100k photon

    # selecteer op mechanisme
    event_array = np.array(events)
    mechanism = event_array[:,1] # tweede kolom = mechanisme

    FE_events = event_array.compress(mechanism=='0', axis=0) # select photo electric
    compton_events = event_array.compress(mechanism=='1',axis=0) # selecteer compton
    pair_events = event_array.compress(mechanism=='2',axis=0) # selecteer paar creatie

    TOTAAL = event_array.size/4

    #
    # Tabel 1: aantal fotonen per mechanisme en percentages
    #

    print "Totaal %d primaire fotonen gegenereerd. %d detected (%f procent)" % (TOTAAL_GENERATED, TOTAAL, percentage(TOTAAL, TOTAAL_GENERATED))

    # eventtabel heeft 4 items, dus delen door 4
    print "Alleen FE:", FE_events.size/4, percentage(FE_events.size/4,TOTAAL)
    print "Alleen Compton:", compton_events.size/4, percentage(compton_events.size/4,TOTAAL)
    print "Alleen Paarvorming:", pair_events.size/4, percentage(pair_events.size/4,TOTAAL)

def Eloss_in_detector_histrogram():
    #
    # Figuur 1: energie verlies in detector histogram
    #
    Eloss = np.array([event[3] for event in event_array]).astype(np.float32)

    plt.figure()
    plt.hist(Eloss, bins=np.linspace(0.,10.,21), log=True, histtype='step')
    plt.title('Photon energy loss in detector histogram')
    plt.xlabel('Energy lost [MeV]')
    plt.savefig('../papers/fig-Eloss-hist.pdf')

#
# Lees input file
#
# lelijke code met veel globals...
#

def read_input():
    global events
    events = []     # array of events
                    # single event = (Eprime, mechanism, x, Eloss)
    global event_array

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

def genereer_alle_data_voor_paper():
    foton_percentages()
    Eloss_in_detector_histrogram()

if __name__ == '__main__':

    print 'reading:', FILENAME
    read_input()

    #mechanism = event_array[:,1] # tweede kolom = mechanisme

    #Egamma = event_array[:,0]

    #E_100k_1MeV = event_array.compress(((Egamma > .1) & (Egamma < 1.)),axis=0)
    #E_1MeV_2MeV = event_array.compress(((Egamma > 1.) & (Egamma < 2.)),axis=0)
    #E_2MeV_5MeV = event_array.compress(((Egamma > 2.) & (Egamma < 5.)),axis=0)
    #E_5MeV_10MeV = event_array.compress(((Egamma > 5.) & (Egamma < 10.)),axis=0)

    print 'ga je gang!\n'
#    genereer_alle_data_voor_paper()
