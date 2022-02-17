# Lexmeter
 
Script Python pour analyser les dissymétries d'un corpus lexicométrique et voir si deux partitions se recoupent.

Script réalisé par Octave Julien (Pireh / Lamop - Université Paris 1 Panthéon-Sorbonne), février 2022.

## Fonctionnement détaillé
Lexmeter charge un corpus au format XML (un fichier unique ou des fichiers multiples rassemblés dans un dossier). Il faut indiquer quelle balise sert à identifier dans le corpus les textes à considérer (`<text>` par exemple, sans les chevrons). Il faut ensuite préciser quels attributs présents dans ces balises doivent être pris en compte. Ces attributs sont ceux utilisés pour définir des partitions du corpus. 

Lexmeter identifie les différentes valeurs prises par ces attributs (c'est-à-dire les différentes parties des partitions correspondantes), compte le nombre de textes correspondant à chaque paire de valeurs des deux attributs, et calcule leur longueur cumulée. Les résulats se présentent sous la forme d'un tri croisé permettant de voir les correspondances entre les parties des deux partitions.

Le tri croisé peut enfin être exporté aux formats csv (colonnes séparées par des points virgules), html, ou tex.

## Dépendances
Lexmeter utilise les librairies BeautifulSoup et Prettytable, qui peuvent être installées avec pip :

`pip3 install prettytable`

`pip3 install beautifulsoup4`
## Utilisation
Le script peut être utilisé de trois manières :

### Mode interactif
Lancer le script avec l'interpréteur Python avec la commande :

`python3 Lexmeter.py`

Le script demandera ensuite les différents paramètres de l'analyse.

### En ligne de commande
Les paramètres peuvent être indiqués directement en ligne de commande. Par exemple :

`python3 Lexmeter.py -f /chemin/du/corpus.xml -export /chemin/du/tableau/de/resultats.csv -t text -a1 attribut1 -a2 attribut2`

* `-f` 		Chemin du corpus (dossier ou fichier XML)
* `-export` Chemin du fichier à créer pour exporter le tableau de résultats
* `-t`	Balise utilisée dans le corpus pour délimiter les textes
* `-a1`	Premier attribut à croiser
* `-a2`	Second attribut à croiser

### Comme un module importé
En important le script comme un module dans un autre scrypt Python avec

`import Lexmeter`

il est possible d'invoquer la fonction lexmeter() avec les paramètres requis.