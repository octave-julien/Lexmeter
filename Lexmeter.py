# -*- coding: utf-8 -*-
import os
from string import punctuation
from re import split
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

def encadre(chaine):
    l=len(chaine)
    resultat="+"+(l+2)*"-"+"+\n"
    resultat=resultat+"| "+chaine+" |\n"
    resultat=resultat+"+"+(l+2)*"-"+"+"
    print(resultat)

def ouvreCorpus(cheminCorpus):
    corpusEntier=''
    if os.path.isdir(cheminCorpus)==True:
        listeFichiersCorpus=os.listdir(cheminCorpus)
        for fichierCorpus in listeFichiersCorpus:
            #print fichierCorpus
            extension=os.path.splitext(fichierCorpus)[1]
            #print extension
            if extension=='.xml':
                #print "extension OK"
                contenuFichierCorpus=open(cheminCorpus+"/"+fichierCorpus,'r').read()
                corpusEntier=corpusEntier+"\n"+contenuFichierCorpus
        if corpusEntier=='':
            print("Aucun fichier XML ou fichiers XML vides dans "+cheminCorpus)
            return(False)
        return(corpusEntier)
    elif os.path.isfile(cheminCorpus)==True:
        contenuFichierCorpus=open(cheminCorpus,'r').read()
        return(contenuFichierCorpus)
    else:
        return False
        #return listeFichiersCorpus
        
def listeTextes(corpus, baliseStructure):
    corpus=bs(corpus)
    listeDesTextes=corpus.findAll(baliseStructure)
    return(listeDesTextes)

#compteurAttributs={}

def listeAttributs(listeDesTextes): 
    compteurAttributs={}  
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

def listeValeurs(nomAttribut):
    resultat=[]
    for texte in listeDesTextes:
        if texte.has_attr(nomAttribut):
            valeur=texte.get(nomAttribut)
            if valeur not in resultat:
                resultat.append(valeur)
    return(resultat)
            
def creerTC(valsAttr1,valsAttr2):
    tc={}
    #for
    for valAttr1 in valsAttr1:
        ligne={}
        for valAttr2 in valsAttr2:
            ligne[valAttr2]=[0,0]
        tc[valAttr1]=ligne
    return(tc)

def longueurTexte(texte):
    texte=texte.text
    for signe in punctuation:
        texte=texte.replace(signe, " ")
    nbMots=len(split(r' +',texte))
    return(nbMots)

def mettreEnFormeTC(tc):
    resultat=[]
    valsAttr1.sort()
    valsAttr2.sort()
    
    enTetesLignes=tuple(valsAttr1) # Il faut une version immutable pour que l'utilisation des dictionnaires plus bas marche bien.
    enTetesCol=list(valsAttr2)
    enTetesCol.insert(0,"")
    resultat.append(enTetesCol)
    enTetesCol=enTetesCol[1:]
    enTetesCol=tuple(enTetesCol)
    #resultat.insert(0,"")
    print(enTetesCol)
    for valLigne in enTetesLignes:
        ligne=[]
        ligne.append(valLigne)
        for valCol in enTetesCol:
            ligne.append(tc[valLigne][valCol])
        resultat.append(ligne)
    return(resultat)
    
def afficheTC(tc):
    tc2=list(tc)
    table=PrettyTable(tc2[0])
    for i in range(1,len(tc2)):
        for j in range(1,len(tc2[i])):
            tc2[i][j]=str(tc2[i][j][1])+" ("+str(tc2[i][j][0])+")"
        #tc2[i].insert(0,tc2[i][0])
        table.add_row(tc2[i])
    print(table)
        

cheminCorpus=input("Chemin du corpus :\n")

resultat=ouvreCorpus(cheminCorpus)
print("\n\n")
encadre(u"Nom de la balise définissant les textes du corpus :")
baliseStructure=input()
#print resultat
listeDesTextes=listeTextes(resultat,baliseStructure)
compteurAttributs=listeAttributs(listeDesTextes)
nbTextes=len(listeDesTextes)
nbAttributs=compteurAttributs.items()
print("\n\n")
encadre(u"Décompte des attributs :")
print("\n"+str(nbTextes)+" textes dans le corpus :")
list(nbAttributs).sort(key=lambda x:-x[1])
for nbAttribut in nbAttributs:
    print(str(nbAttribut[1])+" avec l'attribut "+nbAttribut[0])

print("\n\n")
encadre(u"Choisissez deux attributs à croiser :")
attr1=input("1e attribut (en lignes) : ")
attr2=input("2e attribut (en colonnes) : ")

valsAttr1=listeValeurs(attr1)
valsAttr2=listeValeurs(attr2)

#typeAnalyse=input("Faire l'analyse à partir de la longueur des textes (l) ou du nombre de textes (n) ? : ")


# Format de retour
#{ 
#  valAttr1-1:{valAttr2-1:(nbTextes, longueur), valAttr2-2:(nbTextes, longueur), valAttr2-3:(nbTextes, longueur)},
#  valAttr1-2:{valAttr2-1:(nbTextes, longueur), valAttr2-2:(nbTextes, longueur), valAttr2-3:(nbTextes, longueur)},
#  valAttr1-3:{valAttr2-1:(nbTextes, longueur), valAttr2-2:(nbTextes, longueur), valAttr2-3:(nbTextes, longueur)}
#}

tc=creerTC(valsAttr1,valsAttr2)
nbValsAttr1=len(valsAttr1)
nbValsAttr2=len(valsAttr2)

for texte in listeDesTextes:
    attr1_ceTexte=texte.get(attr1)
    attr2_ceTexte=texte.get(attr2)
    if attr1_ceTexte!=None and attr2_ceTexte!=None:
        longueur=longueurTexte(texte)
        #print attr1_ceTexte," ",attr2_ceTexte
        tc[attr1_ceTexte][attr2_ceTexte][0]+=1
        tc[attr1_ceTexte][attr2_ceTexte][1]+=longueur
        
tc=mettreEnFormeTC(tc)
afficheTC(tc)

sortie=""
##for i in range(0,nbValsAttr1+1):
##    for j in range(0,nbValsAttr2+1):
##        if i==0 or j==0:
##            sortie=sortie+tc[i][j]+";"
##        else:
##            sortie=sortie+tc[i][j][0]+" ("+tc[i][j][1]+");"
##print(sortie)


invite="""
Que faire avec le tableau obtenu ?
Exporter en CSV : entrez "c"
Exporter en HTML : entrez "h"
"""

choixExport = input(invite)
chaineCSV = ""
if choixExport == "c":
	for ligne in tc:
		for cellule in ligne:
			chaineCSV = chaineCSV + ";" + cellule
		chaineCSV = chaineCSV + "\n"
	cheminFichierExport = input("Chemin et nom du fichier à exporter (au format /export.csv) :\n")
	fichierExport = open(cheminFichierExport, 'w')
	fichierExport.write(chaineCSV)
	fichierExport.close()
		
