import json
from pyproj import CRS, Transformer
import math
from statistics import median

def extract_adres(polozka):
    geom_ad = []
    ad_num = []
    ad_ulice = []
    data = json.load(polozka)
    adresy = list(data['features'])
    for cast in adresy:
        geometrie = cast['geometry']['coordinates']
        geom_ad.append(geometrie)
        cislo = cast['properties']['addr:housenumber']
        ad_num.append(cislo)
        ulice = cast['properties']['addr:street']
        ad_ulice.append(ulice)
    return geom_ad, ad_num, ad_ulice

def extract_kontejner(polozka):
    geom_kon = []
    data = json.load(polozka)
    kontejnery = list(data['features'])
    for cast in kontejnery:
        if cast['properties']['PRISTUP']=="volně":
            geometrie = cast['geometry']['coordinates']
            geom_kon.append(geometrie)
    return geom_kon

def vypocet_vzdalenosti(adresy, kontejnery):
    vzdalenosti = []
    for cast in adresy:
        mindl = 10000
        for kus in kontejnery:
            delka = math.sqrt(((cast[0]-kus[0])**2)+((cast[1]-kus[1])**2))
            if mindl > delka:
                mindl = delka
        if mindl == 10000:
            print("Nejbližší kontejner je pro některou adresu dále než 10 km. Nastala chyba, končím.")
            quit()
        vzdalenosti.append(mindl)
    return vzdalenosti

with open("adresy.geojson", "r") as a:
    geom_ad, ad_num, ad_ulice = extract_adres(a)

print("Načteno ",len(geom_ad)," adres.")

with open("kontejnery.geojson", "r") as k:
    geom_kon = extract_kontejner(k)

print("Načteno ",len(geom_kon)," kontejnerů.")

geom_ad_sjtsk = []

wgs = CRS.from_epsg(4326) # WGS-84
sjtsk = CRS.from_epsg(5514) # S-JTSK

wgs2jtsk = Transformer.from_crs(wgs,sjtsk)

for cast in geom_ad:
    geom_ad_sjtsk.append(wgs2jtsk.transform(cast[1], cast[0]))

vzdalenosti = vypocet_vzdalenosti(geom_ad_sjtsk, geom_kon)

suma = sum(vzdalenosti)
prumer = suma/len(vzdalenosti)
vz_median = median(vzdalenosti)

indmax = vzdalenosti.index(max(vzdalenosti))

print("Průměrná vzdálenost ke kontejneru je",round(prumer),"m.")
print("Medián vzdáleností ke kontejneru je",round(vz_median),"m.")
print("Nejdelší vzdálenost ke kontejneru je z adresy",ad_ulice[indmax],ad_num[indmax],", a to",round(max(vzdalenosti)),"m.")
