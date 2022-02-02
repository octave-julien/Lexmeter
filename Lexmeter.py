import os
from string import punctuation
from re import split
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable
import  argparse


def encadre(chaine):
    '''Affiche un message encadré.'''
    l=len(chaine)
    resultat="+"+(l+2)*"-"+"+\n"
    resultat=resultat+"| "+chaine+" |\n"
    resultat=resultat+"+"+(l+2)*"-"+"+"
    print(resultat)


def ouvreCorpus(cheminCorpus):
    """Charge le corpus indiqué par cheminCorpus
    -Il peut s'agir d'un fichier XML unique ou d'un
     dossier contenant plusieurs fichiers XML."""
    corpusEntier=''
    if os.path.isdir(cheminCorpus)==True:
        os.chdir(cheminCorpus)
        listeFichiersCorpus=os.listdir(cheminCorpus)
        for fichierCorpus in listeFichiersCorpus:
            extension=os.path.splitext(fichierCorpus)[1]
            if extension=='.xml':
                contenuFichierCorpus = open(fichierCorpus, 'r').read()
                corpusEntier=corpusEntier+"\n"+contenuFichierCorpus
        if corpusEntier=='':
            print("-!- Aucun fichier XML ou fichiers XML vides dans "+cheminCorpus)
            return(False)
        return(corpusEntier)
    elif os.path.isfile(cheminCorpus)==True:
        contenuFichierCorpus=open(cheminCorpus,'r').read()
        return(contenuFichierCorpus)
    else:
        return False

def listeTextes(corpus, baliseStructure):
    """Retourne l'ensemble des textes du corpus sous forme de liste.
    -Le corpus est fourni sous forme d'une chaîne de caractères.
    -baliseStructure est la balise à utiliser pour identifier les
    textes (ou autre unité de structure) à considérer."""
    corpus=bs(corpus, features="lxml")
    listeDesTextes=corpus.findAll(baliseStructure)
    if len(listeDesTextes) == 0:
        print(f"-!- Aucune balise <{baliseStructure}> trouvée dans le corpus.\n\n")
        return False
    return(listeDesTextes)


def listerAttributs(listeDesTextes):
    """Enregistre dans la variable globale compteurAttributs
       le dénombrement des attributs utilisés dans le corpus.
       -listeDesTextes est une liste de textes sous forme d'éléments
        XML (balises et texte)
       -compteurAttributs prend la forme d'un dictionnaire associant
        à chaque attribut rencontré le nombre de textes où il figure."""
    global compteurAttributs
    compteurAttributs = {}
    for texte in listeDesTextes:
        attributs=texte.attrs
        nomsAttributs=attributs.keys()
        for nomAttribut in nomsAttributs:
            #print nomAttribut
            if nomAttribut in compteurAttributs: # Remplace has_key()
                #print "Key trouvée"
                compteurAttributs[nomAttribut]+=1
            else:
                compteurAttributs[nomAttribut]=1
    return(compteurAttributs)

def listeValeurs(nomAttribut, listeDesTextes):
    """Renvoie sous forme de liste les différents attributs rencontrés
       dans les textes de listeDesTextes."""
    valeursPossibles=[]
    for texte in listeDesTextes:
        if texte.has_attr(nomAttribut):
            valeur=texte.get(nomAttribut)
            if valeur not in valeursPossibles:
                valeursPossibles.append(valeur)
    return(valeursPossibles)
            
def creerTC(attr1,attr2, listeDesTextes):
    """Renvoie un tri croisé indiquant le nombre de textes et leur
    longueur cumulée pour chaque couple de valeurs des attributs
    attr1 et attr2, à partir des textes enregistrés dans listeDesTextes."""
    valsAttr1 = listeValeurs(attr1, listeDesTextes)
    valsAttr2 = listeValeurs(attr2, listeDesTextes)
    tc={}
    for valAttr1 in valsAttr1:
        ligne={}
        for valAttr2 in valsAttr2:
            ligne[valAttr2]=[0,0]
        tc[valAttr1]=ligne
    for texte in listeDesTextes:
        attr1_ceTexte = texte.get(attr1)
        attr2_ceTexte = texte.get(attr2)
        if attr1_ceTexte != None and attr2_ceTexte != None:
            longueur = longueurTexte(texte)
            tc[attr1_ceTexte][attr2_ceTexte][0] += 1
            tc[attr1_ceTexte][attr2_ceTexte][1] += longueur
    return(tc)

