# Úkol 2 - kontejnery

Tento program slouží k vypočtení průměru a mediánu vzdáleností k veřejným kontejnerům pro určené adresy.

Dále program nalezne adresu, ze které je vzdálenost ke kontejneru největší a vypíše ji.

## Vstupní parametry

Ve složce, kde je uložen `.py` soubor, je nutné mít další dva vstupní sobory:
* `adresy.geojson` - soubor ve formátu GeoJson, kde jsou uložené požadované adresy (např. čtvrtě).
* `kontejnery.geojson` - soubor ve formátu GeoJson, kde jsou uložené kontejnery požadované oblasti.

Pro funkčnost programu je nutné, aby souřadnice adres byly v systému WGS 84 (EPSG: 4326). Souřadnice kontejnerů musí naopak být v systému S-JTSK (EPSG: 5514)

Z tohoto repozitáře lze stáhnout vzorová data pro městskou čtvť Vršovice v Praze.

Soubory adres lze stáhnout například na stránkách [Overpass Turbo](http://overpass-turbo.eu/).
Data kontejnerů lze sáthnout na [pražském Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB)

## Výstup

Program vypíše průměr ze vzdáleností mezi adresami a nejbližšími kontejnery. Dále nalezne ze seznamu vzdáleností mediánovou hodnotu.

Vypsána je také adresa, ze které je vzdálenost ke kontejneru největší.

Na [stránce úkolu](https://github.com/xtompok/uvod-do-prg_20/tree/master/du02) se lze dozvědět zadání úkolu.