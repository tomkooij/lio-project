Station (GPS) offset 102, 104, 105

Station 102 heeft "bad timestamps" (dwz onbruikbare) data van 1 sep 2014 tot 21 sep 2015 vanwege PySPARC/quantisation error: https://github.com/HiSPARC/datastore/issues/9

Maar de station offsets van 105-102 zijn lang na 21 sep 2015 nog "NaN":

(datetime.datetime(2013, 9, 17, 0, 0), 7.7000000000000002),
 (datetime.datetime(2013, 9, 18, 0, 0), 8.3000000000000007),
 (datetime.datetime(2013, 9, 19, 0, 0), 8.5),
 (datetime.datetime(2013, 9, 20, 0, 0), 13.1),
 (datetime.datetime(2013, 9, 21, 0, 0), nan),
 (datetime.datetime(2013, 10, 2, 0, 0), 3.3999999999999999),
 (datetime.datetime(2013, 10, 22, 0, 0), nan),
 (datetime.datetime(2016, 3, 15, 0, 0), 7.7000000000000002),
 (datetime.datetime(2016, 3, 17, 0, 0), 11.699999999999999),
 (datetime.datetime(2016, 3, 18, 0, 0), 12.199999999999999),
 (datetime.datetime(2016, 3, 19, 0, 0), 12.6),
 (datetime.datetime(2016, 3, 20, 0, 0), 12.300000000000001),

Maar 104-102 Klopt wel "gewoon".

14 nov 2016
===========
jan 2016: (coinc_102_105_jan_2016.h5)
18k coincidenties
timedelta's bepaald --> [] leeg!
Oorzaak: detector offsets van station 105 zijn NaN in jan 2016
Worden pas op 21 maart weer niet NaN

Onderzoek: (det.py): 1jan2016 events van 102 en 105.

determine_detector_timing_offsets() 105 -> 4*NaN.
102 werkt wel gewoon.

Probleem: 105 heeft van sep 2015 tot mrt 2016 "geen MPV piek"

find_mpv() testen voor data van 105 (1 jan 2016)

mpv.py --> test find_mpv()
102 -> lukt
105 -> fit fails, want "initial_guess" is fout. Kan ook niet in het algoritme.

related issue:
https://github.com/HiSPARC/sapphire/issues/32
