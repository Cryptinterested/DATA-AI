#!/usr/bin/env python3
import sys


def Apriori(T, epsilon) :

	dicobis = {}

	L = [] #Contiendra l'union des Li
	nombresDifferents = [] # Servira à stocker tous les entiers différents de T

	# On parcourt T afin de stocker tous les entiers différents dans nombresDifferents
	for t in T : 
		for nombre in t :
			if nombre not in nombresDifferents :
				nombresDifferents.append(nombre)

	# Initialisation de L1, liste des singletons apparaissant au moins epsilon fois dans T
	L1 = []
	dico = {}
	compteur = 0
	for n in nombresDifferents :
		compteur = 0
		for t in T :
			if n in t :
				compteur= compteur+1
				dico[n] = compteur
	for element in dico : 
		if dico[element] >= epsilon : 
			L1.append([element])

	# On ajoute L1 à l'ensemble
	L.append(L1)
	
	# On génère tous les Li à partir de L1 et on les ajoute à L
	Li = L1
	aux = []
	
	while Li != [] :
		for i in range(len(nombresDifferents)) :
			for tab in Li :
				if confiance(T,tab,[nombresDifferents[i]]) >= 0.75 : # On teste la confiance avant d'aller plus loin 
					if apparaitEpsilonFois(tab+[nombresDifferents[i]],T,epsilon) and not contientdeja(aux,tab+[nombresDifferents[i]]) : # Verifie si le uplet créé apparait epsilon fois dans T
						
						a = tuple(tab)
						dicobis[a," => ",nombresDifferents[i]]= confiance(T,tab,[nombresDifferents[i]])
						
						aux.append(tab+[nombresDifferents[i]])
		L.append(aux)
		Li = aux
		aux = []
		i = 0

	return L,dicobis


def support(T,t) : 
	compteur = 0
	for tab in T :
		if contient(tab,t) and contientPlusieursFois(t) == False :
			compteur = compteur + 1
	return compteur/ len(T)

def confiance(T,X,Y) : 
	if support(T,X) != 0 : 
		return support(T,X+Y)/support(T,X)
	else :
		return 0


def contientdeja(T,t): #Permet de tester si un tableau T contient plusieurs fois le sous tableau t
	compteur1 = 0
	compteur2 = 0
	for tab in T :
		if len(tab) == len(t) :
			for elt in t:
				if elt in tab :
					compteur2 = compteur2 + 1
			if compteur2 == len(t) :
				compteur1 = compteur1 + 1
			compteur2 = 0
	return compteur1 > 0


def contientPlusieursFois(tab) : # Permet de tester si un tableau d'entiers contient plusieurs fois les même entiers, cette méthode complète contient(T1,T2)
	for nb in tab :
		if tab.count(nb) > 1 :
			return True
	return False

def apparaitEpsilonFois(nuplet, T, epsilon) : #Permet de tester si un uplet apparait epsilon fois dans les sous tableaux de T
	compteur = 0
	if contientPlusieursFois(nuplet) : 
		return False
	else :
		for tab in T :
			if contient(tab,nuplet) :
				compteur = compteur + 1
	return compteur >= epsilon

def contient(T1,T2) : # Permet de tester si T1 contient les elements de T2 , ex [1,3,2] et [1,2]
	b = True
	for nb in T2 :
		if nb not in T1 :
			b = False
	return b


def main() :
	T=[[1,2,5],[1,3,5],[1,2],[1,2,3,4,5],[1,2,4,5],[2,3,5],[1,5]]
	#print(contientdeja([[1,2,3],[1,3],[2,3,1]],[3,1,2]))
	#print(apparaitEpsilonFois([1,1],[[1,3,2],[1,2,4],[1,0,2]], 3))
	#print(support(T,[1,2,5]))
	#print(confiance(T,[1,2],[5]))
	res,dicobis = Apriori(T,3)

	print("Niveau de confiance d'avoir le tuple de gauche et celui de droite : ")
	for cle,valeur in dicobis.items() :
		print(cle, ":", valeur)


	print("Résultat :\n")
	for i in range(len(res)) :
		if res[i] != [] :
			print("L",i, ":" ,res[i])

if __name__ == '__main__':
	main()
	