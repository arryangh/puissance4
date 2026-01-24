import copy

# Historique pour undo/redo
historique_matrices = []
index_historique = -1


def reset_historique(matrice):
    """Appelé au début d'une nouvelle partie"""
    global historique_matrices, index_historique
    historique_matrices = []
    index_historique = -1
    sauvegarder_etat(matrice)


def sauvegarder_etat(matrice):
    """Sauvegarde l'état actuel de la matrice dans l'historique"""
    global historique_matrices, index_historique

    # Si on a fait undo puis un nouveau coup → on coupe le futur
    if index_historique < len(historique_matrices) - 1:
        historique_matrices = historique_matrices[:index_historique + 1]

    historique_matrices.append(copy.deepcopy(matrice))
    index_historique += 1


def undo_redo(matrice, action, mode_ia):
    """Undo/Redo avec le mode pour faire 1 undo/redo pour 1v1 et 2 undo/redo pour IA"""
    global historique_matrices, index_historique

    # En mode IA on saute 2 coups, sinon 1
    pas = 2 if mode_ia is not None else 1

    if action == "u":  # UNDO
        if index_historique - pas >= 0:
            index_historique -= pas
        else:
            return -1

    elif action == "r":  # REDO
        if index_historique + pas < len(historique_matrices):
            index_historique += pas
        else:
            return -1

    else:
        return -1

    # Recharger la matrice depuis l'historique
    etat = historique_matrices[index_historique]
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            matrice[i][j] = etat[i][j]

    return 0


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

    if col < 0 or col >= len(matrice[0]):
        return -1

    for row in range(rows - 1, -1, -1):
        if matrice[row][col] == 0:
            matrice[row][col] = joueur
            return 0

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
    """Retourne la liste des colonnes où on peut jouer"""
    cols = len(matrice[0])
    coups = []

    for col in range(cols):
        if matrice[0][col] == 0:
            coups.append(col)

    return coups


def grille_pleine(matrice):
    """Vérifie si la grille est complètement remplie"""
    for col in range(len(matrice[0])):
        if matrice[0][col] == 0:
            return False
    return True


def compter_sequences(matrice, joueur, longueur, nb_aligned=4):
    """
    Compte le nombre de séquences d'une certaine longueur pour un joueur
    Une séquence peut encore être complétée (pas bloquée)
    """
    rows = len(matrice)
    cols = len(matrice[0])
    count = 0

    # Vérifier horizontalement
    for row in range(rows):
        for col in range(cols - nb_aligned + 1):
            sequence = [matrice[row][col + i] for i in range(nb_aligned)]
            if sequence.count(joueur) == longueur and sequence.count(0) == nb_aligned - longueur and sequence.count(
                    -joueur) == 0:
                count += 1

    # Vérifier verticalement
    for row in range(rows - nb_aligned + 1):
        for col in range(cols):
            sequence = [matrice[row + i][col] for i in range(nb_aligned)]
            if sequence.count(joueur) == longueur and sequence.count(0) == nb_aligned - longueur and sequence.count(
                    -joueur) == 0:
                count += 1

    # Vérifier diagonale descendante (\)
    for row in range(rows - nb_aligned + 1):
        for col in range(cols - nb_aligned + 1):
            sequence = [matrice[row + i][col + i] for i in range(nb_aligned)]
            if sequence.count(joueur) == longueur and sequence.count(0) == nb_aligned - longueur and sequence.count(
                    -joueur) == 0:
                count += 1

    # Vérifier diagonale montante (/)
    for row in range(nb_aligned - 1, rows):
        for col in range(cols - nb_aligned + 1):
            sequence = [matrice[row - i][col + i] for i in range(nb_aligned)]
            if sequence.count(joueur) == longueur and sequence.count(0) == nb_aligned - longueur and sequence.count(
                    -joueur) == 0:
                count += 1

    return count