def longueurTexte(texte):
    '''Renvoie la longueur d'un texte en tant que nombre de mots.'''
    texte=texte.text
    for signe in punctuation:
        texte=texte.replace(signe, " ")
    nbMots=len(split(r' +',texte))
    return(nbMots)

def mettreEnFormeTC(tc):
    resultat=[]
    valsAttr1 = list(tc.keys())
    premiereCle = valsAttr1[0]
    valsAttr2 = list(tc[premiereCle].keys())
    valsAttr1.sort()
    valsAttr2.sort()
    
    enTetesLignes=tuple(valsAttr1) # Il faut une version immutable pour que l'utilisation des dictionnaires plus bas marche bien.
    enTetesCol=list(valsAttr2)
    enTetesCol.insert(0,"")
    resultat.append(enTetesCol)
    enTetesCol=enTetesCol[1:]
    enTetesCol=tuple(enTetesCol)
    for valLigne in enTetesLignes:
        ligne=[]
        ligne.append(valLigne)
        for valCol in enTetesCol:
            ligne.append(tc[valLigne][valCol])
        resultat.append(ligne)
    return(resultat)
    
def afficheTC(tc): # A refaire pour éviter d'utiliser prettytable
    """Transforme et affiche le tri croisé des attributs.
    -Affiche dans chaque cellule la longueur des textes et leur nombre
    entre parenthèse.
    -Nécessite le module PrettyTable"""
    tc2=list(tc)
    table=PrettyTable(tc2[0])
    for i in range(1,len(tc2)):
        for j in range(1,len(tc2[i])):
            tc2[i][j]=str(tc2[i][j][1])+" ("+str(tc2[i][j][0])+")"
        #tc2[i].insert(0,tc2[i][0])
        table.add_row(tc2[i])
    print(table)

def exporteResultatLexmeter(tc, fichier, format="csv"):
    """Fonction principale d'export du tri croisé dans un fichier.
    -tc est le tri croisé généré par lexmeter().
    -fichier est le chemin du fichier à créer.
    -format est le format du fichier (csv -par défaut-, html ou tex).
    -les fichiers csv utilisent le point-virgule comme séparateur
    de colonnes."""
    contenuExport = ""
    if format.lower() == "csv":
        for ligne in tc:
            contenuExport = contenuExport + ";".join(ligne) + "\n"
    if format.lower() == "html":
        contenuExport = "<table>\n"
        for ligne in tc:
            contenuExport = contenuExport + "<tr>"
            for cellule in ligne:
                contenuExport = contenuExport + "<td>" + cellule + "</td>"
            contenuExport = contenuExport + "</tr>\n"
        contenuExport = contenuExport + "</table>"
    if format.lower() == "tex":
        nbCol = len(tc[0])
        contenuExport = """\\begin{table} 
        \\begin{tabular}{"""
        structure = "|l" + (nbCol-1)*"|r" + "|} \n \\hline\n"
        contenuExport = contenuExport + structure
        for i,ligne in enumerate(tc):
            strLigne = "&".join(ligne) + "\\\\"
            contenuExport = contenuExport + strLigne + "\n"
            if i == 0: # Ligne des en-têtes, on rajoute la hline
                contenuExport = contenuExport + "\\hline \n"


        contenuExport = contenuExport + """\\hline
        \\end{tabular}
        \\end{table}"""
    try:
        fichierSortie = open(fichier, "w")
    except:
        print("-!- Problème avec la création du fichier.")
        return(False)
    fichierSortie.write(contenuExport)
    fichierSortie.close()

def extension(chemin):
    '''Vérifie que l'extension du fichier associé au chemin indiqué est bien
    csv, html ou tex.'''
    extension = chemin.split(".")[-1]
    if extension.lower() in ['html','csv','tex']:
        return(extension)
    else:
        print("-!- Le chemin du fichier doit se terminer par l'extension '.html', '.csv' ou '.tex'.")
        return None

