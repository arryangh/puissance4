import tkinter as tk
from vue import VueGrille, VueHome, VueParametres, VueActions
from model import *


class ControleurJeu:
    """Contrôleur principal du jeu Puissance 4"""

    def __init__(self, root, rows=6, cols=7, nb_aligned=4, mode_ia=None, difficulte=None):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.nb_aligned = nb_aligned
        self.mode_ia = mode_ia
        self.difficulte = difficulte

        # Calcul dynamique de la taille des cellules pour écrans 1920x1080
        # Calculer la taille en fonction de la dimension la plus contraignante
        max_rows_size = 690 / rows  # Hauteur max disponible (6 lignes * 115 = 690)
        max_cols_size = 805 / cols  # Largeur max disponible (7 colonnes * 115 = 805)

        # Prendre la plus petite des deux pour que tout rentre
        self.cell_size = int(min(max_rows_size, max_cols_size, 115))  # Max 115px

        self.animation_en_cours = False
        self.partie_terminee = False

        # Création de la matrice de jeu
        self.matrice = createMatrice(rows, cols)
        reset_historique(self.matrice)
        self.joueur_actuel = 1  # 1 pour rouge, -1 pour jaune

        # Création de la vue
        self.vue = VueGrille(root, rows, cols, self.cell_size)

        # Binding des événements souris
        self.vue.canvas.bind("<Motion>", self.sur_mouvement_souris)
        self.vue.canvas.bind("<Button-1>", self.sur_clic)
        self.vue.canvas.bind("<Leave>", self.sur_sortie_souris)

    def sur_mouvement_souris(self, event):
        """Gère le survol de la souris pour afficher l'effet d'ombre"""
        if self.animation_en_cours or self.partie_terminee:
            return

        # Bloquer le survol si c'est le tour de l'IA
        if self.mode_ia and self.est_tour_ia():
            return

        col = event.x // self.cell_size

        if 0 <= col < self.cols:
            if col != self.vue.colonne_survol:
                self.vue.afficher_effet_survol(col)
        else:
            self.vue.effacer_effet_survol()

    def sur_sortie_souris(self, event):
        """Efface l'effet de survol quand la souris quitte le canvas"""
        self.vue.effacer_effet_survol()

    def sur_clic(self, event):
        """Gère le clic pour ajouter un pion"""
        if self.animation_en_cours or self.partie_terminee:
            return

        # Bloquer les clics si c'est le tour de l'IA
        if self.mode_ia and self.est_tour_ia():
            return

        col = event.x // self.cell_size

        if 0 <= col < self.cols:
            self.jouer_coup(col)

    def est_tour_ia(self):
        """Vérifie si c'est le tour de l'IA"""
        if self.mode_ia == "rouge" and self.joueur_actuel == 1:
            return True
        if self.mode_ia == "jaune" and self.joueur_actuel == -1:
            return True
        return False

    def tour_ia(self):
        """Fait jouer l'IA"""
        if self.partie_terminee:
            return

        joueur_ia = 1 if self.mode_ia == "rouge" else -1
        col = meilleur_coup_ia(self.matrice, joueur_ia, self.difficulte, self.nb_aligned)

        if col is not None:
            self.jouer_coup(col)

    def jouer_coup(self, col):
        """Tente de jouer un coup dans la colonne donnée"""
        row_destination = None
        for row in range(self.rows - 1, -1, -1):
            if self.matrice[row][col] == 0:
                row_destination = row
                break

        if row_destination is None:
            print("Colonne pleine !")
            return

        resultat = ajouter_pion(self.matrice, self.joueur_actuel, col)
        sauvegarder_etat(self.matrice)

        if resultat == 0:
            self.animer_chute_pion(col, row_destination, self.joueur_actuel)

    def animer_chute_pion(self, col, row_final, joueur):
        """Anime la chute du pion"""
        self.animation_en_cours = True
        self.vue.effacer_effet_survol()

        def fin_animation():
            self.animation_en_cours = False
            self.verifier_fin_partie()

        self.vue.animer_chute_pion(col, row_final, joueur, fin_animation)

    def verifier_fin_partie(self):
        """Vérifie si la partie est terminée"""
        resultat = verifier_victoire(self.matrice, self.nb_aligned)

        if resultat == 1:
            self.partie_terminee = True
            self.vue.effacer_effet_survol()
            self.vue.afficher_message("🎉 Victoire du joueur ROUGE ! 🎉")
            print("\n" + "=" * 50)
            afficherMatrice(self.matrice)
            print("🎉 Victoire du joueur ROUGE ! 🎉")
            print("=" * 50)
        elif resultat == -1:
            self.partie_terminee = True
            self.vue.effacer_effet_survol()
            self.vue.afficher_message("🎉 Victoire du joueur JAUNE ! 🎉")
            print("\n" + "=" * 50)
            afficherMatrice(self.matrice)
            print("🎉 Victoire du joueur JAUNE ! 🎉")
            print("=" * 50)
        elif self.grille_pleine():
            self.partie_terminee = True
            self.vue.effacer_effet_survol()
            self.vue.afficher_message("Match nul !")
            print("\n" + "=" * 50)
            afficherMatrice(self.matrice)
            print("Match nul !")
            print("=" * 50)
        else:
            self.joueur_actuel *= -1

            # Si c'est le tour de l'IA, la faire jouer après un court délai
            if self.mode_ia and self.est_tour_ia():
                self.root.after(500, self.tour_ia)

    def grille_pleine(self):
        """Vérifie si la grille est pleine"""
        for col in range(self.cols):
            if self.matrice[0][col] == 0:
                return False
        return True

    def undo(self):
        """Annule le dernier coup"""
        if undo_redo(self.matrice, "u", self.mode_ia) == 0:
            # En mode IA on recule de 2 coups → le joueur rejoue
            if self.mode_ia is not None:
                pass
            else:
                # En 1v1 on change de joueur
                self.joueur_actuel *= -1

            self.partie_terminee = False
            self.vue.rafraichir_grille(self.matrice)

    def redo(self):
        """Rétablit le coup annulé"""
        if undo_redo(self.matrice, "r", self.mode_ia) == 0:
            # En mode IA on rejoue un tour complet → le joueur reste le même
            if self.mode_ia is not None:
                pass
            else:
                self.joueur_actuel *= -1

            self.vue.rafraichir_grille(self.matrice)


