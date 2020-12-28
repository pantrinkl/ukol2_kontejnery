import json
from pyproj import CRS, Transformer
import math

geom_ad = []
geom_kon = []

with open("adresy.geojson", "r") as a:
    data = json.load(a)
    adresy = list(data['features'])
    for cast in adresy:
        geometrie = cast['geometry']['coordinates']
        geom_ad.append(geometrie)
    print(adresy[1])
    print(geom_ad[3])
with open("kontejnery.geojson", "r") as k:
    data = json.load(k)
    kontejnery = list(data['features'])
    for cast in kontejnery:
        if cast['properties']['PRISTUP']=="volně":
            geometrie = cast['geometry']['coordinates']
            geom_kon.append(geometrie)
    print(kontejnery[1])
    print(geom_kon[3])

geom_ad_sjtsk = []

wgs = CRS.from_epsg(4326) # WGS-84
sjtsk = CRS.from_epsg(5514) # S-JTSK

wgs2jtsk = Transformer.from_crs(wgs,sjtsk)

for cast in geom_ad:
    geom_ad_sjtsk.append(wgs2jtsk.transform(cast[1], cast[0]))
print(geom_ad_sjtsk[2])

vzdalenosti = []

for cast in geom_ad_sjtsk:
    mindl = 10000
    for kus in geom_kon:
        delka = math.sqrt(((cast[0]-kus[0])**2)+((cast[1]-kus[1])**2))
        if mindl > delka:
            mindl = delka
    vzdalenosti.append(mindl)
print(min(vzdalenosti))
print(max(vzdalenosti))
