import tkinter as tk
from vue import VueGrille, VueAccueil, VueParametres, VueActions
from model import Creer_matrice, Reinitialiser_historique, Sauvegarder_etat, Verifier_victoire, Afficher_matrice, Ajouter_pion, Undo_redo, Meilleur_coup_ia


class ControleurJeu:
    """
    Contrôleur principal du jeu Puissance 4.

    Gère la logique du jeu, les interactions utilisateur, l'animation des pions,
    la détection de fin de partie et l'intégration avec l'IA.
    """

    def __init__(self, CTJracine, iLignes=6, iColonnes=7, iNombre_alignes=4, cMode_ia=None, iDifficulte=None):
        """
        Initialise le contrôleur de jeu.

        Args:
            CTJracine (tk.Tk): Fenêtre principale Tkinter
            iLignes (int): Nombre de lignes de la grille (défaut: 6)
            iColonnes (int): Nombre de colonnes de la grille (défaut: 7)
            iNombre_alignes (int): Nombre de pions à aligner pour gagner (défaut: 4)
            cMode_ia (str or None): "rouge" si l'IA joue rouge, "jaune" si jaune, None en mode 1v1
            iDifficulte (int or None): Profondeur de recherche de l'IA (1=facile, 3=moyen, 5=difficile)
        """
        self.CTJ_racine = CTJracine
        self.iCTJ_lignes = iLignes
        self.iCTJ_colonnes = iColonnes
        self.iCTJ_nombre_alignes = iNombre_alignes
        self.cCTJ_mode_ia = cMode_ia
        self.iCTJ_difficulte = iDifficulte

        # Calcul dynamique de la taille des cellules pour écrans 1920x1080
        # Calculer la taille en fonction de la dimension la plus contraignante
        fTaille_max_lignes = 690 / iLignes  # Hauteur max disponible (6 lignes * 115 = 690)
        fTaille_max_colonnes = 805 / iColonnes  # Largeur max disponible (7 colonnes * 115 = 805)

        # Prendre la plus petite des deux pour que tout rentre
        self.iTCJ_taille_cellule = int(min(fTaille_max_lignes, fTaille_max_colonnes, 90))  

        self.bCTJ_animation_en_cours = False
        self.bCTJ_partie_terminee = False

        # Création de la matrice de jeu
        self.lCTJ_matrice = Creer_matrice(iLignes, iColonnes)
        Reinitialiser_historique(self.lCTJ_matrice)
        self.iCTJ_joueur_actuel = 1  # 1 pour rouge, -1 pour jaune

        # Création de la vue
        self.CTJ_vue = VueGrille(CTJracine, iLignes, iColonnes, self.iTCJ_taille_cellule)

        # Binding des événements souris
        self.CTJ_vue.VGR_canvas.bind("<Motion>", self.CTJ_sur_mouvement_souris)
        self.CTJ_vue.VGR_canvas.bind("<Button-1>", self.CTJ_sur_clic)
        self.CTJ_vue.VGR_canvas.bind("<Leave>", self.CTJ_sur_sortie_souris)

    def CTJ_sur_mouvement_souris(self, cEvenement):
        """
        Gère le mouvement de la souris pour afficher l'effet de survol.

        Affiche un effet d'ombre sur la colonne survolée, sauf si une animation
        est en cours, la partie est terminée, ou si c'est le tour de l'IA.

        Args:
            cEvenement (tk.Event): Événement de mouvement de souris
        """
        if self.bCTJ_animation_en_cours or self.bCTJ_partie_terminee:
            return

        # Bloquer le survol si c'est le tour de l'IA
        if self.cCTJ_mode_ia and self.CTJ_est_tour_ia():
            return
        # Calculer le numero de la colonne 
        iColonne = cEvenement.x // self.iTCJ_taille_cellule
        # Verifier si la colonne est valide (càd dans la grille) 
        if 0 <= iColonne < self.iCTJ_colonnes:
            if iColonne != self.CTJ_vue.VGR_colonne_survol:
                self.CTJ_vue.VGR_afficher_effet_survol(iColonne)
        else:
            self.CTJ_vue.VGR_effacer_effet_survol()

    def CTJ_sur_sortie_souris(self, cEvenement):
        """
        Efface l'effet de survol quand la souris quitte le canvas.

        Args:
            cEvenement (tk.Event): Événement de sortie de souris
        """
        self.CTJ_vue.VGR_effacer_effet_survol()

    def CTJ_sur_clic(self, cEvenement):
        """
        Gère le clic de souris pour ajouter un pion.

        Ignore les clics si une animation est en cours, la partie est terminée,
        ou si c'est le tour de l'IA.

        Args:
            cEvenement (tk.Event): Événement de clic de souris
        """
        if self.bCTJ_animation_en_cours or self.bCTJ_partie_terminee:
            return

        # Bloquer les clics si c'est le tour de l'IA
        if self.cCTJ_mode_ia and self.CTJ_est_tour_ia():
            return
        # Calculer le numero de la colonne
        iColonne = cEvenement.x // self.iTCJ_taille_cellule
        # Verifier si la colonne est valide (càd dans la grille) 
        if 0 <= iColonne < self.iCTJ_colonnes:
            self.CTJ_jouer_coup(iColonne)

    def CTJ_est_tour_ia(self):
        """
        Vérifie si c'est le tour de l'IA de jouer.

        Returns:
            bool: True si c'est le tour de l'IA, False sinon
        """
        if self.cCTJ_mode_ia == "rouge" and self.iCTJ_joueur_actuel == 1:
            return True
        if self.cCTJ_mode_ia == "jaune" and self.iCTJ_joueur_actuel == -1:
            return True
        return False

    def CTJ_tour_ia(self):
        """
        Fait jouer l'IA en calculant et en jouant le meilleur coup.

        Utilise l'algorithme Minimax avec la profondeur correspondant
        au niveau de difficulté choisie.
        """
        # Si la partie est fini ne rien faire
        if self.bCTJ_partie_terminee:
            return

        iJoueur_ia = 1 if self.cCTJ_mode_ia == "rouge" else -1
        iColonne = Meilleur_coup_ia(self.lCTJ_matrice, iJoueur_ia, self.iCTJ_difficulte, self.iCTJ_nombre_alignes)

        if iColonne is not None:
            self.CTJ_jouer_coup(iColonne)

    def CTJ_jouer_coup(self, iColonne):
        """
        Tente de jouer un coup dans la colonne spécifiée.

        Trouve la ligne de destination (la plus basse disponible), ajoute le pion
        à la matrice, sauvegarde l'état et lance l'animation.

        Args:
            iColonne (int): L'indice de la colonne où jouer
        """
        iLigne_destination = None
        # Parcours les lignes de bas en haut pour trouver la premiere case vide
        for iLigne in range(self.iCTJ_lignes - 1, -1, -1):
            #v Verifie si la case est vide 
            if self.lCTJ_matrice[iLigne][iColonne] == 0:
                iLigne_destination = iLigne
                break

        if iLigne_destination is None:
            print("Colonne pleine !")
            return

        iResultat = Ajouter_pion(self.lCTJ_matrice, self.iCTJ_joueur_actuel, iColonne)
        Sauvegarder_etat(self.lCTJ_matrice)

        if iResultat == 0:
            self.CTJ_animer_chute_pion(iColonne, iLigne_destination, self.iCTJ_joueur_actuel)

    def CTJ_animer_chute_pion(self, iColonne, iLigne_finale, iJoueur):
        """
        Lance l'animation de chute du pion.

        Bloque les interactions pendant l'animation et vérifie la fin de partie
        une fois l'animation terminée.

        Args:
            iColonne (int): L'indice de la colonne
            iLigne_finale (int): L'indice de la ligne finale du pion
            iJoueur (int): 1 ou -1 selon le joueur
        """
        self.bCTJ_animation_en_cours = True
        self.CTJ_vue.VGR_effacer_effet_survol()

        def cFin_animation():
            """Fonction appelée à la fin de l'animation."""
            self.bCTJ_animation_en_cours = False
            self.CTJ_verifier_fin_partie()

        self.CTJ_vue.VGR_animer_chute_pion(iColonne, iLigne_finale, iJoueur, cFin_animation)

    def CTJ_verifier_fin_partie(self):
        """
        Vérifie si la partie est terminée (victoire ou match nul).

        Affiche le message approprié si la partie est terminée, sinon
        change de joueur et fait jouer l'IA si c'est son tour.
        """
        iResultat = Verifier_victoire(self.lCTJ_matrice, self.iCTJ_nombre_alignes)

        if iResultat == 1:
            self.bCTJ_partie_terminee = True
            self.CTJ_vue.VGR_effacer_effet_survol()
            self.CTJ_vue.VGR_afficher_message("Victoire du ROUGE!")
            print("\n" + "=" * 50)
            Afficher_matrice(self.lCTJ_matrice)
            print("Victoire du joueur ROUGE ! ")
            print("=" * 50)
        elif iResultat == -1:
            self.bCTJ_partie_terminee = True
            self.CTJ_vue.VGR_effacer_effet_survol()
            self.CTJ_vue.VGR_afficher_message("Victoire du JAUNE !")
            print("\n" + "=" * 50)
            Afficher_matrice(self.lCTJ_matrice)
            print(" Victoire du joueur JAUNE !")
            print("=" * 50)
        elif self.CTJ_grille_pleine():
            self.bCTJ_partie_terminee = True
            self.CTJ_vue.VGR_effacer_effet_survol()
            self.CTJ_vue.VGR_afficher_message("Match nul !")
            print("\n" + "=" * 50)
            Afficher_matrice(self.lCTJ_matrice)
            print("Match nul !")
            print("=" * 50)
        else:
            self.iCTJ_joueur_actuel *= -1

            # Si c'est le tour de l'IA, la faire jouer après un court délai
            if self.cCTJ_mode_ia and self.CTJ_est_tour_ia():
                self.CTJ_racine.after(500, self.CTJ_tour_ia)

    def CTJ_grille_pleine(self):
        """
        Vérifie si la grille est complètement pleine.

        Returns:
            bool: True si toutes les colonnes sont pleines, False sinon
        """
        # Parcours les colonnes pour savoir si c'est plein
        for iColonne in range(self.iCTJ_colonnes):
            if self.lCTJ_matrice[0][iColonne] == 0:
                return False
        return True

    def CTJ_annuler(self):
        """
        Annule le dernier coup (ou les deux derniers en mode IA).

        En mode 1v1, annule un coup et change de joueur.
        En mode IA, annule deux coups (joueur + IA) pour que le joueur rejoue.
        """
        if Undo_redo(self.lCTJ_matrice, "u", self.cCTJ_mode_ia) == 0:
            # En mode IA on recule de 2 coups → le joueur rejoue
            if self.cCTJ_mode_ia is not None:
                pass
            else:
                # En 1v1 on change de joueur
                self.iCTJ_joueur_actuel *= -1

            self.bCTJ_partie_terminee = False
            self.CTJ_vue.VGR_rafraichir_grille(self.lCTJ_matrice)

    def CTJ_refaire(self):
        """
        Rétablit le coup précédemment annulé.

        En mode 1v1, refait un coup et change de joueur.
        En mode IA, refait deux coups (joueur + IA) pour que ca marche.
        """
        if Undo_redo(self.lCTJ_matrice, "r", self.cCTJ_mode_ia) == 0:
            # En mode IA on rejoue un tour complet → le joueur reste le même
            if self.cCTJ_mode_ia is not None:
                pass
            else:
                self.iCTJ_joueur_actuel *= -1

            self.CTJ_vue.VGR_rafraichir_grille(self.lCTJ_matrice)


