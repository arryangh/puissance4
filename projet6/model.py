import copy

# Historique pour annuler/refaire
lHistorique_matrices = []
iIndice_historique = -1


def Reinitialiser_historique(lMatrice):
    """
    Réinitialise l'historique des coups et sauvegarde l'état initial.
    Mettre la matrice de départ (vide) au début de l'historique vièrge

    Appelé au début d'une nouvelle partie pour effacer l'historique précédent
    et commencer avec un historique vierge contenant uniquement l'état initial.

    Args:
        lMatrice (list): La matrice de jeu initiale à sauvegarder
    """
    global lHistorique_matrices, iIndice_historique
    lHistorique_matrices = []  # une liste de matrice (dimension 3)
    iIndice_historique = -1
    Sauvegarder_etat(lMatrice)  # mettre la première matrice à ce moment là


def Sauvegarder_etat(lMatrice):
    """
    Sauvegarde l'état actuel de la matrice dans l'histrique.

    Si des annulation ont été effectués (l'indice est en arrière dans l'historique),
    cette fonction coupe tout l'historique future avant d'ajouter le nouvel état.

    Args:
        lMatrice (list): La matrice de jeu à sauvegarder
    """
    global lHistorique_matrices, iIndice_historique

    # Si on a fait annuler puis un nouveau coup → on coupe le futur
    if iIndice_historique < len(lHistorique_matrices) - 1:
        lHistorique_matrices = lHistorique_matrices[:iIndice_historique + 1]

    lHistorique_matrices.append(copy.deepcopy(lMatrice))  # deep copy pour réecrir à un nouveau endroit du mémoire (et par réferncer pour éviter les bugs)
    iIndice_historique += 1


def Undo_redo(lMatrice, cAction, cMode_ia):
    """
    Gère les opérations de undo/redo (demandé dans l'énnoncé)

    En mode 1v1, undo/redo 1 seul coup. (pour que chaque personne puisse rejouer)
    En mode IA, undo/redo 2 coup (le coup du joueur + le coup de l'IA). (pour que l'IA puisse par rapport au nouveau coup)


    Args:
        lMatrice (list): La matrice de jeu à modifier
        cAction (str): "u" pour annuler (undo), "r" pour refaire (redo)
        cMode_ia: None si mode 1v1, sinon indique le mode IA

    Returns:
        int: 0 si succès, -1 si impossible (début/fin d'historique atteint)
    """
    global lHistorique_matrices, iIndice_historique

    # En mode IA on saute 2 coups, sinon 1
    if cMode_ia is not None:  # si c'est le mode IA
        iPas = 2
    else:  # si c'est pas le mode IA
        iPas = 1

    if cAction == "u":  # u = UNDO
        if iIndice_historique - iPas >= 0:
            iIndice_historique -= iPas
        else:  # iIndice_historique - iPas < 0
            return -1  # opération impossible

    elif cAction == "r":  # r = REDO
        if iIndice_historique + iPas < len(lHistorique_matrices):
            iIndice_historique += iPas
        else:  # iIndice_historique + iPas >= len(lHistorique_matrices)
            return -1  # opération impossible

    else:  # dans tout autre cas
        return -1

    # Recharger la matrice depuis l'historique
    cEtat = lHistorique_matrices[iIndice_historique]
    for i in range(len(lMatrice)):
        for j in range(len(lMatrice[0])):
            lMatrice[i][j] = cEtat[i][j]

    return 0


def Creer_matrice(iLignes, iColonnes):
    """
    Crée une matrice vide pour le jeu.

    Args:
        iLignes (int): Nombre de lignes de la grille
        iColonnes (int): Nombre de colonnes de la grille

    Returns:
        list: Une matrice (liste de listes) remplie de zéros
    """
    lMatrice = []
    for iBoucle in range(iLignes):
        lLigne = []
        for jBoucle in range(iColonnes):
            lLigne.append(0)
        lMatrice.append(lLigne)
    return lMatrice




def Afficher_matrice(lMatrice):
    """
    Affiche la matrice de jeu dans la console avec des emojji.

    Légende:
    - 🔴 : Joueur 1 (valeur 1)
    - 🟡 : Joueur -1 (valeur -1)
    - ⚪ : Case vide (valeur 0)

    Args:
        lMatrice (list): La matrice de jeu à afficher
    """
    print("\n  ", end="")
    for iColonne in range(len(lMatrice[0])):
        print(f" {iColonne} ", end="")
    print("\n  " + "---" * len(lMatrice[0]))

    for lLigne in lMatrice:
        print("  ", end="")
        for iCellule in lLigne:
            if iCellule == 1:
                cSymbole = "🔴"
            elif iCellule == -1:
                cSymbole = "🟡"
            else:
                cSymbole = "⚪"
            print(f"{cSymbole} ", end="")
        print()
    print()


