import copy


def createMatrice(rows, cols):
    """Crée une matrice vide de taille rows x cols"""
    return [[0 for _ in range(cols)] for _ in range(rows)]


def afficherMatrice(matrice):
    """Affiche la matrice dans la console"""
    print("\n  ", end="")
    for col in range(len(matrice[0])):
        print(f" {col} ", end="")
    print("\n  " + "---" * len(matrice[0]))

    for row in matrice:
        print("  ", end="")
        for cell in row:
            if cell == 1:
                symbole = "🔴"
            elif cell == -1:
                symbole = "🟡"
            else:
                symbole = "⚪"
            print(f"{symbole} ", end="")
        print()
    print()


def ajouter_pion(matrice, joueur, col):
    """
    Ajoute un pion du joueur dans la colonne spécifiée
    Retourne 0 si succès, -1 si colonne invalide ou pleine
    """
    rows = len(matrice)

    # Vérifier si la colonne est valide
    if col < 0 or col >= len(matrice[0]):
        return -1

    # Trouver la première ligne vide en partant du bas
    for row in range(rows - 1, -1, -1):
        if matrice[row][col] == 0:
            matrice[row][col] = joueur
            return 0

    # Colonne pleine
    return -1


def verifier_victoire(matrice, nb_aligned=4):
    """
    Vérifie s'il y a un gagnant
    Retourne 1 si joueur 1 gagne, -1 si joueur -1 gagne, 0 sinon
    """
    rows = len(matrice)
    cols = len(matrice[0])

    # Vérifier horizontalement
    for row in range(rows):
        for col in range(cols - nb_aligned + 1):
            if matrice[row][col] != 0:
                if all(matrice[row][col + i] == matrice[row][col] for i in range(nb_aligned)):
                    return matrice[row][col]

    # Vérifier verticalement
    for row in range(rows - nb_aligned + 1):
        for col in range(cols):
            if matrice[row][col] != 0:
                if all(matrice[row + i][col] == matrice[row][col] for i in range(nb_aligned)):
                    return matrice[row][col]

    # Vérifier diagonale descendante (\)
    for row in range(rows - nb_aligned + 1):
        for col in range(cols - nb_aligned + 1):
            if matrice[row][col] != 0:
                if all(matrice[row + i][col + i] == matrice[row][col] for i in range(nb_aligned)):
                    return matrice[row][col]

    # Vérifier diagonale montante (/)
    for row in range(nb_aligned - 1, rows):
        for col in range(cols - nb_aligned + 1):
            if matrice[row][col] != 0:
                if all(matrice[row - i][col + i] == matrice[row][col] for i in range(nb_aligned)):
                    return matrice[row][col]

    return 0


def coups_possibles(matrice):
    """
    Retourne la liste des colonnes où on peut jouer
    """
    cols = len(matrice[0])
    coups = []

    for col in range(cols):
        # Si la première ligne de la colonne est vide, on peut jouer
        if matrice[0][col] == 0:
            coups.append(col)

    return coups


def grille_pleine(matrice):
    """Vérifie si la grille est complètement remplie"""
    for col in range(len(matrice[0])):
        if matrice[0][col] == 0:
            return False
    return True


def evaluer_position(matrice, nb_aligned=4):
    """
    Fonction d'évaluation pour Minimax
    Retourne : 1 si victoire du joueur 1
              -1 si victoire du joueur -1
               0 sinon
    """
    resultat = verifier_victoire(matrice, nb_aligned)
    return resultat


def minimax(matrice, profondeur, est_maximisant, nb_aligned=4):
    """
    Algorithme Minimax

    Args:
        matrice: état actuel du jeu
        profondeur: profondeur restante à explorer
        est_maximisant: True si c'est le tour du joueur maximisant (1), False sinon (-1)
        nb_aligned: nombre de pions alignés pour gagner

    Returns:
        La valeur de la position
    """
    # Condition d'arrêt : profondeur 0 ou partie terminée
    victoire = verifier_victoire(matrice, nb_aligned)
    if profondeur == 0 or victoire != 0 or grille_pleine(matrice):
        return evaluer_position(matrice, nb_aligned)

    coups = coups_possibles(matrice)

    if est_maximisant:
        # Joueur 1 (maximisant)
        val = float('-inf')
        for coup in coups:
            # Créer une copie de la matrice pour simuler le coup
            nouvelle_matrice = copy.deepcopy(matrice)
            ajouter_pion(nouvelle_matrice, 1, coup)

            # Appel récursif
            evaluation = minimax(nouvelle_matrice, profondeur - 1, False, nb_aligned)
            val = max(val, evaluation)

        return val
    else:
        # Joueur -1 (minimisant)
        val = float('inf')
        for coup in coups:
            # Créer une copie de la matrice pour simuler le coup
            nouvelle_matrice = copy.deepcopy(matrice)
            ajouter_pion(nouvelle_matrice, -1, coup)

            # Appel récursif
            evaluation = minimax(nouvelle_matrice, profondeur - 1, True, nb_aligned)
            val = min(val, evaluation)

        return val


