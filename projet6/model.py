import copy

# Historique pour annuler/refaire
historique_matrices = []
indice_historique = -1


def reinitialiser_historique(matrice):
    """
    Réinitialise l'historique des coups et sauvegarde l'état initial.
    Mettre la matrice de départ (vide) au début de l'historique vièrge

    Appelé au début d'une nouvelle partie pour effacer l'historique précédent
    et commencer avec un historique vierge contenant uniquement l'état initial.

    Args:
        matrice (list): La matrice de jeu initiale à sauvegarder
    """
    global historique_matrices, indice_historique
    historique_matrices = []  # une liste de matrice (dimension 3)
    indice_historique = -1
    sauvegarder_etat(matrice) # mettre la première matrice à ce moment là


def sauvegarder_etat(matrice):
    """
    Sauvegarde l'état actuel de la matrice dans l'histrique.

    Si des annulation ont été effectués (l'indice est en arrière dans l'historique),
    cette fonction coupe tout l'historique future avant d'ajouter le nouvel état.

    Args:
        matrice (list): La matrice de jeu à sauvegarder
    """
    global historique_matrices, indice_historique

    # Si on a fait annuler puis un nouveau coup → on coupe le futur
    if indice_historique < len(historique_matrices) - 1:
        historique_matrices = historique_matrices[:indice_historique + 1]

    historique_matrices.append(copy.deepcopy(matrice))  # deep copy pour réecrir à un nouveau endroit du mémoire (et par réferncer pour éviter les bugs)
    indice_historique += 1


def undo_redo(matrice, action, mode_ia):
    """
    Gère les opérations de undo/redo (demandé dans l'énnoncé)

    En mode 1v1, undo/redo 1 seul coup. (pour que chaque personne puisse rejouer)
    En mode IA, undo/redo 2 coup (le coup du joueur + le coup de l'IA). (pour que l'IA puisse par rapport au nouveau coup)


    Args:
        matrice (list): La matrice de jeu à modifier
        action (str): "u" pour annuler (undo), "r" pour refaire (redo)
        mode_ia: None si mode 1v1, sinon indique le mode IA

    Returns:
        int: 0 si succès, -1 si impossible (début/fin d'historique atteint)
    """
    global historique_matrices, indice_historique

    # En mode IA on saute 2 coups, sinon 1
    if mode_ia is not None:  # si c'est le mode IA
        pas = 2
    else:  # si c'est pas le mode IA
        pas = 1

    if action == "u":  # ANNULER
        if indice_historique - pas >= 0:
            indice_historique -= pas
        else:
            return -1

    elif action == "r":  # REFAIRE
        if indice_historique + pas < len(historique_matrices):
            indice_historique += pas
        else:
            return -1

    else:
        return -1

    # Recharger la matrice depuis l'historique
    etat = historique_matrices[indice_historique]
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            matrice[i][j] = etat[i][j]

    return 0


def creer_matrice(lignes, colonnes):
    """
    Crée une matrice vide pour le jeu.

    Args:
        lignes (int): Nombre de lignes de la grille
        colonnes (int): Nombre de colonnes de la grille

    Returns:
        list: Une matrice (liste de listes) remplie de zéros
    """
    return [[0 for _ in range(colonnes)] for _ in range(lignes)]


def afficher_matrice(matrice):
    """
    Affiche la matrice de jeu dans la console avec des emojis.

    Légende:
    - 🔴 : Joueur 1 (valeur 1)
    - 🟡 : Joueur -1 (valeur -1)
    - ⚪ : Case vide (valeur 0)

    Args:
        matrice (list): La matrice de jeu à afficher
    """
    print("\n  ", end="")
    for colonne in range(len(matrice[0])):
        print(f" {colonne} ", end="")
    print("\n  " + "---" * len(matrice[0]))

    for ligne in matrice:
        print("  ", end="")
        for cellule in ligne:
            if cellule == 1:
                symbole = "🔴"
            elif cellule == -1:
                symbole = "🟡"
            else:
                symbole = "⚪"
            print(f"{symbole} ", end="")
        print()
    print()