class ControleurApplication:
    """
    Contrôleur principal de l'application.

    Gère la navigation entre les différentes vues (accueil, paramètres, jeu)
    et orchestre le cycle de vie de l'application.
    """

    def __init__(self, CTAracine):
        """
        Initialise le contrôleur de l'application.

        Args:
            CTAracine (tk.Tk): Fenêtre principale Tkinter
        """
        self.CTA_racine = CTAracine
        self.CTA_controleur_jeu = None
        self.CTA_afficher_accueil()

    def CTA_afficher_accueil(self):
        """
        Affiche le menu d'accueil avec les options de mode de jeu.

        Propose le mode 1v1 et les trois niveaux de difficulté contre l'IA.
        """
        cVue_accueil = VueAccueil(self.CTA_racine)
        # Construit l'affichage d'accueil avec les boutons et les fonction
        cVue_accueil.VAC_creer_interface(
            cRappel_1v1=lambda: self.CTA_afficher_parametres(None, None),
            cRappel_facile=lambda: self.CTA_afficher_parametres("jaune", 1),
            cRappel_moyen=lambda: self.CTA_afficher_parametres("jaune", 3),
            cRappel_difficile=lambda: self.CTA_afficher_parametres("jaune", 5)
        )

    def CTA_afficher_parametres(self, cMode_ia, iDifficulte):
        """
        Affiche la page des paramètres de jeu.

        Permet de configurer la taille de la grille, le nombre de pions à aligner,
        qui commence, et la couleur du joueur (en mode IA).

        Args:
            cMode_ia (str or None): "rouge", "jaune" ou None selon le mode choisi
            iDifficulte (int or None): 1, 3 ou 5 selon la difficulté choisi
        """
        cVue_parametres = VueParametres(self.CTA_racine, cMode_ia, iDifficulte)
        # Construit l'affichage des parametres avec les boutons et les fonction
        cVue_parametres.VPA_creer_interface(
            cRappel_jouer=lambda cVar_lignes, cVar_colonnes, cVar_alignes, cVar_premier, cVar_couleur: self.CTA_lancer_jeu(
                cMode_ia, iDifficulte, cVar_lignes, cVar_colonnes, cVar_alignes, cVar_premier, cVar_couleur
            ),
            cRappel_retour=self.CTA_afficher_accueil
        )

    def CTA_lancer_jeu(self, cMode_ia, iDifficulte, cVar_lignes, cVar_colonnes, cVar_alignes, cVar_premier, cVar_couleur_joueur):
        """
        Lance une nouvelle partie avec les paramètres configurés.

        Nettoie la fenêtre, crée le contrôleur de jeu avec les bons paramètres,
        détermine qui commence, et crée l'interface des actions.

        Args:
            cMode_ia (str or None): Mode de jeu sélectionné
            iDifficulte (int or None): Niveau de difficulté de l'IA
            cVar_lignes (tk.StringVar): Variable contenant le nombre de lignes
            cVar_colonnes (tk.StringVar): Variable contenant le nombre de colonnes
            cVar_alignes (tk.StringVar): Variable contenant le nombre de pions à aligner
            cVar_premier (tk.StringVar): Variable indiquant qui commence
            cVar_couleur_joueur (tk.StringVar): Variable contenant la couleur du joueur
        """
        # Nettoyer la fenêtre
        for cWidget in self.CTA_racine.winfo_children():
            cWidget.destroy()
        # Recupere la valeur des lignes, colonnes et nb aligne et les convertit en int
        iLignes = int(cVar_lignes.get())
        iColonnes = int(cVar_colonnes.get())
        iNombre_alignes = int(cVar_alignes.get())

        # Déterminer qui commence et les couleurs
        if cMode_ia is None:
            # Mode 1v1
            cPremier = cVar_premier.get()
            cMode_ia_final = None
            cCouleur_joueur = None
        else:
            # Mode contre IA
            cCouleur_joueur = cVar_couleur_joueur.get()
            cPremier = cVar_premier.get()

            # Déterminer le mode_ia en fonction de la couleur du joueur
            if cCouleur_joueur == "Rouge":
                cMode_ia_final = "jaune"
            else:
                cMode_ia_final = "rouge"

        # Créer le jeu
        self.CTA_controleur_jeu = ControleurJeu(
            self.CTA_racine, iLignes=iLignes, iColonnes=iColonnes, iNombre_alignes=iNombre_alignes,
            cMode_ia=cMode_ia_final if cMode_ia else None, iDifficulte=iDifficulte
        )

        # Déterminer qui commence
        if cMode_ia is None:
            # Mode 1v1
            if cPremier == "Jaune":
                self.CTA_controleur_jeu.iCTJ_joueur_actuel = -1
            else:
                self.CTA_controleur_jeu.iCTJ_joueur_actuel = 1
        else:
            # Mode contre IA
            if cPremier == "IA":
                # L'IA commence
                if cMode_ia_final == "rouge":
                    self.CTA_controleur_jeu.iCTJ_joueur_actuel = 1
                else:
                    self.CTA_controleur_jeu.iCTJ_joueur_actuel = -1
                # Faire jouer l'IA après un délai
                self.CTA_racine.after(500, self.CTA_controleur_jeu.CTJ_tour_ia)
            else:
                # Le joueur commence
                if cCouleur_joueur == "Rouge":
                    self.CTA_controleur_jeu.iCTJ_joueur_actuel = 1
                else:
                    self.CTA_controleur_jeu.iCTJ_joueur_actuel = -1

        print("ici le jeu est lancé")

        # Créer les actions
        cVue_actions = VueActions(self.CTA_racine)
        cVue_actions.VAT_creer_interface(
            cRappel_annuler=self.CTA_controleur_jeu.CTJ_annuler,
            cRappel_refaire=self.CTA_controleur_jeu.CTJ_refaire,
            cRappel_rejouer=lambda: self.CTA_lancer_jeu(
                cMode_ia, iDifficulte, cVar_lignes, cVar_colonnes, cVar_alignes, cVar_premier, cVar_couleur_joueur
            ),
            cRappel_accueil=self.CTA_afficher_accueil
        )