def Ajouter_pion(lMatrice, iJoueur, iColonne):
    """
    Ajoute un pion du joueur (1 ou -1) dans la colonne donné en paramètre.

    Le pion tombe jusqu'à la position la plus basse disponible dans la colonne,
    simulant la gravité.

    Args:
        lMatrice (list): La matrice de jeu
        iJoueur (int): 1 ou -1 selon le joueur
        iColonne (int): L'indice de la colonne où placer le pion

    Returns:
        int: 0 si le pion a été ajouté avec succès, -1 si la colonne est invalide ou pleine
    """
    iLignes = len(lMatrice)

    if iColonne < 0 or iColonne >= len(lMatrice[0]):  # gestion d'erreur de numéro de colonne
        print("Numero de colonne en dehors de l'interval autorisé.")
        return -1

    for iLigne in range(iLignes - 1, -1, -1):  # boucle inverse pour placer le pion le plus bas possible
        if lMatrice[iLigne][iColonne] == 0:
            lMatrice[iLigne][iColonne] = iJoueur
            return 0

    return -1


def Verifier_victoire(lMatrice, iNombre_alignes=4):
    """
    Vérifie s'il y a un gagnant dans la partie.

    Examine toutes les directions possibles (horizontal, vertical, diagonale et antidiagnoale)
    pour trouver une séquence du nombre requis de pions alignés (4 par défaut mais peut changer).

    Args:
        lMatrice (list): La matrice de jeu à vérifier
        iNombre_alignes (int): Nombre de pions alignés nécessaires pour gagner (par défaut: 4)

    Returns:
        int: 1 si le joueur 1 gagne, -1 si le joueur -1 gagne, 0 si pas de gagnant
    """
    iLignes = len(lMatrice)  # nombre de lignes
    iColonnes = len(lMatrice[0]) # nombre de colonnes

    # Vérifier horizontalement
    for iLigne in range(iLignes):
        for iColonne in range(iColonnes - iNombre_alignes + 1):
            if lMatrice[iLigne][iColonne] != 0:  # continuer la vérification si pas de cellule sans pion (pas de cellule vide)
                bAlignement_horizontal = True  # alignement de pion (on sait pas encore si pions identiques)
                for i in range(iNombre_alignes):  # # vérifier si les pions identiques sont de même "couleur"
                    if lMatrice[iLigne][iColonne + i] != lMatrice[iLigne][iColonne]:
                        bAlignement_horizontal = False
                        break

                if bAlignement_horizontal:
                    return lMatrice[iLigne][iColonne]  # renvoyer le numéro du pion si n pion alignées

    # Vérifier verticalement
    for iLigne in range(iLignes - iNombre_alignes + 1):
        for iColonne in range(iColonnes):
            if lMatrice[iLigne][iColonne] != 0:  # continuer la vérification si pas de cellule sans pion (pas de cellule vide)
                bAlignement_vertical = True  # alignement de pion (on sait pas encore si pions identiques)
                for i in range(iNombre_alignes):  # vérifier si les pions identiques sont de même "couleur"
                    if lMatrice[iLigne + i][iColonne] != lMatrice[iLigne][iColonne]:
                        bAlignement_vertical = False
                        break

                if bAlignement_vertical:
                    return lMatrice[iLigne][iColonne]  # renvoyer le numéro du pion si n pion alignées

    # Vérifier diagonale descendante (\)
    for iLigne in range(iLignes - iNombre_alignes + 1):
        for iColonne in range(iColonnes - iNombre_alignes + 1):
            if lMatrice[iLigne][iColonne] != 0:  # continuer la vérification si pas de cellule sans pion (pas de cellule vide)
                bAlignement_diag_desc = True  # alignement de pion (on sait pas encore si pions identiques)
                for i in range(iNombre_alignes):  # vérifier si les pions identiques sont de même "couleur"
                    if lMatrice[iLigne + i][iColonne + i] != lMatrice[iLigne][iColonne]:
                        bAlignement_diag_desc = False
                        break

                if bAlignement_diag_desc:
                    return lMatrice[iLigne][iColonne]  # renvoyer le numéro du pion si n pion alignées

    # Vérifier diagonale montante (/)
    for iLigne in range(iNombre_alignes - 1, iLignes):
        for iColonne in range(iColonnes - iNombre_alignes + 1):
            if lMatrice[iLigne][iColonne] != 0:  # continuer la vérification si pas de cellule sans pion (pas de cellule vide)
                bAlignement_diag_mont = True  # alignement de pion (on sait pas encore si pions identiques)
                for i in range(iNombre_alignes):  # vérifier si les pions identiques sont de même "couleur"
                    if lMatrice[iLigne - i][iColonne + i] != lMatrice[iLigne][iColonne]:
                        bAlignement_diag_mont = False
                        break

                if bAlignement_diag_mont:
                    return lMatrice[iLigne][iColonne]  # renvoyer le numéro du pion si n pion alignées

    return 0  # si après toutes les vérifications et boucles il n'y a pas n pions aligné de même couleur (cas le plus récurant)


