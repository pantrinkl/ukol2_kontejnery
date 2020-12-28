import json
from pyproj import CRS, Transformer
import math

geom_ad = []
geom_kon = []
ad_ulice = []
ad_num = []

with open("adresy.geojson", "r") as a:
    data = json.load(a)
    adresy = list(data['features'])
    for cast in adresy:
        geometrie = cast['geometry']['coordinates']
        geom_ad.append(geometrie)
        cislo = cast['properties']['addr:housenumber']
        ad_num.append(cislo)
        ulice = cast['properties']['addr:street']
        ad_ulice.append(ulice)

print("Načteno ",len(geom_ad)," adres.")

with open("kontejnery.geojson", "r") as k:
    data = json.load(k)
    kontejnery = list(data['features'])
    for cast in kontejnery:
        if cast['properties']['PRISTUP']=="volně":
            geometrie = cast['geometry']['coordinates']
            geom_kon.append(geometrie)

print("Načteno ",len(geom_kon)," kontejnerů.")

geom_ad_sjtsk = []

wgs = CRS.from_epsg(4326) # WGS-84
sjtsk = CRS.from_epsg(5514) # S-JTSK

wgs2jtsk = Transformer.from_crs(wgs,sjtsk)

for cast in geom_ad:
    geom_ad_sjtsk.append(wgs2jtsk.transform(cast[1], cast[0]))

vzdalenosti = []

for cast in geom_ad_sjtsk:
    mindl = 10000
    for kus in geom_kon:
        delka = math.sqrt(((cast[0]-kus[0])**2)+((cast[1]-kus[1])**2))
        if mindl > delka:
            mindl = delka
    vzdalenosti.append(mindl)

suma = sum(vzdalenosti)
prumer = suma/len(vzdalenosti)

indmax = vzdalenosti.index(max(vzdalenosti))

print("Průměrná vzdálenost ke kontejneru je",round(prumer),"m.")
print("Nejdelší vzdálenost ke kontejneru je z adresy",ad_ulice[indmax],ad_num[indmax],", a to",round(max(vzdalenosti)),"m.")
