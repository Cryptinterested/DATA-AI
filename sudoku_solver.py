#!/usr/bin/env python3
from ortools.sat.python import cp_model
import math, random


#Comme évoqué lors du précédent cours j'ai un problème de main(), pour exécuter chaque exercice lancer directement Exercicei() (voir fin du fichier) ou i est le nuémro de l'exercice

# Permet de créer un plateau de sudoku en y insérant des valeurs de façon aléatoire en fonction du niveau de difficulté
def Plateau(niveau) :
	model = cp_model.CpModel()
	plateauJeu = []
	valeursDonnees = [] # Stocke les indices des cases remplies aléatoirement

	for i in range(9) : # Initialise le plateau sudoku classique 3x3
		sousGrille = [[ None for i in range(3)] for j in range (3)]
		plateauJeu.append(sousGrille)

	if niveau == 5 :
		nbval = 17
	elif niveau == 4 :
		nbval = 26
	elif niveau == 3 :
		nbval = 33
	elif niveau == 2 :
		nbval = 40
	elif niveau == 1 :
		nbval = 50
	else :
		Sudoku(9)

	i = 0
	while i < nbval : # Insere nbval valeurs à la grille de sudoku
		grille = random.randint(0,8) # Je selectionne une grille parmis les 9 disponibles
		ligne = random.randint(0,2) # Je selectionne une ligne
		colonne = random.randint(0,2) # je selectionne une colonne
		if plateauJeu[grille][ligne][colonne] == None :
			nb = model.NewIntVar(1,9, 'Case({},{})'.format(ligne,colonne))
			plateauJeu[grille][ligne][colonne] = nb
			model.Add(plateauJeu[grille][ligne][colonne] == nb) # Contrainte de case donnée aléatoirement
			valeursDonnees.append([grille,ligne,colonne]) #
			i+= 1

	
	for sousGrille in plateauJeu :

		for element in sousGrille : # Contrainte pour assurer qu'une ligne ne contient que des elements différents
			element = [e for e in element if e != None]
			model.AddAllDifferent(element)

		for j in range(len(sousGrille[0])) : # Vérifie que les nombres sur les colonnes soient différents (dans une sousGrille)
			model.AddAllDifferent([sousGrille[i][j] for i in range(3) if sousGrille[i][j] != None])

		model.AddAllDifferent([sousGrille[i][j] for i in range(3) for j in range(3) if sousGrille[i][j] != None ]) # Les elements de la sousGrille touts différents

	for j in range(3) : # Generalisation de la contrainte des lignes sur le sudoku entier
		cst = 0
		path = 3
		while cst+path <= 9 :
			model.AddAllDifferent([plateauJeu[i][j][k] for i in range(cst,cst+path,1) for k in range(3) if plateauJeu[i][j][k] != None ])
			cst = cst + path

	for k in range(3) : # Generalisation de la contrainte des colonnes sur le sudoku entier
		for cst in range(0,3) :
			model.AddAllDifferent([plateauJeu[i][j][k] for i in range(cst,3,3) for j in range(3) if plateauJeu[i][j][k] != None])


	return plateauJeu, model, valeursDonnees


def Sudoku(taille=9) : # Permet de rechercher une combinaison possible à partir du plateau initialisé ci-dessus

	num_vals = taille
	var = int(math.sqrt(taille))

	# Demande la difficulté du jeu
	difficulte = int(input("Choisir un niveau de difficulté : \n 1) Débutant\n 2) Facile\n 3) Moyen\n 4) Difficile\n 5) Très difficile\n"))
	print('\n')
	
	# Variables initialisées précédemment

	plateauJeu, model, valeursDonnees = Plateau(difficulte)

	# Affectation des valeurs manquantes dans PlateauJeu
	for i in range(len(plateauJeu)) :
		for j in range(3) :
			for k in range(3) :
				if plateauJeu[i][j][k] == None :
					plateauJeu[i][j][k] = model.NewIntVar(1,num_vals, 'Case({},{})'.format(j,k))

	#Ajout des contraintes globales
	for sousGrille in plateauJeu :

		for element in sousGrille : #vérifie que les nombres sur lignes soient différents
			model.AddAllDifferent(element)

		for j in range(len(sousGrille[0])) : #vérifie que les nombres sur les colonnes soient différents
			model.AddAllDifferent([sousGrille[i][j] for i in range(len(sousGrille))])

		model.AddAllDifferent([sousGrille[i][j] for i in range(3) for j in range(3) if sousGrille[i][j] != None ]) # Les elements de la sousGrille touts différents

	for j in range(var) :
		cst = 0
		path = int(math.sqrt(taille))
		while cst+path <= taille :
			model.AddAllDifferent([plateauJeu[i][j][k] for i in range(cst,cst+path,1) for k in range(var)])
			cst = cst + path

	for k in range(var) :
		for cst in range(0,int(math.sqrt(taille))) :
			model.AddAllDifferent([plateauJeu[i][j][k] for i in range(cst,taille,int(math.sqrt(taille))) for j in range(var)])
		
	#Création du solver

	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	#Affichage

	if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL: 
		Affichage(plateauJeu,valeursDonnees, solver) # Affichage du plateau créé initialement avant remplissage 
		print('\n')
		print('Configuration trouvée ! \n')
		path = int(math.sqrt(taille))
		cst = 0
		# Affichage du plateau rempli avec les contraintes
		while cst+path <= taille :
			for i in range(var) :
				for p in range(cst,cst+path,1) :
					for j in range(var) :
						print(solver.Value(plateauJeu[p][i][j]),end="  ")
					print("  ",end='')
				print('\n')
			print('\n')
			cst = cst + path


	
def Affichage(plateauJeu,valeursDonnees, solver) : #Affiche PlateauJeu uniquement avec leur valeurs données initialement stockées dans valeursDonnees 
	path = 3
	var = path
	cst = 0
	while cst+path <= 9 :
		for i in range(var) :
			for p in range(cst,cst+path,1) :
				for j in range(var) :
					if plateauJeu[p][i][j] != None and appartient([p,i,j],valeursDonnees) :
						print(solver.Value(plateauJeu[p][i][j]),end="  ")
					else :
						print('-',end="  ")
				print("  ",end='')
			print('\n')
		print('\n')
		cst = cst + path


def appartient(liste, ensemble_liste) : # Verifie qu'une liste [a,b,c] appartient bien à ensemble_liste
	for elt in ensemble_liste :
		if elt[0] == liste[0] and elt[1]== liste[1] and elt[2]== liste[2] :
			return True 
	return False


print("Sudoku 3x3 \n")
Sudoku()