def ajouter_pion(matrice, joueur, colonne):
    """
    Ajoute un pion du joueur dans la colonne spécifiée.

    Le pion tombe jusqu'à la position la plus basse disponible dans la colonne,
    simulant la gravité.

    Args:
        matrice (list): La matrice de jeu
        joueur (int): 1 ou -1 selon le joueur
        colonne (int): L'indice de la colonne où placer le pion

    Returns:
        int: 0 si le pion a été ajouté avec succès, -1 si la colonne est invalide ou pleine
    """
    lignes = len(matrice)

    if colonne < 0 or colonne >= len(matrice[0]):
        return -1

    for ligne in range(lignes - 1, -1, -1):
        if matrice[ligne][colonne] == 0:
            matrice[ligne][colonne] = joueur
            return 0

    return -1


def verifier_victoire(matrice, nombre_alignes=4):
    """
    Vérifie s'il y a un gagnant dans la partie.

    Examine toutes les directions possibles (horizontal, vertical, diagonales)
    pour trouver une séquence du nombre requis de pions alignés.

    Args:
        matrice (list): La matrice de jeu à vérifier
        nombre_alignes (int): Nombre de pions alignés nécessaires pour gagner (défaut: 4)

    Returns:
        int: 1 si le joueur 1 gagne, -1 si le joueur -1 gagne, 0 si pas de gagnant
    """
    lignes = len(matrice)
    colonnes = len(matrice[0])

    # Vérifier horizontalement
    for ligne in range(lignes):
        for colonne in range(colonnes - nombre_alignes + 1):
            if matrice[ligne][colonne] != 0:
                if all(matrice[ligne][colonne + i] == matrice[ligne][colonne] for i in range(nombre_alignes)):
                    return matrice[ligne][colonne]

    # Vérifier verticalement
    for ligne in range(lignes - nombre_alignes + 1):
        for colonne in range(colonnes):
            if matrice[ligne][colonne] != 0:
                if all(matrice[ligne + i][colonne] == matrice[ligne][colonne] for i in range(nombre_alignes)):
                    return matrice[ligne][colonne]

    # Vérifier diagonale descendante (\)
    for ligne in range(lignes - nombre_alignes + 1):
        for colonne in range(colonnes - nombre_alignes + 1):
            if matrice[ligne][colonne] != 0:
                if all(matrice[ligne + i][colonne + i] == matrice[ligne][colonne] for i in range(nombre_alignes)):
                    return matrice[ligne][colonne]

    # Vérifier diagonale montante (/)
    for ligne in range(nombre_alignes - 1, lignes):
        for colonne in range(colonnes - nombre_alignes + 1):
            if matrice[ligne][colonne] != 0:
                if all(matrice[ligne - i][colonne + i] == matrice[ligne][colonne] for i in range(nombre_alignes)):
                    return matrice[ligne][colonne]

    return 0


def coups_possibles(matrice):
    """
    Retourne la liste des colonnes où il est possible de jouer.

    Une colonne est jouable si sa case du haut (ligne 0) est vide.

    Args:
        matrice (list): La matrice de jeu

    Returns:
        list: Liste des indices de colonnes disponibles
    """
    colonnes = len(matrice[0])
    coups = []

    for colonne in range(colonnes):
        if matrice[0][colonne] == 0:
            coups.append(colonne)

    return coups


def grille_pleine(matrice):
    """
    Vérifie si la grille est complètement remplie.

    Args:
        matrice (list): La matrice de jeu

    Returns:
        bool: True si aucune colonne n'est jouable, False sinon
    """
    for colonne in range(len(matrice[0])):
        if matrice[0][colonne] == 0:
            return False
    return True