def Coups_possibles(lMatrice):
    """
    Retourne la liste des colonnes où il est possible de jouer.

    Une colonne est jouable si sa case du haut (ligne 0) est vide. (la cellule la plus haute de la colonne)

    Args:
        lMatrice (list): La matrice de jeu

    Returns:
        list: Liste des indices de colonnes disponibles
    """
    iColonnes = len(lMatrice[0])  # nombre de colonne
    lCoups = []

    for iColonne in range(iColonnes):
        if lMatrice[0][iColonne] == 0:  # si l'élèment le plus haut de la colonne est vide (il reste des places encore)
            lCoups.append(iColonne)  # on ajoute le numéro de colonne à la liste d'entier "colonnes"

    return lCoups


def Grille_pleine(lMatrice):
    """
    Vérifie si la grille est complètement remplie.

    Args:
        lMatrice (list): La matrice de jeu

    Returns:
        bool: True si aucune colonne n'est jouable, False sinon
    """
    for iColonne in range(len(lMatrice[0])):
        if lMatrice[0][iColonne] == 0:
            return False  # si il y a un pion en haut d'au moins une colonne
        
    return True  # si toutes les colonnes sont remplies


def Compter_sequences(lMatrice, iJoueur, iLongueur, iNombre_alignes=4):
    """
    Compte le nombre de séquences d'une certaine longueur pour un joueur. (pour évaluer la dangeureusité d'une position)

    Une séquence valide contient exactement 'iLongueur' pions du joueur,
    le reste étant des cases vides (0), et aucun pion adverse.
    ça permet d'identifier les opportunités encore ouvertes. (les bons coups à jouer)

    Args:
        lMatrice (list): La matrice de jeu
        iJoueur (int): 1 ou -1 selon le joueur
        iLongueur (int): Nombre de pions du joueur dans la séquence
        iNombre_alignes (int): Taille de la fenêtre à examiner (défaut: 4)

    Returns:
        int: Nombre de séquences trouvées
    """
    iLignes = len(lMatrice)
    iColonnes = len(lMatrice[0])
    iCompteur = 0

    # Vérifier horizontalement
    for iLigne in range(iLignes): # Pour chaque ligne de la matrice
        for iColonne in range(iColonnes - iNombre_alignes + 1): # Pour chaque position de départ possible pour une fenêtre horizontale de taille iNombre_alignes
            lSequence = [] # Récupérer tous les éléments horizontales
            for iBoucle in range(iNombre_alignes):
                lSequence.append(lMatrice[iLigne][iColonne + iBoucle])

            # Vérifier les conditions : exactement 'iLongueur' pions du joueur et le reste des cases vides, et aucun pion adverse
            if (lSequence.count(iJoueur) == iLongueur and
                    lSequence.count(0) == iNombre_alignes - iLongueur and
                    lSequence.count(-iJoueur) == 0):
                iCompteur += 1

    # Vérifier verticalement
    # Pour chaque position de départ possible pour une fenêtre verticale de taille iNombre_alignes
    for iLigne in range(iLignes - iNombre_alignes + 1):
        # Pour chaque colonne de la matrice
        for iColonne in range(iColonnes):
            lSequence = []
            # Récupérer tous les éléments dans la fenêtre verticale
            for iBoucle in range(iNombre_alignes):
                lSequence.append(lMatrice[iLigne + iBoucle][iColonne])

            # Vérifier les conditions: exactement 'iLongueur' pions du joueur,
            # le reste des cases vides, et aucun pion adverse
            if (lSequence.count(iJoueur) == iLongueur and
                    lSequence.count(0) == iNombre_alignes - iLongueur and
                    lSequence.count(-iJoueur) == 0):
                iCompteur += 1

    # Vérifier diagonale descendante (\)
    # Pour chaque position de départ possible pour une fenêtre diagonale descendante de taille iNombre_alignes
    for iLigne in range(iLignes - iNombre_alignes + 1):
        for iColonne in range(iColonnes - iNombre_alignes + 1):
            lSequence = []
            # Récupérer tous les éléments dans la fenêtre diagonale descendante
            for iBoucle in range(iNombre_alignes):
                lSequence.append(lMatrice[iLigne + iBoucle][iColonne + iBoucle])

            # Vérifier les conditions: exactement 'iLongueur' pions du joueur,
            # le reste des cases vides, et aucun pion adverse
            if (lSequence.count(iJoueur) == iLongueur and
                    lSequence.count(0) == iNombre_alignes - iLongueur and
                    lSequence.count(-iJoueur) == 0):
                iCompteur += 1

    # Vérifier diagonale montante (/)
    # Pour chaque position de départ possible pour une fenêtre diagonale montante de taille iNombre_alignes
    for iLigne in range(iNombre_alignes - 1, iLignes):
        for iColonne in range(iColonnes - iNombre_alignes + 1):
            lSequence = []
            # Récupérer tous les éléments dans la fenêtre diagonale montante
            for iBoucle in range(iNombre_alignes):
                lSequence.append(lMatrice[iLigne - iBoucle][iColonne + iBoucle])

            # Vérifier les conditions: exactement 'iLongueur' pions du joueur,
            # le reste des cases vides, et aucun pion adverse
            if (lSequence.count(iJoueur) == iLongueur and
                    lSequence.count(0) == iNombre_alignes - iLongueur and
                    lSequence.count(-iJoueur) == 0):
                iCompteur += 1

    return iCompteur


