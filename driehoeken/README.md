Lio-project 2015/2016

Bepaal correlatie afstand station en zenithoekverdeling

*Analyse scripts*
driehoeken.py (output: driehoeken.csv) zoek geschikte driehoeken

download_data.py  download coincidenties
reconstruct.py    doet richtingsreconstructies voor de hele datastore

fit_triangles.py (ouput: driehoeken-fits.csv) maak zenithoekverdelingen en fit model

plot_oct_2016.py   maak plotjes voor verslag


*Datastore*
trave:  /data/hisparc/tom/Datastore/driehoeken
laptop: D:\\Datastore\\Driehoeken

2015full_x_y_z.h5  : heel 2015 per driehoek (x,y,z) [test dataset]
x_y_z_all.h5       : alle beschikbare coincidenties voor driehoek

*Extra*

fit_ciampa.py module die fits e.d. uitvoert
station_maps.py module die plaatjes maakt van (driehoeken van) stations op OSM kaart
test_C.py onderzoek verband C (Iyono) en zenithoekverdeling
