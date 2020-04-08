# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:32:10 2020

@author: JEAN Daniel && KANE Amath 
"""
from sklearn.metrics import confusion_matrix
from sklearn import datasets
from sklearn.naive_bayes import GaussianNB

iris = datasets.load_iris()

import csv
#import reader from csv
from math import sqrt
 
#Calcul la distance Euclidienne entre deux vecteurs
def Distance_eucludienne(vecteur1, vecteur2):
	distance = 0.0
	for i in range(len(vecteur1)-1):
		distance += (float(vecteur1[i])- float(vecteur2[i]))**2
	return sqrt(distance)
"""
def ChargerFichier(NomFichier):
	Base = list()
	with open(NomFichier, 'r') as Fichier:
		lanceur = reader(Fichier)
		for colonne in lanceur:
			if not colonne:
				continue
			Base.append(colonne)
	return Base
"""



def ChargerFichier1(fichier):
    base = []
    with open(fichier,newline='') as csvfile :
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for ligne in spamreader :
            base.append(', '.join(ligne).split(','))
    return base


def ConvertionColonneEnFloat(BaseDeDonnee, colonne):
	for element in BaseDeDonnee:
		element[colonne] = float(element[colonne].strip())
        
def ConvertionColonneEnInt(BaseDeDonnee, colonne):
	valeurligne = [colonne1[colonne] for colonne1 in BaseDeDonnee]
	liste = set(valeurligne)
	Sauvegarde = dict()
	for i, valeur in enumerate(liste):
		Sauvegarde[valeur] = i
		print('[%s] => %d' % (valeur, i))
	for colonne in BaseDeDonnee:
		colonne[colonne] = Sauvegarde[colonne[colonne]]
	return Sauvegarde

def BaseDeDonnee_minmax(BaseDeDonnee):  #Trouve le minimum et le maximum pour chaque colonnne
	listeminmax = list()
	for i in range(len(BaseDeDonnee[0])):
		valeurcolonne = [colonne[i] for colonne in BaseDeDonnee]
		valeurmini = min(valeurcolonne)
		valeurmini = max(valeurcolonne)
		listeminmax.append([valeurmini, valeurmini])
	return listeminmax

#Normalisation des donnnées en colonne
def Normalisation_BaseDeDonnee(BaseDeDonnee, listeminmax):
	for colonne in BaseDeDonnee:
		for i in range(len(colonne)):
			colonne[i] = (colonne[i] - listeminmax[i][0]) / (listeminmax[i][1] - listeminmax[i][0])
            

 
# Localise les voisins les plus similaires
def TrouverVoisin(BaseDeDonnee, Echantillon, NombredePoints):  #Ici NombredePoints represente k 
	distance = list()
	for element in BaseDeDonnee:
		dist = Distance_eucludienne(Echantillon, element)
		distance.append((element, dist))
	distance.sort(key=lambda tup: tup[1])
	voisin = list()
	for i in range(NombredePoints):
		voisin.append(distance[i][0])
	return voisin


def Prediction(BaseDeDonnee, Echantillon, NombredePoints):
	voisin = TrouverVoisin(BaseDeDonnee, Echantillon, NombredePoints)
	Valeur = [Colonne[-1] for Colonne in voisin]
	prediction = max(set(Valeur), key=Valeur.count)
	return prediction
 
#Creaction base de donnée

BaseDeDonne=ChargerFichier1('iris.data')
colonne = [5.7,2.9,4.2,1.3]
print("Choisir un nombre de points sur lequel faire l'etude compris entre 1 et 150" )
nombrepoints=eval(input())
echantillon = Prediction(BaseDeDonne, colonne, nombrepoints)
print('Donnee=%s, Prediction: %s' % (colonne, echantillon))
target = iris.target
data = iris.data
clf = GaussianNB()
clf.fit(data, target)
clf.get_params()
result = clf.predict(data)
conf = confusion_matrix(target, result)
print("la matrice de confusion est : ")
print(conf)