def meilleur_coup_ia(matrice, joueur_ia, profondeur=5, nb_aligned=4):
    """
    Trouve le meilleur coup pour l'IA en utilisant Minimax

    Args:
        matrice: état actuel du jeu
        joueur_ia: 1 ou -1 selon qui est l'IA
        profondeur: profondeur de recherche
        nb_aligned: nombre de pions alignés pour gagner

    Returns:
        La colonne du meilleur coup
    """
    coups = coups_possibles(matrice)

    if not coups:
        return None

    meilleur_coup = coups[0]

    if joueur_ia == 1:
        # IA maximise
        meilleure_valeur = float('-inf')
        for coup in coups:
            nouvelle_matrice = copy.deepcopy(matrice)
            ajouter_pion(nouvelle_matrice, joueur_ia, coup)

            valeur = minimax(nouvelle_matrice, profondeur - 1, False, nb_aligned)

            if valeur > meilleure_valeur:
                meilleure_valeur = valeur
                meilleur_coup = coup
    else:
        # IA minimise
        meilleure_valeur = float('inf')
        for coup in coups:
            nouvelle_matrice = copy.deepcopy(matrice)
            ajouter_pion(nouvelle_matrice, joueur_ia, coup)

            valeur = minimax(nouvelle_matrice, profondeur - 1, True, nb_aligned)

            if valeur < meilleure_valeur:
                meilleure_valeur = valeur
                meilleur_coup = coup

    return meilleur_coup


def jouer_contre_ia():
    """
    Mode de jeu : Humain vs IA dans la console
    """
    print("=" * 50)
    print("🎮 PUISSANCE 4 - Joueur vs IA 🎮")
    print("=" * 50)

    # Configuration de la partie
    rows = 6
    cols = 7
    nb_aligned = 4

    print("\nChoisissez la difficulté de l'IA :")
    print("1 - Facile (profondeur 3)")
    print("2 - Moyen (profondeur 5)")
    print("3 - Difficile (profondeur 7)")

    while True:
        try:
            choix = int(input("\nVotre choix (1-3) : "))
            if choix == 1:
                profondeur = 3
                break
            elif choix == 2:
                profondeur = 5
                break
            elif choix == 3:
                profondeur = 7
                break
            else:
                print("Choix invalide !")
        except ValueError:
            print("Entrez un nombre entre 1 et 3 !")

    print("\nChoisissez votre couleur :")
    print("1 - Rouge (🔴) - Vous commencez")
    print("2 - Jaune (🟡) - L'IA commence")

    while True:
        try:
            choix = int(input("\nVotre choix (1-2) : "))
            if choix == 1:
                joueur_humain = 1
                joueur_ia = -1
                break
            elif choix == 2:
                joueur_humain = -1
                joueur_ia = 1
                break
            else:
                print("Choix invalide !")
        except ValueError:
            print("Entrez 1 ou 2 !")

    # Initialisation de la partie
    matrice = createMatrice(rows, cols)
    joueur_actuel = 1  # Rouge commence toujours

    print("\n" + "=" * 50)
    print("🎯 Début de la partie !")
    print("=" * 50)

    # Boucle de jeu
    while True:
        afficherMatrice(matrice)

        # Vérifier victoire
        resultat = verifier_victoire(matrice, nb_aligned)
        if resultat != 0:
            if resultat == joueur_humain:
                print("🎉 VICTOIRE ! Vous avez gagné ! 🎉")
            else:
                print("💀 DÉFAITE ! L'IA a gagné ! 💀")
            break

        # Vérifier match nul
        if grille_pleine(matrice):
            print("🤝 Match nul ! 🤝")
            break

        # Tour du joueur
        if joueur_actuel == joueur_humain:
            print(f"🎮 Votre tour ({'🔴 Rouge' if joueur_humain == 1 else '🟡 Jaune'})")

            while True:
                try:
                    col = int(input(f"Choisissez une colonne (0-{cols - 1}) : "))

                    if col < 0 or col >= cols:
                        print(f"Colonne invalide ! Choisissez entre 0 et {cols - 1}")
                        continue

                    if matrice[0][col] != 0:
                        print("Cette colonne est pleine !")
                        continue

                    ajouter_pion(matrice, joueur_actuel, col)
                    break

                except ValueError:
                    print("Entrez un nombre valide !")

        else:
            # Tour de l'IA
            print(f"🤖 Tour de l'IA ({'🔴 Rouge' if joueur_ia == 1 else '🟡 Jaune'})")
            print("L'IA réfléchit...", end="", flush=True)

            coup_ia = meilleur_coup_ia(matrice, joueur_ia, profondeur, nb_aligned)
            ajouter_pion(matrice, joueur_actuel, coup_ia)

            print(f"\n✓ L'IA joue en colonne {coup_ia}")

        # Changer de joueur
        joueur_actuel *= -1
        print()

    print("\n" + "=" * 50)
    print("Merci d'avoir joué !")
    print("=" * 50)


# Section main
if __name__ == "__main__":
    jouer_contre_ia()