def Evaluer_position(lMatrice, iJoueur_ia, iNombre_alignes=4):
    """
    Évalue la qualité d'une position pour le minmax.

    Utilise une fonction d'évaluation heuristique qui prend en compte:
    - Les victoires immédiates (score maximal/minimal)
    - Le nombre de séquences de 2 et 3 pion aligné
    - Le contrôle du centre (stratégiquement important)
    - Les menaces adverses (fortement pénalisées)

    Args:
        lMatrice (list): La matrice de jeu à évaluer
        iJoueur_ia (int): 1 ou -1 selon qui est l'IA
        iNombre_alignes (int): Nombre de pions alignés pour gagner (défaut: 4)

    Returns:
        int: Score de la position (positif = bon pour l'IA, négatif = mauvais pour l'IA)
    """
    # Vérifier victoire immédiate
    iVictoire = Verifier_victoire(lMatrice, iNombre_alignes)
    if iVictoire == iJoueur_ia:
        return 10000  # Victoire de l'IA = excellent
    elif iVictoire == -iJoueur_ia:
        return -10000  # Victoire de l'adversair = catastrophique

    iScore = 0

    # Compter les séquences pour l'IA
    iIa_trois = Compter_sequences(lMatrice, iJoueur_ia, 3, iNombre_alignes)
    iIa_deux = Compter_sequences(lMatrice, iJoueur_ia, 2, iNombre_alignes)

    # Compter les séquences pour l'adversair
    iAdversaire_trois = Compter_sequences(lMatrice, -iJoueur_ia, 3, iNombre_alignes)
    iAdversaire_deux = Compter_sequences(lMatrice, -iJoueur_ia, 2, iNombre_alignes)

    # Pondération : bloquer 3 alignés adverses est CRITIQUE
    iScore += iIa_trois * 100  # 3 pions alignés IA = très bien
    iScore += iIa_deux * 10  # 2 pions alignés IA = bien
    iScore -= iAdversaire_trois * 150  # 3 pions alignés adversair = URGENT à bloquer
    iScore -= iAdversaire_deux * 15  # 2 pions alignés adversair = à surveiller

    # Bonus pour jouer au centre (colonnes centrales sont stratégiques)
    iColonnes = len(lMatrice[0])
    iCentre = iColonnes // 2
    for iLigne in range(len(lMatrice)):
        if lMatrice[iLigne][iCentre] == iJoueur_ia:
            iScore += 3

    return iScore