class ControleurApplication:
    """Contrôleur principal de l'application"""

    def __init__(self, root):
        self.root = root
        self.controleur_jeu = None
        self.afficher_home()

    def afficher_home(self):
        """Affiche le menu d'accueil"""
        vue_home = VueHome(self.root)
        vue_home.creer_interface(
            callback_1v1=lambda: self.afficher_parametres(None, None),
            callback_facile=lambda: self.afficher_parametres("jaune", 1),
            callback_moyen=lambda: self.afficher_parametres("jaune", 3),
            callback_difficile=lambda: self.afficher_parametres("jaune", 5)
        )

    def afficher_parametres(self, mode_ia, difficulte):
        """Affiche la page des paramètres"""
        vue_params = VueParametres(self.root, mode_ia, difficulte)
        vue_params.creer_interface(
            callback_jouer=lambda var_rows, var_cols, var_aligned, var_premier, var_couleur: self.lancer_jeu(
                mode_ia, difficulte, var_rows, var_cols, var_aligned, var_premier, var_couleur
            ),
            callback_retour=self.afficher_home
        )

    def lancer_jeu(self, mode_ia, difficulte, var_rows, var_cols, var_aligned, var_premier, var_couleur_joueur):
        """Lance une nouvelle partie"""
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()

        rows = int(var_rows.get())
        cols = int(var_cols.get())
        nb_aligned = int(var_aligned.get())

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
        self.controleur_jeu = ControleurJeu(
            self.root, rows=rows, cols=cols, nb_aligned=nb_aligned,
            mode_ia=mode_ia_final if mode_ia else None, difficulte=difficulte
        )

        # Déterminer qui commence
        if mode_ia is None:
            # Mode 1v1
            if premier == "Jaune":
                self.controleur_jeu.joueur_actuel = -1
            else:
                self.controleur_jeu.joueur_actuel = 1
        else:
            # Mode contre IA
            if premier == "IA":
                # L'IA commence
                if mode_ia_final == "rouge":
                    self.controleur_jeu.joueur_actuel = 1
                else:
                    self.controleur_jeu.joueur_actuel = -1
                # Faire jouer l'IA après un délai
                self.root.after(500, self.controleur_jeu.tour_ia)
            else:
                # Le joueur commence
                if couleur_joueur == "Rouge":
                    self.controleur_jeu.joueur_actuel = 1
                else:
                    self.controleur_jeu.joueur_actuel = -1

        print("ici le jeu est lancé")

        # Créer les actions
        vue_actions = VueActions(self.root)
        vue_actions.creer_interface(
            callback_undo=self.controleur_jeu.undo,
            callback_redo=self.controleur_jeu.redo,
            callback_rejouer=lambda: self.lancer_jeu(
                mode_ia, difficulte, var_rows, var_cols, var_aligned, var_premier, var_couleur_joueur
            ),
            callback_home=self.afficher_home
        )