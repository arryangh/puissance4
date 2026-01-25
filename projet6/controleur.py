import tkinter as tk
from vue import VueGrille, VueAccueil, VueParametres, VueActions
from model import *


class ControleurJeu:
    """
    Contrôleur principal du jeu Puissance 4.

    Gère la logique du jeu, les interactions utilisateur, l'animation des pions,
    la détection de fin de partie et l'intégration avec l'IA.
    """

    def __init__(self, racine, lignes=6, colonnes=7, nombre_alignes=4, mode_ia=None, difficulte=None):
        """
        Initialise le contrôleur de jeu.

        Args:
            racine (tk.Tk): Fenêtre principale Tkinter
            lignes (int): Nombre de lignes de la grille (défaut: 6)
            colonnes (int): Nombre de colonnes de la grille (défaut: 7)
            nombre_alignes (int): Nombre de pions à aligner pour gagner (défaut: 4)
            mode_ia (str or None): "rouge" si l'IA joue rouge, "jaune" si jaune, None en mode 1v1
            difficulte (int or None): Profondeur de recherche de l'IA (1=facile, 3=moyen, 5=difficile)
        """
        self.CTJ_racine = racine
        self.CTJ_lignes = lignes
        self.CTJ_colonnes = colonnes
        self.CTJ_nombre_alignes = nombre_alignes
        self.CTJ_mode_ia = mode_ia
        self.CTJ_difficulte = difficulte

        # Calcul de la taille des cellules pour écrans 1920x1080
        # Calculer la taille en fonction de la dimension la plus contraignante (pour que ça marche partout)
        taille_max_lignes = 690 / lignes  # Hauteur max disponible (6 lignes * 115 = 690)
        taille_max_colonnes = 805 / colonnes  # Largeur max disponible (7 colonnes * 115 = 805)

        # Prendre la plus petite des deux pour que tout rentre
        self.CTJ_taille_cellule = int(min(taille_max_lignes, taille_max_colonnes, 115))  # Max 115px

        self.CTJ_animation_en_cours = False
        self.CTJ_partie_terminee = False

        # Création de la matrice de jeu
        self.CTJ_matrice = creer_matrice(lignes, colonnes)
        reinitialiser_historique(self.CTJ_matrice)
        self.CTJ_joueur_actuel = 1  # 1 pour rouge, -1 pour jaune

        # Création de la vue
        self.CTJ_vue = VueGrille(racine, lignes, colonnes, self.CTJ_taille_cellule)

        # Binding des événements souris
        self.CTJ_vue.VGR_canvas.bind("<Motion>", self.sur_mouvement_souris)
        self.CTJ_vue.VGR_canvas.bind("<Button-1>", self.sur_clic)
        self.CTJ_vue.VGR_canvas.bind("<Leave>", self.sur_sortie_souris)

    def sur_mouvement_souris(self, evenement):
        """
        Gère le mouvement de la souris pour afficher l'effet de survol.

        Affiche un effet d'ombre sur la colonne survolée, sauf si une animation
        est en cours, la partie est terminée, ou si c'est le tour de l'IA.

        Args:
            evenement (tk.Event): Événement de mouvement de souris
        """
        if self.CTJ_animation_en_cours or self.CTJ_partie_terminee:
            return

        # Bloquer le survol si c'est le tour de l'IA
        if self.CTJ_mode_ia and self.est_tour_ia():
            return

        colonne = evenement.x // self.CTJ_taille_cellule

        if 0 <= colonne < self.CTJ_colonnes:
            if colonne != self.CTJ_vue.VGR_colonne_survol:
                self.CTJ_vue.afficher_effet_survol(colonne)
        else:
            self.CTJ_vue.effacer_effet_survol()

    def sur_sortie_souris(self, evenement):
        """
        Efface l'effet de survol quand la souris quitte le canvas.

        Args:
            evenement (tk.Event): Événement de sortie de souris
        """
        self.CTJ_vue.effacer_effet_survol()

    def sur_clic(self, evenement):
        """
        Gère le clic de souris pour ajouter un pion.

        Ignore les clics si une animation est en cours, la partie est terminée,
        ou si c'est le tour de l'IA.

        Args:
            evenement (tk.Event): Événement de clic de souris
        """
        if self.CTJ_animation_en_cours or self.CTJ_partie_terminee:
            return

        # Bloquer les clics si c'est le tour de l'IA
        if self.CTJ_mode_ia and self.est_tour_ia():
            return

        colonne = evenement.x // self.CTJ_taille_cellule

        if 0 <= colonne < self.CTJ_colonnes:
            self.jouer_coup(colonne)

    def est_tour_ia(self):
        """
        Vérifie si c'est le tour de l'IA de jouer.

        Returns:
            bool: True si c'est le tour de l'IA, False sinon
        """
        if self.CTJ_mode_ia == "rouge" and self.CTJ_joueur_actuel == 1:
            return True
        if self.CTJ_mode_ia == "jaune" and self.CTJ_joueur_actuel == -1:
            return True
        return False

    def tour_ia(self):
        """
        Fait jouer l'IA en calculant et en jouant le meilleur coup.

        Utilise l'algorithme Minimax avec la profondeur correspondant
        au niveau de difficulté choisi.
        """
        if self.CTJ_partie_terminee:
            return

        joueur_ia = 1 if self.CTJ_mode_ia == "rouge" else -1
        colonne = meilleur_coup_ia(self.CTJ_matrice, joueur_ia, self.CTJ_difficulte, self.CTJ_nombre_alignes)

        if colonne is not None:
            self.jouer_coup(colonne)

    def jouer_coup(self, colonne):
        """
        Tente de jouer un coup dans la colonne spécifiée.

        Trouve la ligne de destination (la plus basse disponible), ajoute le pion
        à la matrice, sauvegarde l'état et lance l'animation.

        Args:
            colonne (int): L'indice de la colonne où jouer
        """
        ligne_destination = None
        for ligne in range(self.CTJ_lignes - 1, -1, -1):
            if self.CTJ_matrice[ligne][colonne] == 0:
                ligne_destination = ligne
                break

        if ligne_destination is None:
            print("Colonne pleine !")
            return

        resultat = ajouter_pion(self.CTJ_matrice, self.CTJ_joueur_actuel, colonne)
        sauvegarder_etat(self.CTJ_matrice)

        if resultat == 0:
            self.animer_chute_pion(colonne, ligne_destination, self.CTJ_joueur_actuel)

    def animer_chute_pion(self, colonne, ligne_finale, joueur):
        """
        Lance l'animation de chute du pion.

        Bloque les interactions pendant l'animation et vérifie la fin de partie
        une fois l'animation terminée.

        Args:
            colonne (int): L'indice de la colonne
            ligne_finale (int): L'indice de la ligne finale du pion
            joueur (int): 1 ou -1 selon le joueur
        """
        self.CTJ_animation_en_cours = True
        self.CTJ_vue.effacer_effet_survol()

        def fin_animation():
            """Fonction appelée à la fin de l'animation."""
            self.CTJ_animation_en_cours = False
            self.verifier_fin_partie()

        self.CTJ_vue.animer_chute_pion(colonne, ligne_finale, joueur, fin_animation)

    def verifier_fin_partie(self):
        """
        Vérifie si la partie est terminée (victoire ou match nul).

        Affiche le message approprié si la partie est terminée, sinon
        change de joueur et fait jouer l'IA si c'est son tour.
        """
        resultat = verifier_victoire(self.CTJ_matrice, self.CTJ_nombre_alignes)

        if resultat == 1:
            self.CTJ_partie_terminee = True
            self.CTJ_vue.effacer_effet_survol()
            self.CTJ_vue.afficher_message("Victoire du ROUGE!")
            print("\n" + "=" * 50)
            afficher_matrice(self.CTJ_matrice)
            print("Victoire du joueur ROUGE !")
            print("=" * 50)

        elif resultat == -1:
            self.CTJ_partie_terminee = True
            self.CTJ_vue.effacer_effet_survol()
            self.CTJ_vue.afficher_message("Victoire du JAUNE !")
            print("\n" + "=" * 50)
            afficher_matrice(self.CTJ_matrice)
            print("Victoire du joueur JAUNE !")
            print("=" * 50)

        elif self.grille_pleine():
            self.CTJ_partie_terminee = True
            self.CTJ_vue.effacer_effet_survol()
            self.CTJ_vue.afficher_message("Match nul !")
            print("\n" + "=" * 50)
            afficher_matrice(self.CTJ_matrice)
            print("Match nul !")
            print("=" * 50)

        else:
            self.CTJ_joueur_actuel *= -1

            # Si c'est le tour de l'IA, la faire jouer après un court délai
            if self.CTJ_mode_ia and self.est_tour_ia():
                self.CTJ_racine.after(500, self.tour_ia)

    def grille_pleine(self):
        """
        Vérifie si la grille est complètement pleine.

        Returns:
            bool: True si toutes les colonnes sont pleines, False sinon
        """
        for colonne in range(self.CTJ_colonnes):
            if self.CTJ_matrice[0][colonne] == 0:
                return False
        return True

    def annuler(self):
        """
        Annule le dernier coup (ou les deux derniers en mode IA).

        En mode 1v1, annule un coup et change de joueur.
        En mode IA, annule deux coups (joueur + IA) pour que le joueur rejoue.
        """
        if undo_redo(self.CTJ_matrice, "u", self.CTJ_mode_ia) == 0:
            # En mode IA on recule de 2 coups → le joueur rejoue
            if self.CTJ_mode_ia is not None:
                pass
            else:
                # En 1v1 on change de joueur
                self.CTJ_joueur_actuel *= -1

            self.CTJ_partie_terminee = False
            self.CTJ_vue.rafraichir_grille(self.CTJ_matrice)

    def refaire(self):
        """
        Rétablit le coup précédemment annulé.

        En mode 1v1, refait un coup et change de joueur.
        En mode IA, refait deux coups (joueur + IA) pour maintenir la cohérence.
        """
        if undo_redo(self.CTJ_matrice, "r", self.CTJ_mode_ia) == 0:
            # En mode IA on rejoue un tour complet → le joueur reste le même
            if self.CTJ_mode_ia is not None:
                pass
            else:
                self.CTJ_joueur_actuel *= -1

            self.CTJ_vue.rafraichir_grille(self.CTJ_matrice)


