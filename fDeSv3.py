import os
import sys
import time
import copy #pour faire des copy de matrices

# utilisé comme des variables globales
historique_matrices = []
index_historique = -1  # Position actuelle dans l'historique


def undo_redo(matrice, action):
    """
    Navigue dans l'historique des états

    Paramètres:
    - matrice: la grille de jeu (sera modifiée)
    - action: "u" pour undo (reculer) ou "r" pour redo (avancer)

    Retourne:
    - 0 si l'action a réussi
    - -1 si impossible (début/fin de l'historique atteint)
    """
    global historique_matrices, index_historique

    if action == "u":  # Undo
        if index_historique > 0:
            index_historique -= 1
            # Copier l'état précédent dans la matrice
            for i in range(len(matrice)):
                for j in range(len(matrice[0])):
                    matrice[i][j] = historique_matrices[index_historique][i][j]
            return 0
        else:
            return -1  # Déjà au début de l'historique

    elif action == "r":  # Redo
        if index_historique < len(historique_matrices) - 1:
            index_historique += 1
            # Copier l'état suivant dans la matrice
            for i in range(len(matrice)):
                for j in range(len(matrice[0])):
                    matrice[i][j] = historique_matrices[index_historique][i][j]
            return 0
        else:
            return -1  # Déjà à la fin de l'historique

    return -1


#ajouter une copie de la matrice dans "historique_matrices"
def sauvegarder_etat(matrice):
    """Sauvegarde l'état actuel de la matrice dans l'historique"""
    global historique_matrices, index_historique

    # Si on n'est pas à la fin de l'historique, supprimer les états futurs
    if index_historique < len(historique_matrices) - 1:
        historique_matrices = historique_matrices[:index_historique + 1]

    # Ajouter une copie profonde de la matrice
    historique_matrices.append(copy.deepcopy(matrice))
    index_historique += 1


def ajouter_pion(matrice, joueur, colonne):
    """
    Ajoute un jeton dans la colonne spécifiée

    Paramètres:
    - matrice: la grille de jeu
    - joueur: 1 ou -1
    - colonne: numéro de colonne (0 à taille_x-1)

    Retourne:
    - 0 si l'ajout a réussi
    - -1 si la colonne est pleine
    """
    # Sauvegarder l'état AVANT la modification
    sauvegarder_etat(matrice)

    # Vérifier que la colonne est valide
    if colonne < 0 or colonne >= len(matrice[0]):
        return -1

    # Parcourir la colonne de bas en haut
    for i in range(len(matrice) - 1, -1, -1):
        if matrice[i][colonne] == 0:  # Case vide trouvée
            matrice[i][colonne] = joueur
            return 0

    # Si on arrive ici, la colonne est pleine
    return -1



def afficherMatrice(matrice):
    for i in range(0, len(matrice)):
        for j in range(0, len(matrice[0])):
            if j==0:
                print(f"[{matrice[i][j]:2d}, ", end="")
            if (j>0 and j<(len(matrice[0]))-1):
                print(f"{matrice[i][j]:2d}, ", end="")
            if j==len(matrice[0])-1:
                print(f"{matrice[i][j]:2d}]", end="")
        print("")
    print("________________________________")
    print("  0   1   2   3   4   5   6   7 ", end="")





def createMatrice():
    matrice = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    taille_x = len(matrice)
    taille_y = len(matrice[0])
    n = 1
    for i in range(0, taille_x):
        for j in range(0, taille_y):
            matrice[i][j] = n
            n += 1
    return matrice