def compter_sequences(matrice, joueur, longueur, nombre_alignes=4):
    """
    Compte le nombre de séquences d'une certaine longueur pour un joueur.

    Une séquence valide contient exactement 'longueur' pions du joueur,
    le reste étant des cases vides (0), et aucun pion adverse.
    Cela permet d'identifier les opportunités encore ouvertes.

    Args:
        matrice (list): La matrice de jeu
        joueur (int): 1 ou -1 selon le joueur
        longueur (int): Nombre de pions du joueur dans la séquence
        nombre_alignes (int): Taille de la fenêtre à examiner (défaut: 4)

    Returns:
        int: Nombre de séquences trouvées
    """
    lignes = len(matrice)
    colonnes = len(matrice[0])
    compteur = 0

    # Vérifier horizontalement
    for ligne in range(lignes):
        for colonne in range(colonnes - nombre_alignes + 1):
            sequence = [matrice[ligne][colonne + i] for i in range(nombre_alignes)]
            if sequence.count(joueur) == longueur and sequence.count(0) == nombre_alignes - longueur and sequence.count(
                    -joueur) == 0:
                compteur += 1

    # Vérifier verticalement
    for ligne in range(lignes - nombre_alignes + 1):
        for colonne in range(colonnes):
            sequence = [matrice[ligne + i][colonne] for i in range(nombre_alignes)]
            if sequence.count(joueur) == longueur and sequence.count(0) == nombre_alignes - longueur and sequence.count(
                    -joueur) == 0:
                compteur += 1

    # Vérifier diagonale descendante (\)
    for ligne in range(lignes - nombre_alignes + 1):
        for colonne in range(colonnes - nombre_alignes + 1):
            sequence = [matrice[ligne + i][colonne + i] for i in range(nombre_alignes)]
            if sequence.count(joueur) == longueur and sequence.count(0) == nombre_alignes - longueur and sequence.count(
                    -joueur) == 0:
                compteur += 1

    # Vérifier diagonale montante (/)
    for ligne in range(nombre_alignes - 1, lignes):
        for colonne in range(colonnes - nombre_alignes + 1):
            sequence = [matrice[ligne - i][colonne + i] for i in range(nombre_alignes)]
            if sequence.count(joueur) == longueur and sequence.count(0) == nombre_alignes - longueur and sequence.count(
                    -joueur) == 0:
                compteur += 1

    return compteur


def evaluer_position(matrice, joueur_ia, nombre_alignes=4):
    """
    Évalue la qualité d'une position pour l'IA.

    Utilise une fonction d'évaluation heuristique qui prend en compte:
    - Les victoires immédiates (score maximal/minimal)
    - Le nombre de séquences de 3 et 2 pions alignés
    - Le contrôle du centre (stratégiquement important)
    - Les menaces adverses (fortement pénalisées)

    Args:
        matrice (list): La matrice de jeu à évaluer
        joueur_ia (int): 1 ou -1 selon qui est l'IA
        nombre_alignes (int): Nombre de pions alignés pour gagner (défaut: 4)

    Returns:
        int: Score de la position (positif = bon pour l'IA, négatif = mauvais pour l'IA)
    """
    # Vérifier victoire immédiate
    victoire = verifier_victoire(matrice, nombre_alignes)
    if victoire == joueur_ia:
        return 10000  # Victoire de l'IA = excellent
    elif victoire == -joueur_ia:
        return -10000  # Victoire de l'adversaire = catastrophique

    score = 0

    # Compter les séquences pour l'IA
    ia_trois = compter_sequences(matrice, joueur_ia, 3, nombre_alignes)
    ia_deux = compter_sequences(matrice, joueur_ia, 2, nombre_alignes)

    # Compter les séquences pour l'adversaire
    adversaire_trois = compter_sequences(matrice, -joueur_ia, 3, nombre_alignes)
    adversaire_deux = compter_sequences(matrice, -joueur_ia, 2, nombre_alignes)

    # Pondération : bloquer 3 alignés adverses est CRITIQUE
    score += ia_trois * 100  # 3 pions alignés IA = très bon
    score += ia_deux * 10  # 2 pions alignés IA = bon
    score -= adversaire_trois * 150  # 3 pions alignés adversaire = URGENT à bloquer
    score -= adversaire_deux * 15  # 2 pions alignés adversaire = à surveiller

    # Bonus pour jouer au centre (colonnes centrales sont stratégiques)
    colonnes = len(matrice[0])
    centre = colonnes // 2
    for ligne in range(len(matrice)):
        if matrice[ligne][centre] == joueur_ia:
            score += 3

    return score


