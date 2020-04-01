#!/usr/bin/env python3

def creationPlateau() :
    etat_initial = [['.','.','.'],
                    ['.','.','.'],
                    ['.','.','.']]
    return etat_initial

def Affichage(plateau): # Methode d'affichage du plateau
    for i in range(0, 3):
        for j in range(0, 3):
            print(' {} '.format(plateau[i][j]), end=" ")
        print("\n")
    print()


def coupValide(ligne,colonne,plateau) : # Teste si un coup donné est valide dans le plateau
    if ligne < 0 or ligne > 2 or colonne < 0 or colonne > 2: # Teste si le coup est dans les bornes
        return False
    elif plateau[ligne][colonne] != '.': # Teste si la case à remplir est bien vide
        return False
    else:
        return True

def Resultat(ligne,colonne,valeur, plateau) : # Si le coup est valide, rempli la case avec valeur
    if coupValide(ligne,colonne,plateau) :
        plateau[ligne][colonne] = valeur

def Actions(plateau) : # Renvoie la liste des actions possibles
    actions = [] 
    for i in range(0, 3):
        for j in range(0, 3):
            if plateau[i][j] == '.' :
                actions.append([i,j])
    return actions


def test_terminal(plateau) : # Teste si le jeu, est fini et renvoie le signe du vainqueur ou bien '.' si il y a égalité
    # Teste de victoire verticale
    for i in range(0, 3):
        if (plateau[0][i] != '.' and plateau[0][i] == plateau[1][i] and plateau[1][i] == plateau[2][i]):
            return plateau[0][i]

    # Teste de victoire Horizontale
    for i in range(0, 3):
        if (plateau[i] == ['X', 'X', 'X']):
            return 'X'
        elif (plateau[i] == ['O', 'O', 'O']):
            return 'O'

    # Teste de victoire 1ere diagonale
    if (plateau[0][0] != '.' and plateau[0][0] == plateau[1][1] and plateau[0][0] == plateau[2][2]):
        return plateau[0][0]

    # Teste de victoire deuxième diagonale
    if (plateau[0][2] != '.' and plateau[0][2] == plateau[1][1] and plateau[0][2] == plateau[2][0]):
        return plateau[0][2]

    # Si perosnne n'a Personne n'a gagné
    for i in range(0, 3):
        for j in range(0, 3):
            if (plateau[i][j] == '.'):
                return None
    # Si égalité entre les deux joueurs
    return '.'

def Utility(resultat,plateau) : # Renvoie le score, si on gagne, renvoie 1, si on a perdu renvoie -1 et renvoie 0 sinon 
    if resultat == 'X': # Si on a perdu
        return (-1, 0, 0)
    elif resultat == 'O': # Si on a gagné
        return (1, 0, 0)
    elif resultat == '.': # Si égalité 
        return (0, 0, 0)


def max_value(plateau):
    maxvalue = -2
    ligne = None
    colonne = None
    # Teste si le jeu est fini 
    if test_terminal(plateau) != None :
        return Utility(test_terminal(plateau),plateau)
    # Sinon test_terminal vaut false et on calcule
    else :
        for a in Actions(plateau) :
            if plateau[a[0]][a[1]] == '.': # Si case vide
                plateau[a[0]][a[1]] = 'O'
                m, min_ligne, min_colonne = min_value(plateau)
                if m > maxvalue: #Alpha-Beta teste
                    maxvalue = m
                    ligne = a[0]
                    colonne = a[1]
                # On remet la case à vide
                plateau[a[0]][a[1]] = '.'
    return maxvalue, ligne, colonne


def min_value(plateau):
    minvalue = 2
    ligne = None
    colonne = None
    # Teste si le jeu est fini 
    if test_terminal(plateau) != None :
        return Utility(test_terminal(plateau),plateau)
    # Sinon test_terminal vaut false et on calcule    
    else :
        for a in Actions(plateau) :
            if plateau[a[0]][a[1]] == '.':
                plateau[a[0]][a[1]] = 'X'
                m, max_ligne, max_colonne = max_value(plateau)
                if m < minvalue: # Alpha-Beta teste
                    minvalue = m
                    ligne = a[0]
                    colonne = a[1]
                plateau[a[0]][a[1]] = '.'
    return minvalue, ligne, colonne


def Minimax_decision(plateau, Joueur):
    print("\nInitialisation ... ",end="\n\n")
    while True:
        Affichage(plateau)
        # On teste si le jeu est fini ou non 
        if test_terminal(plateau) != None :
            resultat = test_terminal(plateau)
            if resultat != None:
                if resultat == 'X':
                    print('Vous avez gagné !')
                elif resultat == 'O':
                    print("L'ordinateur a gagné ...")
                elif resultat == '.':
                    print("Égalité !")
                return 
        else : 
            #C'est notre tour
            if Joueur == 'X':
                while True:

                    m, ligneO, colonneO = min_value(plateau)
                    print('Déplacement recommandé : X = {}, Y = {}'.format(ligneO, colonneO))

                    ligneX = int(input('Choisir une ligne : '))
                    colonneX = int(input('Choisir une colonne : '))
                    print()
                    ligneO, colonneO = ligneX, colonneX

                    if coupValide(ligneX, colonneX,plateau):
                        Resultat(ligneX,colonneX,'X',plateau)
                        Joueur = 'O'
                        break
                    else:
                        print('Mouvement invalide, réessayer !')

            #Au tour de l'ordinateur de jouer
            else:
                m ,ligneX, colonneX = max_value(plateau)
                Resultat(ligneX,colonneX,'O',plateau)
                Joueur = 'X'



def main():
    plateau = creationPlateau()
    Minimax_decision(plateau,'X') # Ici, Mettre O si on souhaite que l'ordinateur commence, sinon laisser X

if __name__ == "__main__":
    main()