def verifier_victoire(matrice):
    taille_x = len(matrice)
    taille_y = len(matrice[0])
    nb = 4  # nb jetons à aligner

    # -----------------------------
    # Vérification lignes
    # -----------------------------
    def ligne():
        result = 0
        for i in range(taille_x):
            for j in range(taille_y - nb + 1):
                somme = 0
                for k in range(nb):
                    # print(f"{matrice[i][j+k]:3d}", end="" if k < nb-1 else "\n")
                    somme += matrice[i][j+k]
                if somme == nb:
                    if result == 0:
                        result = 1
                elif somme == -nb:
                    if result == 0:
                        result = -1
        return result

    # -----------------------------
    # Vérification colonnes
    # -----------------------------
    def colonne():
        result = 0
        for i in range(taille_x - nb + 1):
            for j in range(taille_y):
                somme = 0
                for k in range(nb):
                     # print(f"{matrice[i+k][j]:3d}", end="" if k < nb-1 else "\n")
                    somme += matrice[i+k][j]
                if somme == nb:
                    if result == 0:
                        result = 1
                elif somme == -nb:
                    if result == 0:
                        result = -1
        return result

    # -----------------------------
    # Vérification diagonale ↘
    # -----------------------------
    def diagonal():
        result = 0
        for i in range(taille_x - nb + 1):
            for j in range(taille_y - nb + 1):
                somme = 0
                for k in range(nb):
                    # print(f"{matrice[i+k][j+k]:3d}", end="" if k < nb-1 else "\n")
                    somme += matrice[i+k][j+k]
                if somme == nb:
                    if result == 0:
                        result = 1
                elif somme == -nb:
                    if result == 0:
                        result = -1
        return result

    # -----------------------------
    # Vérification anti-diagonale ↙
    # -----------------------------
    def antidiagonal():
        result = 0
        for i in range(taille_x - nb + 1):
            for j in range(nb-1, taille_y):
                somme = 0
                for k in range(nb):
                    # print(f"{matrice[i+k][j-k]:3d}", end="" if k < nb-1 else "\n")
                    somme += matrice[i+k][j-k]
                if somme == nb:
                    if result == 0:
                        result = 1
                elif somme == -nb:
                    if result == 0:
                        result = -1
        return result

    # -----------------------------
    # Exécution de toutes les vérifications
    # -----------------------------
    result = ligne()
    if result == 0:
        result = colonne()
    if result == 0:
        result = diagonal()
    if result == 0:
        result = antidiagonal()

    return result


#matrice = createMatrice()
matrice = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
]

print(f"taille = {len(matrice)}")


def boucleJeuConsole():
    # Boucle de jeu modifiée
    print(f"taille = {len(matrice)}")

    # Sauvegarder l'état initial
    sauvegarder_etat(matrice)

    result = 0
    tour = 1

    while result == 0:
        afficherMatrice(matrice)

        print(f"\nJoueur {tour}, à vous de jouer !")
        print("(Entrez 'u' pour undo, 'r' pour redo)")

        try:
            entree = input(f"Choisissez une colonne (0 à {len(matrice[0]) - 1}): ")

            # Vérifier si c'est une commande undo/redo
            if entree.lower() == "u":
                resultat_undo = undo_redo(matrice, "u")
                if resultat_undo == -1:
                    print("❌ Impossible de reculer, vous êtes au début de l'historique !")
                else:
                    print("✅ Coup annulé !")
                    # Changer de joueur (car on revient en arrière)
                    tour = -tour
                input("Appuyez sur Entrée pour continuer...")
                continue

            elif entree.lower() == "r":
                resultat_redo = undo_redo(matrice, "r")
                if resultat_redo == -1:
                    print("❌ Impossible d'avancer, vous êtes à la fin de l'historique !")
                else:
                    print("✅ Coup rétabli !")
                    # Changer de joueur
                    tour = -tour
                input("Appuyez sur Entrée pour continuer...")
                continue

            # Sinon, traiter comme un numéro de colonne
            colonne = int(entree)

            # Essayer d'ajouter l'élément
            resultat_ajout = ajouter_pion(matrice, tour, colonne)

            if resultat_ajout == -1:
                print("Colonne invalide ou pleine ! Réessayez.")
                input("Appuyez sur Entrée pour continuer...")
                continue

            # Vérifier la victoire
            result = verifier_victoire(matrice)

            # Changer de joueur si pas de victoire
            if result == 0:
                tour = -tour

        except ValueError:
            print("Entrée invalide ! Entrez un nombre, 'u' ou 'r'.")
            input("Appuyez sur Entrée pour continuer...")

    # Afficher le résultat final
    afficherMatrice(matrice)
    print(f"\n🎉 Le joueur {tour} a gagné ! 🎉")

    while True:
        sortie = input("\nAppuyez sur 'q' pour quitter: ").lower()
        if sortie == 'q':
            break

    print("Merci d'avoir joué !")


boucleJeuConsole()