def minimax(matrice, profondeur, est_maximisant, joueur_ia, nombre_alignes=4):
    """
    Implémente l'algorithme Minimax pour trouver le meilleur coup.

    Explore récursivement l'arbre des possibilités jusqu'à une certaine profondeur
    ou jusqu'à une fin de partie. L'IA maximise son score tandis que l'adversaire
    le minimise.

    Args:
        matrice (list): État actuel du jeu
        profondeur (int): Profondeur restante à explorer (0 = arrêt)
        est_maximisant (bool): True si c'est le tour de l'IA, False pour l'adversaire
        joueur_ia (int): 1 ou -1 selon qui est l'IA
        nombre_alignes (int): Nombre de pions alignés pour gagner (défaut: 4)

    Returns:
        int: La valeur de la position (score d'évaluation)
    """
    # Condition d'arrêt
    victoire = verifier_victoire(matrice, nombre_alignes)
    if profondeur == 0 or victoire != 0 or grille_pleine(matrice):
        return evaluer_position(matrice, joueur_ia, nombre_alignes)

    coups = coups_possibles(matrice)

    if est_maximisant:
        # Tour de l'IA (maximise)
        valeur = float('-inf')
        for coup in coups:
            nouvelle_matrice = copy.deepcopy(matrice)
            ajouter_pion(nouvelle_matrice, joueur_ia, coup)
            evaluation = minimax(nouvelle_matrice, profondeur - 1, False, joueur_ia, nombre_alignes)
            valeur = max(valeur, evaluation)
        return valeur
    else:
        # Tour de l'adversaire (minimise)
        valeur = float('inf')
        for coup in coups:
            nouvelle_matrice = copy.deepcopy(matrice)
            ajouter_pion(nouvelle_matrice, -joueur_ia, coup)
            evaluation = minimax(nouvelle_matrice, profondeur - 1, True, joueur_ia, nombre_alignes)
            valeur = min(valeur, evaluation)
        return valeur


def meilleur_coup_ia(matrice, joueur_ia, profondeur=5, nombre_alignes=4):
    """
    Détermine le meilleur coup pour l'IA en utilisant l'algorithme Minimax.

    Stratégie en 3 priorités:
    1. Gagner immédiatement si possible
    2. Bloquer une victoire adverse imminente
    3. Utiliser Minimax pour trouver le meilleur coup stratégique

    Args:
        matrice (list): État actuel du jeu
        joueur_ia (int): 1 ou -1 selon qui est l'IA
        profondeur (int): Profondeur de recherche Minimax (défaut: 5)
        nombre_alignes (int): Nombre de pions alignés pour gagner (défaut: 4)

    Returns:
        int or None: L'indice de la colonne du meilleur coup, ou None si aucun coup possible
    """
    coups = coups_possibles(matrice)

    if not coups:
        return None

    # PRIORITÉ 1 : Vérifier si l'IA peut gagner immédiatement
    for coup in coups:
        matrice_temporaire = copy.deepcopy(matrice)
        ajouter_pion(matrice_temporaire, joueur_ia, coup)
        if verifier_victoire(matrice_temporaire, nombre_alignes) == joueur_ia:
            return coup  # Gagner immédiatement !

    # PRIORITÉ 2 : Vérifier si l'adversaire peut gagner (BLOQUER directement)
    for coup in coups:
        matrice_temporaire = copy.deepcopy(matrice)
        ajouter_pion(matrice_temporaire, -joueur_ia, coup)
        if verifier_victoire(matrice_temporaire, nombre_alignes) == -joueur_ia:
            return coup  # Bloquer la victoire adverse !

    # PRIORITÉ 3 : Utiliser Minimax pour trouver le meilleur coup stratégique
    meilleur_coup = coups[0]
    meilleure_valeur = float('-inf')

    for coup in coups:
        nouvelle_matrice = copy.deepcopy(matrice)
        ajouter_pion(nouvelle_matrice, joueur_ia, coup)

        valeur = minimax(nouvelle_matrice, profondeur - 1, False, joueur_ia, nombre_alignes)

        if valeur > meilleure_valeur:
            meilleure_valeur = valeur
            meilleur_coup = coup

    return meilleur_coup