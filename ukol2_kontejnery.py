import json
from pyproj import CRS, Transformer
import math
from statistics import median
from sys import exit
from argparse import ArgumentParser

# nacteni dat z geoJSONu
def nacti_json(adresy):
    try:
        with open(adresy, "r") as a:
            data = json.load(a)
            polozky = list(data['features'])
            return polozky
    except FileNotFoundError:
        exit("Nenalezen soubor s adresami.")
    except PermissionError:
        exit("Nemám přístup k souboru s adresami.")

# extrakce ulice, c.p. a souradnic adres
def extrakce_adres(data):
    geom = []
    cp = []
    ulicky = []
    # extrakce dat pro kazdou adresu
    for cast in data:
        geometrie = cast['geometry']['coordinates']
        geom.append(geometrie)
        cislo = cast['properties']['addr:housenumber']
        cp.append(cislo)
        ulice = cast['properties']['addr:street']
        ulicky.append(ulice)
    # vraceni seznamu souradnic, c.p. a ulice
    return geom, cp, ulicky

# extrakce souradnic kontejneru
def extrakce_kontejneru(data):
    geom = []
    # extrakce souradnic kazdeho kontejneru
    for cast in data:
        if cast['properties']['PRISTUP']=="volně":
            geometrie = cast['geometry']['coordinates']
            geom.append(geometrie)
    # vraceni souradnic
    return geom

# vypocet vzdalenosti k nejblizsimu kontejneru
def vypocet_vzdalenosti(adresy, kontejnery):
    vzdalenosti = []
    # pro kazdou adresu
    for cast in adresy:
        #  nastavime nejblizsi kontejner na 10 km
        mindl = 10001
        # a projedeme kontejnery
        # pokud je vzdalenost pod 10 km, nahradime nejblizsi kontejner timto
        for kus in kontejnery:
            delka = math.sqrt(((cast[0]-kus[0])**2)+((cast[1]-kus[1])**2))
            if mindl > delka:
                mindl = delka
        # pokud je stale vzdalenost k nejblizsimu 10 km, je jasne, ze adresa je ponekud daleko.
        if mindl == 10001:
            print("Nejbližší kontejner je pro některou adresu dále než 10 km. Nastala chyba, končím.")
            quit()
        vzdalenosti.append(mindl)
    # vraceni vzdalenosti adres k nejblizsimu kontejneru
    return vzdalenosti

# nacteni adres vstupnich souboru
parser = ArgumentParser(description="Nacteni vstupnich souboru")

parser.add_argument("-a", dest="adresy", required=False,
                    help="jmeno souboru s adresami", type = str)
parser.add_argument("-k", dest="kontejnery", required=False,
                    help="jmeno souboru s kontejnery", type = str)

args = parser.parse_args()

# pokud uzivatel nedodal adresy, predpokladame pudvodni nazvy
if args.adresy == None:
    args.adresy = "adresy.geojson"

if args.kontejnery == None:
    args.kontejnery = "kontejnery.geojson"

# otevreni jsonu s adresami, extrakce adres a jejich souradnic
ad_polozky = nacti_json(args.adresy)
geom_ad, ad_num, ad_ulice = extrakce_adres(ad_polozky)

print("Načteno ",len(geom_ad)," adres.")

# otevreni jsonu s kontejnery, extrakce jejich souradnic
kon_polozky = nacti_json(args.kontejnery)
geom_kon = extrakce_kontejneru(kon_polozky)

print("Načteno ",len(geom_kon)," kontejnerů.")

# prevedeni souradnic adres do S-JTSK
geom_ad_sjtsk = []

wgs = CRS.from_epsg(4326) # WGS-84
sjtsk = CRS.from_epsg(5514) # S-JTSK

wgs2jtsk = Transformer.from_crs(wgs,sjtsk)

for cast in geom_ad:
    geom_ad_sjtsk.append(wgs2jtsk.transform(cast[1], cast[0]))

# vypocet vzdalenosti k nejblizsimu kontejneru pro kazdou adresu
vzdalenosti = vypocet_vzdalenosti(geom_ad_sjtsk, geom_kon)

# vypocet statistickych hodnot z vzdalenosti
suma = sum(vzdalenosti)
prumer = suma/len(vzdalenosti)
vz_median = median(vzdalenosti)

# nalezeni indexu adresy s nejvetsi vzdalenosti ke kontejneru
indmax = vzdalenosti.index(max(vzdalenosti))

# vypsani dulezitych dat
print(f"Průměrná vzdálenost ke kontejneru je {prumer:.0f} m.")
print(f"Medián vzdáleností ke kontejneru je {vz_median:.0f} m.")
print("Nejdelší vzdálenost ke kontejneru je z adresy",ad_ulice[indmax],ad_num[indmax],f"a to {max(vzdalenosti):.0f} m.")