def lexmeter(cheminCorpus, balise, attr1, attr2, fichierSortie=None, formatSortie=None): # Fonction qui appelle toutes les autres
    """Créé un tri croisé permettant de dénombrer et de mesurer la
    longueur des textes d'un corpus en fonction des valeurs de deux attributs indiqués.
    Fonction principale du programme, elle appelle les autres fonctions.
    -cheminCorpus : chemin du fichier XML ou du dossier contenant les fichiers
    XML du corpus.
    -balise : nom de la balise délimitant les textes (ou autres unités de structure)
    du corpus.
    -attr1 et attr2 : attributs de ces balises à considérer.
    -fichierSortie : chemin du fichier à créer pour exporter le tableau.
    -formatSortie : format à utiliser pour le fichier de sortie (csv, html ou tex)."""
    global compteurAttributs
    if attr1 not in compteurAttributs.keys():
        print(f"\n-!- {attr1} n'est pas un attribut présent dans les balises <{balise}>.")
        return False
    if attr2 not in compteurAttributs.keys():
        print(f"\n-!- {attr2} n'est pas un attribut présent dans les balises <{balise}>.")
        return False
    contenuCorpus = ouvreCorpus(cheminCorpus)
    if contenuCorpus == False:
        return False
    listeDesTextes = listeTextes(contenuCorpus, balise)
    if listeDesTextes == False:
        return False

    tc = creerTC(attr1, attr2, listeDesTextes)
    tc = mettreEnFormeTC(tc)

    if fichierSortie != None:
        exporteResultatLexmeter(tc,formatSortie,fichierSortie)
        return True
    else:
        return(tc)




if __name__ == "__main__":

    # Récupération des paramètres passés éventuellement en ligne de commande
    import argparse
    parser = argparse.ArgumentParser(
    description="Calcule le tri croisé des textes d'un corpus en fonction de deux attributs.")
    parser.add_argument("-f", help="Chemin du corpus (fichier xml ou dossier)")
    parser.add_argument("-t", help="Balise définissant les textes du corpus")
    parser.add_argument("-a1", help="Premier attribut à croiser")
    parser.add_argument("-a2", help="Second attribut à croiser")
    parser.add_argument("-export", help="Chemin du fichier exporté")
    parser.add_argument("-format", help="Format du fichier exporté (csv, html ou latex)")
    args = parser.parse_args()

    # Définition et chargement du corus
    if args.f is None:
        cheminCorpus=input("Chemin du corpus :\n")
    else:
        cheminCorpus = args.f
        print("Fichier selectionné : "+cheminCorpus)
    resultat=ouvreCorpus(cheminCorpus)
    if resultat == False:
        print("-!- Chemin invalide.")
    else:
        print("\n\n")

        # Identification des textes sur la base de la balise indiquée
        if args.t is None:
            encadre(u"Nom de la balise définissant les textes du corpus :")
            baliseStructure=input()
        else:
            baliseStructure = args.t
        #print resultat
        listeDesTextes=listeTextes(resultat,baliseStructure)

        # Définition des attributs à utiliser
        if listeDesTextes is not False:
            compteurAttributs = listerAttributs(listeDesTextes)
            if args.a1 is None or args.a2 is None:
                nbTextes=len(listeDesTextes)
                nbAttributs=compteurAttributs.items()
                print("\n\n")
                encadre(u"Décompte des attributs :")
                print("\n"+str(nbTextes)+" textes dans le corpus :")
                list(nbAttributs).sort(key=lambda x:-x[1])
                for nbAttribut in nbAttributs:
                    print(str(nbAttribut[1])+" avec l'attribut "+nbAttribut[0])
                print("\n")
                encadre(u"Choisissez deux attributs à croiser :")
                attr1=input("1e attribut (en lignes) : ")
                attr2=input("2e attribut (en colonnes) : ")
            else:
                attr1 = args.a1
                attr2 = args.a2

            # Création du tri croisé
            tc = lexmeter(cheminCorpus, baliseStructure, attr1, attr2,)

            # Affichage et enregistrement du tri croisé
            if tc is not False:
                afficheTC(tc)

                if args.export is not None:
                    cheminExport = args.export
                else:
                    demandeChemin = "Chemin du fichier à exporter (utiliser l'extension '.html', '.csv' ou '.tex' pour définir le format du fichier) :\n"
                    cheminExport = input(demandeChemin)
                format = extension(cheminExport)
                try:
                    exporteResultatLexmeter(tc,cheminExport,format)
                    print("\n\nTableau exporté dans le fichier "+cheminExport+"\n\n")
                except:
                    print("\n\n-!- La création du tableau a échoué. Vérifier les paramètres utilisés.\n\n")