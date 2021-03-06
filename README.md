# Úkol 2 - kontejnery

Tento program slouží k vypočtení průměru a mediánu vzdáleností k veřejným kontejnerům pro určené adresy.

Dále program nalezne adresu, ze které je vzdálenost ke kontejneru největší a vypíše ji.

## Vstupní parametry

Ve složce, kde je uložen `.py` soubor, je nutné mít další dva vstupní sobory:

* `adresy.geojson` - soubor ve formátu GeoJSON, kde jsou uložené požadované adresy (např. čtvrtě).\
Nutné atributy pro každou adresu:\
`"addr:housenumber"` - číslo domu\
`"addr:street"` - název ulice\
Souřadnice adres musí být uvedeny v systému WGS 84 (EPSG: 4326).

* `kontejnery.geojson` - soubor ve formátu GeoJSON, kde jsou uložené kontejnery požadované oblasti.\
Nutné atributy pro každý kontejner:\
`"PRISTUP"` - zda je kontejner volně příštupný\
Souřadnice kontejnerů musí být v systému S-JTSK (EPSG: 5514).

Pokud máte data uložená v jiných souborech, lze je při spuštění programu zadat. Přidáním argumentu `-a <nazev_souboru>` zvolíte soubor s adresami. Argumentem `-k <nazev_souboru>` vložíte název souboru s kontejnery. Při nedodání argumentů při spuštění programu je předpokládáno, že se soubory jmenují, jak jsou nazvány výše.

Z tohoto repozitáře lze stáhnout vzorová data pro městskou čtvť Vršovice v Praze.

Soubory adres lze stáhnout například na stránkách [Overpass Turbo](http://overpass-turbo.eu/).
Data kontejnerů lze stáhnout na [pražském Geoportálu](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB).

## Výstup

Program vypíše průměr ze vzdáleností mezi adresami a nejbližšími kontejnery. Dále nalezne ze seznamu vzdáleností mediánovou hodnotu.

Vypsána je také adresa, ze které je vzdálenost ke kontejneru největší.

Na [stránce úkolu](https://github.com/xtompok/uvod-do-prg_20/tree/master/du02) se lze dozvědět zadání úkolu.