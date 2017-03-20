Op 13 maart zijn de (relatieve) hoogtes van de SPA stations opnieuw
bepaald dmv een kaart van de daken van het Science Park:
"Hoogtes van HiSPARC stations in het Science Park Array.pdf"


Deze hoogte beïnvloed de correctie van de station timing offsets.


AltitudeCorrectedStation => sapphire.api.Station object
In dit object worden de hoogte (altitude) in WGS84 van de stations vervangen
door de nieuwe hoogtes (hardcoded in AltitudeCorrectedStation.py).

Station.determing_station_timingoffset is overgeschreven met een een versie die
de offset corrigeerd t.o.v. de nieuwe hoogte. Let op: LANGZAAM, vanwege het
telkens opnieuw ophalen van de LLA coordinaten van de server. Gebruik
`force_stale=True` zoveel mogelijk. Vooral in reconstructies.

test_off.py: Test de uitkomsten. De offset van 510 met als referentie 501 is
ongeveer 13 ns, op 1jan2016. D.w.z. de GPS klok van 510 liep op die dag 13 ns
achter op de GPS klok van 501. 

test_reconstructions.py: Vergelijk het nieuwe en oude Station() object in
een reconstructie. (Zou weinig verschil moeten zijn)