class ControleurApplication:
    """
    Contrôleur principal de l'application.

    Gère la navigation entre les différentes vues (accueil, paramètres, jeu)
    et orchestre le cycle de vie de l'application.
    """

    def __init__(self, racine):
        """
        Initialise le contrôleur de l'application.

        Args:
            racine (tk.Tk): Fenêtre principale Tkinter
        """
        self.CTA_racine = racine
        self.CTA_controleur_jeu = None
        self.afficher_accueil()

    def afficher_accueil(self):
        """
        Affiche le menu d'accueil avec les options de mode de jeu.

        Propose le mode 1v1 et les trois niveaux de difficulté contre l'IA.
        """
        vue_accueil = VueAccueil(self.CTA_racine)
        vue_accueil.creer_interface(
            rappel_1v1=lambda: self.afficher_parametres(None, None),
            rappel_facile=lambda: self.afficher_parametres("jaune", 1),
            rappel_moyen=lambda: self.afficher_parametres("jaune", 3),
            rappel_difficile=lambda: self.afficher_parametres("jaune", 5)
        )

    def afficher_parametres(self, mode_ia, difficulte):
        """
        Affiche la page des paramètres de jeu.

        Permet de configurer la taille de la grille, le nombre de pions à aligner,
        qui commence, et la couleur du joueur (en mode IA).

        Args:
            mode_ia (str or None): "rouge", "jaune" ou None selon le mode choisi
            difficulte (int or None): 1, 3 ou 5 selon la difficulté choisie
        """
        vue_parametres = VueParametres(self.CTA_racine, mode_ia, difficulte)
        vue_parametres.creer_interface(
            rappel_jouer=lambda var_lignes, var_colonnes, var_alignes, var_premier, var_couleur: self.lancer_jeu(
                mode_ia, difficulte, var_lignes, var_colonnes, var_alignes, var_premier, var_couleur
            ),
            rappel_retour=self.afficher_accueil
        )

    def lancer_jeu(self, mode_ia, difficulte, var_lignes, var_colonnes, var_alignes, var_premier, var_couleur_joueur):
        """
        Lance une nouvelle partie avec les paramètres configurés.

        Nettoie la fenêtre, crée le contrôleur de jeu avec les bons paramètres,
        détermine qui commence, et crée l'interface des actions.

        Args:
            mode_ia (str or None): Mode de jeu sélectionné
            difficulte (int or None): Niveau de difficulté de l'IA
            var_lignes (tk.StringVar): Variable contenant le nombre de lignes
            var_colonnes (tk.StringVar): Variable contenant le nombre de colonnes
            var_alignes (tk.StringVar): Variable contenant le nombre de pions à aligner
            var_premier (tk.StringVar): Variable indiquant qui commence
            var_couleur_joueur (tk.StringVar): Variable contenant la couleur du joueur
        """
        # Nettoyer la fenêtre
        for widget in self.CTA_racine.winfo_children():
            widget.destroy()

        lignes = int(var_lignes.get())
        colonnes = int(var_colonnes.get())
        nombre_alignes = int(var_alignes.get())

        # Déterminer qui commence et les couleurs
        if mode_ia is None:
            # Mode 1v1
            premier = var_premier.get()
            mode_ia_final = None
            couleur_joueur = None
        else:
            # Mode contre IA
            couleur_joueur = var_couleur_joueur.get()
            premier = var_premier.get()

            # Déterminer le mode_ia en fonction de la couleur du joueur
            if couleur_joueur == "Rouge":
                mode_ia_final = "jaune"
            else:
                mode_ia_final = "rouge"

        # Créer le jeu
        self.CTA_controleur_jeu = ControleurJeu(
            self.CTA_racine, lignes=lignes, colonnes=colonnes, nombre_alignes=nombre_alignes,
            mode_ia=mode_ia_final if mode_ia else None, difficulte=difficulte
        )

        # Déterminer qui commence
        if mode_ia is None:
            # Mode 1v1
            if premier == "Jaune":
                self.CTA_controleur_jeu.CTJ_joueur_actuel = -1
            else:
                self.CTA_controleur_jeu.CTJ_joueur_actuel = 1
        else:
            # Mode contre IA
            if premier == "IA":
                # L'IA commence
                if mode_ia_final == "rouge":
                    self.CTA_controleur_jeu.CTJ_joueur_actuel = 1
                else:
                    self.CTA_controleur_jeu.CTJ_joueur_actuel = -1
                # Faire jouer l'IA après un délai
                self.CTA_racine.after(500, self.CTA_controleur_jeu.tour_ia)
            else:
                # Le joueur commence
                if couleur_joueur == "Rouge":
                    self.CTA_controleur_jeu.CTJ_joueur_actuel = 1
                else:
                    self.CTA_controleur_jeu.CTJ_joueur_actuel = -1

        print("ici le jeu est lancé")

        # Créer les actions
        vue_actions = VueActions(self.CTA_racine)
        vue_actions.creer_interface(
            rappel_annuler=self.CTA_controleur_jeu.annuler,
            rappel_refaire=self.CTA_controleur_jeu.refaire,
            rappel_rejouer=lambda: self.lancer_jeu(
                mode_ia, difficulte, var_lignes, var_colonnes, var_alignes, var_premier, var_couleur_joueur
            ),
            rappel_accueil=self.afficher_accueil
        )