def Minimax(lMatrice, iProfondeur, bEst_maximisant, iJoueur_ia, iNombre_alignes=4):
    """
    Implémente l'algorithme Minimax pour trouver le meilleur coup.
    Algorithme obligatoire de M.BILLAUT

    Explore récursivement l'arbre des possibilités jusqu'à une certaine profondeure
    ou jusqu'à une fin de partie. L'IA maximise son score tandis que l'adversair
    le minimise.

    Args:
        lMatrice (list): État actuel du jeu
        iProfondeur (int): Profondeur restant à explorer (0 = arrêt)
        bEst_maximisant (bool): True si c'est le tour de l'IA, False pour l'adversair
        iJoueur_ia (int): 1 ou -1 selon qui est l'IA
        iNombre_alignes (int): Nombre de pions alignés pour gagner (défaut: 4)

    Returns:
        int: La valeur de la position (score d'évaluation)
    """
    # Condition d'arrêt
    iVictoire = Verifier_victoire(lMatrice, iNombre_alignes)
    if iProfondeur == 0 or iVictoire != 0 or Grille_pleine(lMatrice):
        return Evaluer_position(lMatrice, iJoueur_ia, iNombre_alignes)

    lCoups = Coups_possibles(lMatrice)

    if bEst_maximisant:
        # Tour de l'IA (maximise)
        fValeur = float('-inf')  # - infinie
        for iCoup in lCoups:
            lNouvelle_matrice = copy.deepcopy(lMatrice)
            Ajouter_pion(lNouvelle_matrice, iJoueur_ia, iCoup)
            iEvaluation = Minimax(lNouvelle_matrice, iProfondeur - 1, False, iJoueur_ia, iNombre_alignes)
            fValeur = max(fValeur, iEvaluation)

        return fValeur


    else:
        # Tour de l'adversair (minimise)
        fValeur = float('inf') # + infinie
        for iCoup in lCoups:
            lNouvelle_matrice = copy.deepcopy(lMatrice)
            Ajouter_pion(lNouvelle_matrice, -iJoueur_ia, iCoup)
            iEvaluation = Minimax(lNouvelle_matrice, iProfondeur - 1, True, iJoueur_ia, iNombre_alignes)
            fValeur = min(fValeur, iEvaluation)

        return fValeur


def Meilleur_coup_ia(lMatrice, iJoueur_ia, iProfondeur=5, iNombre_alignes=4):
    """
    Détermine le meilleur coup pour l'IA en utilisant l'algorithme Minimax.

    Stratégie en 3 priorités:
    1. Gagner immédiatement si possible
    2. Bloquer une victoire adverse imminente
    3. Utiliser Minimax pour trouver le meilleur coup stratégique

    Args:
        lMatrice (list): État actuel du jeu
        iJoueur_ia (int): 1 ou -1 selon qui est l'IA
        iProfondeur (int): Profondeur de recherche Minimax (défaut: 5)
        iNombre_alignes (int): Nombre de pions alignés pour gagner (défaut: 4)

    Returns:
        int or None: L'indice de la colonne du meilleur coup, ou None si aucun coup possible
    """
    lCoups = Coups_possibles(lMatrice)

    if not lCoups: # si pas de coups à jouer
        return None

    # PRIORITÉ 1 : Vérifier si l'IA peut gagner immédiatement
    for iCoup in lCoups:
        lMatrice_temporaire = copy.deepcopy(lMatrice)
        Ajouter_pion(lMatrice_temporaire, iJoueur_ia, iCoup)

        if Verifier_victoire(lMatrice_temporaire, iNombre_alignes) == iJoueur_ia:
            return iCoup  # renvoie le coup gagnant imédiatement

    # PRIORITÉ 2 : Vérifier si l'adversair peut gagner (BLOQUER directement)
    for iCoup in lCoups:
        lMatrice_temporaire = copy.deepcopy(lMatrice)
        Ajouter_pion(lMatrice_temporaire, -iJoueur_ia, iCoup)

        if Verifier_victoire(lMatrice_temporaire, iNombre_alignes) == -iJoueur_ia:
            return iCoup  # renvoie le coup blockant imédiatement

    # PRIORITÉ 3 : Utiliser Minimax pour trouver le meilleur coup stratégique
    iMeilleur_coup = lCoups[0]
    fMeilleure_valeur = float('-inf')

    for iCoup in lCoups:
        lNouvelle_matrice = copy.deepcopy(lMatrice)
        Ajouter_pion(lNouvelle_matrice, iJoueur_ia, iCoup)

        fValeur = Minimax(lNouvelle_matrice, iProfondeur - 1, False, iJoueur_ia, iNombre_alignes)

        if fValeur > fMeilleure_valeur:
            fMeilleure_valeur = fValeur
            iMeilleur_coup = iCoup

    return iMeilleur_coup