def evaluer_position(matrice, joueur_ia, nb_aligned=4):
    """
    Fonction d'évaluation intelligente pour Minimax
    Plus le score est élevé, meilleure est la position pour joueur_ia
    """
    # Vérifier victoire immédiate
    victoire = verifier_victoire(matrice, nb_aligned)
    if victoire == joueur_ia:
        return 10000  # Victoire de l'IA = excellent
    elif victoire == -joueur_ia:
        return -10000  # Victoire de l'adversaire = catastrophique

    score = 0

    # Compter les séquences pour l'IA
    ia_trois = compter_sequences(matrice, joueur_ia, 3, nb_aligned)
    ia_deux = compter_sequences(matrice, joueur_ia, 2, nb_aligned)

    # Compter les séquences pour l'adversaire
    adv_trois = compter_sequences(matrice, -joueur_ia, 3, nb_aligned)
    adv_deux = compter_sequences(matrice, -joueur_ia, 2, nb_aligned)

    # Pondération : bloquer 3 alignés adverses est CRITIQUE
    score += ia_trois * 100  # 3 pions alignés IA = très bon
    score += ia_deux * 10  # 2 pions alignés IA = bon
    score -= adv_trois * 150  # 3 pions alignés adversaire = URGENT à bloquer
    score -= adv_deux * 15  # 2 pions alignés adversaire = à surveiller

    # Bonus pour jouer au centre (colonnes centrales sont stratégiques)
    cols = len(matrice[0])
    centre = cols // 2
    for row in range(len(matrice)):
        if matrice[row][centre] == joueur_ia:
            score += 3

    return score


def minimax(matrice, profondeur, est_maximisant, joueur_ia, nb_aligned=4):
    """
    Algorithme Minimax avec évaluation intelligente

    Args:
        matrice: état actuel du jeu
        profondeur: profondeur restante à explorer
        est_maximisant: True si c'est le tour de l'IA, False sinon
        joueur_ia: 1 ou -1 selon qui est l'IA
        nb_aligned: nombre de pions alignés pour gagner

    Returns:
        La valeur de la position
    """
    # Condition d'arrêt
    victoire = verifier_victoire(matrice, nb_aligned)
    if profondeur == 0 or victoire != 0 or grille_pleine(matrice):
        return evaluer_position(matrice, joueur_ia, nb_aligned)

    coups = coups_possibles(matrice)

    if est_maximisant:
        # Tour de l'IA (maximise)
        val = float('-inf')
        for coup in coups:
            nouvelle_matrice = copy.deepcopy(matrice)
            ajouter_pion(nouvelle_matrice, joueur_ia, coup)
            evaluation = minimax(nouvelle_matrice, profondeur - 1, False, joueur_ia, nb_aligned)
            val = max(val, evaluation)
        return val
    else:
        # Tour de l'adversaire (minimise)
        val = float('inf')
        for coup in coups:
            nouvelle_matrice = copy.deepcopy(matrice)
            ajouter_pion(nouvelle_matrice, -joueur_ia, coup)
            evaluation = minimax(nouvelle_matrice, profondeur - 1, True, joueur_ia, nb_aligned)
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

    # PRIORITÉ 1 : Vérifier si l'IA peut gagner immédiatement
    for coup in coups:
        temp_matrice = copy.deepcopy(matrice)
        ajouter_pion(temp_matrice, joueur_ia, coup)
        if verifier_victoire(temp_matrice, nb_aligned) == joueur_ia:
            return coup  # Gagner immédiatement !

    # PRIORITÉ 2 : Vérifier si l'adversaire peut gagner (BLOQUER directement)
    for coup in coups:
        temp_matrice = copy.deepcopy(matrice)
        ajouter_pion(temp_matrice, -joueur_ia, coup)
        if verifier_victoire(temp_matrice, nb_aligned) == -joueur_ia:
            return coup  # Bloquer la victoire adverse !

    # PRIORITÉ 3 : Utiliser Minimax pour trouver le meilleur coup stratégique
    meilleur_coup = coups[0]
    meilleure_valeur = float('-inf')

    for coup in coups:
        nouvelle_matrice = copy.deepcopy(matrice)
        ajouter_pion(nouvelle_matrice, joueur_ia, coup)

        valeur = minimax(nouvelle_matrice, profondeur - 1, False, joueur_ia, nb_aligned)

        if valeur > meilleure_valeur:
            meilleure_valeur = valeur
            meilleur_coup = coup

    return meilleur_coup