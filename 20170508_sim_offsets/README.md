20170805

Controleer detector timing offsets die door
 sapphire.simulations.GroundParticleSimulation worden gegenereerd (random)


GroundParticleSimulation slaat de (random) offsets op in:
`data.root.coincidences._v_attrs`

```python
cluster = data.get_node_attrs('/coincidences', 'cluster')
detectors = cluster.get_station(STATION).detectors
offsets = [d.offset for d in detectors]
```

Deze worden NIET meegenomen in de standaard ReconstructESDEvents()


Test:
Met de door GroundParticleSimulation gekozen offsets wordt de data (van
  nweiden) correct gereconstrueerd (azimuth verdeling is vlak, bij constante
    Energie van primair deeltje)

TODO:
- Schrijf:
  - ReconstuctSimulatedEvents()
  - ReconstructSimulatedCoincidences() met gps_offsets
