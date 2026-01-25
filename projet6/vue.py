import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class VueGrille:
    """
    Vue (=Interface graphique) pour afficher et gérer l'interface graphique de la grille de jeu puissance 4.

    Gère l'affichage de la grille, l'animation des pions qui tombent dans la grille, les effets de survol
    et les messages de victoire de fin de partie.
    """

    def __init__(self, VGRracine, iLignes, iColonnes, iTaille_cellule):
        """
        Initialise la vue de la grille de jeu (en fonction des dimensions de la grille)

        Args:
            VGRracine (tk.Tk): Fenêtre principale Tkinter
            iLignes (int): Nombre de lignes de la grille
            iColonnes (int): Nombre de colonnes de la grille
            iTaille_cellule (int): Taille en pixels d'une cellule
        """
        self.VGR_racine = VGRracine
        self.iVGR_lignes = iLignes
        self.iVGR_colonnes = iColonnes
        self.iTCJ_taille_cellule = iTaille_cellule

        self.VGR_colonne_survol = None
        self.lVGR_pions_affiches = {}

        # Couleurs des joueurs
        self.dVGR_couleurs = {
            1: "#FF4444",  # Rouge pour joueur 1
            -1: "#FFD700"  # Jaune pour joueur -1
        }

        # Chargement et redimensionnement des images 
        self.VGR_img_normale = Image.open("../affichage/exportAuto/normalCELL.png")
        self.VGR_img_bas = Image.open("../affichage/exportAuto/bottomCELL.png")

        self.VGR_img_normale = self.VGR_img_normale.resize((self.iTCJ_taille_cellule, self.iTCJ_taille_cellule), Image.LANCZOS)
        self.VGR_img_bas = self.VGR_img_bas.resize((self.iTCJ_taille_cellule, self.iTCJ_taille_cellule), Image.LANCZOS)
        # Conversion des images en image tkinter compatible
        self.VGR_tk_img_normale = ImageTk.PhotoImage(self.VGR_img_normale)
        self.VGR_tk_img_bas = ImageTk.PhotoImage(self.VGR_img_bas)

        # Configuration de la fenêtre
        iLargeur_fenetre = self.iVGR_colonnes * self.iTCJ_taille_cellule + 340
        iHauteur_fenetre = self.iVGR_lignes * self.iTCJ_taille_cellule + 40
        self.VGR_racine.geometry(f"{iLargeur_fenetre}x{iHauteur_fenetre}")
        self.VGR_racine.title("Puissance 4")

        # Canvas pour afficher la grille
        self.VGR_canvas = tk.Canvas(
            VGRracine,
            width=self.iVGR_colonnes * self.iTCJ_taille_cellule,
            height=self.iVGR_lignes * self.iTCJ_taille_cellule,
            bg="white",
            highlightthickness=0
        )
        self.VGR_canvas.pack(side=tk.LEFT, padx=20, pady=20)

        self.VGR_afficher_grille()

    def VGR_afficher_grille(self):
        """
        Affiche toutes les cellules de la grille avec les images appropriés.

        Utilise une image différente pour la ligne du bas (bottomCELL) (avec le trait noir en bas du carré)
        et une image normale pour les autres lignes. (sans le trait noi en bas du carré)
        """
        self.VGR_canvas.delete("grille")

        for iLigne in range(self.iVGR_lignes):
            for iColonne in range(self.iVGR_colonnes):
                iX = iColonne * self.iTCJ_taille_cellule
                iY = iLigne * self.iTCJ_taille_cellule

                if iLigne == self.iVGR_lignes - 1:
                    self.VGR_canvas.create_image(iX, iY, image=self.VGR_tk_img_bas, anchor="nw", tags="grille")
                else:
                    self.VGR_canvas.create_image(iX, iY, image=self.VGR_tk_img_normale, anchor="nw", tags="grille")

        self.VGR_canvas.tag_raise("grille")

    def VGR_afficher_effet_survol(self, iColonne):
        """
        Affiche un effet d'ombre grise (hachuré) sur la colonne survolée par la souris.

        Args:
            iColonne (int): L'indice de la colonne à surligner
        """
        self.VGR_canvas.delete("survol")
        self.VGR_colonne_survol = iColonne

        for iLigne in range(self.iVGR_lignes):
            iX = iColonne * self.iTCJ_taille_cellule
            iY = iLigne * self.iTCJ_taille_cellule

            self.VGR_canvas.create_rectangle(
                iX, iY, iX + self.iTCJ_taille_cellule, iY + self.iTCJ_taille_cellule,
                fill="gray", stipple="gray50", tags="survol"
            )

    def VGR_effacer_effet_survol(self):
        """
        Efface l'effet de survol de la grille.
        """
        self.VGR_canvas.delete("survol")
        self.VGR_colonne_survol = None

    def VGR_animer_chute_pion(self, colonne, ligne_finale, joueur, rappel):
        """
        Anime la chute d'un pion avec effet de gravité et rebond.

        Le pion commence au-dessus de la grille, tombe avec une accélération
        gravitationnelle et rebondit légèrement avant de se stabiliser.

        Args:
            colonne (int): L'indice de la colonne où le pion tombe
            ligne_finale (int): L'indice de la ligne finale du pion
            joueur (int): 1 ou -1 selon le joueur
            rappel (callable): Fonction à appeler quand l'animation est terminée
        """
        # Recupere la couleur du pion
        couleur = self.dVGR_couleurs[joueur]
        x_centre = colonne * self.iTCJ_taille_cellule + self.iTCJ_taille_cellule // 2
        y_finale = ligne_finale * self.iTCJ_taille_cellule + self.iTCJ_taille_cellule // 2

        y = -self.iTCJ_taille_cellule // 2
        VELOCITE = 0
        GRAVITE = 3
        AMORTISSEMENT = 0.2
        rayon = self.iTCJ_taille_cellule // 2

        pion = self.VGR_canvas.create_oval(
            x_centre - rayon, y - rayon,
            x_centre + rayon, y + rayon,
            fill=couleur, outline="#8B4513", width=3, tags="pion"
        )

        def animer():
            """
            Sous-fonction récursive qui gère chaque frame de l'animation.

            Appelée toutes les 16ms (~60 FPS) pour mettre à jour la position du pion.
            Simule la physique avec:
            - Accélération gravitationnelle (GRAVITE)
            - Rebond avec perte d'énergie (AMORTISSEMENT)
            - Arrêt quand la vitesse devient négligeable (< 0.5)

            Variables nonlocal modifiées:
                y (int): Position verticale actuelle du pion
                VELOCITE (int): Vitesse de descente actuelle (augmente avec la gravité)
            """
            nonlocal y, VELOCITE

            VELOCITE += GRAVITE
            y += VELOCITE

            if y >= y_finale:
                y = y_finale
                VELOCITE = -VELOCITE * AMORTISSEMENT

                if abs(VELOCITE) < 0.5:
                    self.VGR_canvas.coords(
                        pion,
                        x_centre - rayon, y_finale - rayon,
                        x_centre + rayon, y_finale + rayon
                    )
                    self.lVGR_pions_affiches[(ligne_finale, colonne)] = pion
                    self.VGR_canvas.tag_raise("grille")
                    rappel()
                    return

            self.VGR_canvas.coords(
                pion,
                x_centre - rayon, y - rayon,
                x_centre + rayon, y + rayon
            )

            self.VGR_canvas.tag_raise("grille")
            self.VGR_racine.after(16, animer)

        animer()

    def VGR_afficher_message(self, message):
        """
        Affiche un message au centre de la grille (typiquement pour la fin de partie).

        Args:
            message (str): Le texte du message à afficher
        """
        # Calcule la bonne taille de cadre pour l'image
        iLargeur = self.iVGR_colonnes * self.iTCJ_taille_cellule
        iHauteur = self.iVGR_lignes * self.iTCJ_taille_cellule

        self.VGR_canvas.create_rectangle(
            iLargeur // 4, iHauteur // 2 - 40,
            3 * iLargeur // 4, iHauteur // 2 + 40,
            fill="white", outline="black", width=3, tags="message"
        )

        self.VGR_canvas.create_text(
            iLargeur // 2, iHauteur // 2,
            text=message, font=("Arial", 20, "bold"),
            tags="message"
        )

    def VGR_rafraichir_grille(self, matrice):
        """
        Rafraîchit complètement l'affichage de la grille à partir de la matrice.

        Efface tous les pions et messages existants, puis redessine tous les pions
        présents dans la matrice. Utilisé principalement pour les fonctions undo/redo.

        Args:
            matrice (list): La matrice de jeu à afficher
        """
        self.VGR_canvas.delete("pion")
        self.VGR_canvas.delete("message")  # Supprimer le message de victoire
        self.lVGR_pions_affiches.clear()

        for iLigne in range(self.iVGR_lignes):
            for iColonne in range(self.iVGR_colonnes):
                valeur = matrice[iLigne][iColonne]
                if valeur != 0:
                    couleur = self.dVGR_couleurs[valeur]
                    x = iColonne * self.iTCJ_taille_cellule + self.iTCJ_taille_cellule // 2
                    y = iLigne * self.iTCJ_taille_cellule + self.iTCJ_taille_cellule // 2
                    rayon = self.iTCJ_taille_cellule // 2
                    self.VGR_canvas.create_oval(
                        x - rayon, y - rayon,
                        x + rayon, y + rayon,
                        fill=couleur, outline="#8B4513", width=3, tags="pion"
                    )
        self.VGR_canvas.tag_raise("grille")


class VueAccueil:
    """
    Vue pour le menu d'accueil du jeu.

    Permet au joueur de choisir entre le mode 1v1 ou les différents niveaux
    de difficulté contre l'IA.
    """

    def __init__(self, racine):
        """
        Initialise la vue d'accueil.

        Args:
            racine (tk.Tk): Fenêtre principale Tkinter
        """
        self.VAC_racine = racine
        self.VAC_racine.geometry("400x500")
        self.VAC_racine.configure(bg="white")

    def VAC_creer_interface(self, cRappel_1v1, cRappel_facile, cRappel_moyen, cRappel_difficile):
        """
        Crée l'interface du menu d'accueil avec tous les boutons de sélection.

        Args:
            cRappel_1v1 (callable): Fonction appelée lors du clic sur "Mode 1v1"
            cRappel_facile (callable): Fonction appelée lors du clic sur "Facile"
            cRappel_moyen (callable): Fonction appelée lors du clic sur "Moyen"
            cRappel_difficile (callable): Fonction appelée lors du clic sur "Difficile"
        """
        # Nettoyer la fenêtre
        for cWidget in self.VAC_racine.winfo_children():
            cWidget.destroy()

        # Titre
        cTitre = tk.Label(
            self.VAC_racine,
            text="PUISSANCE 4",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#333333"
        )
        cTitre.pack(pady=40)

        # Sous-titre
        cSous_titre = tk.Label(
            self.VAC_racine,
            text="Choisissez votre mode de jeu",
            font=("Arial", 14),
            bg="white",
            fg="#666666"
        )
        cSous_titre.pack(pady=10)

        # Bouton 1v1
        cBouton_1v1 = tk.Button(
            self.VAC_racine,
            text="Mode 1v1",
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_1v1
        )
        cBouton_1v1.pack(pady=15)

        # Séparateur
        cSeparateur = tk.Label(
            self.VAC_racine,
            text="─── Contre l'IA ───",
            font=("Arial", 12),
            bg="white",
            fg="#999999"
        )
        cSeparateur.pack(pady=10)

        # Bouton Facile
        cBouton_facile = tk.Button(
            self.VAC_racine,
            text="Facile ★",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_facile
        )
        cBouton_facile.pack(pady=10)

        # Bouton Moyen
        cBouton_moyen = tk.Button(
            self.VAC_racine,
            text="Moyen ★★",
            font=("Arial", 16, "bold"),
            bg="#FF9800",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_moyen
        )
        cBouton_moyen.pack(pady=10)

        # Bouton Difficile
        cBouton_difficile = tk.Button(
            self.VAC_racine,
            text="Difficile ★★★",
            font=("Arial", 16, "bold"),
            bg="#F44336",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_difficile
        )
        cBouton_difficile.pack(pady=10)


class VueParametres:
    """
    Vue pour la page de configuration des paramètres de jeu.

    Permet de personnaliser la taille de la grille, le nombre de pions à aligner,
    qui commence en premier, et la couleur du joueur (en mode IA).
    """

    def __init__(self, racine, mode_ia, difficulte):
        """
        Initialise la vue des paramètres.

        Args:
            racine (tk.Tk): Fenêtre principale Tkinter
            mode_ia: None si mode 1v1, sinon indique le mode IA
            difficulte (int): Niveau de difficulté de l'IA (1, 3 ou 5)
        """
        self.VPA_racine = racine
        self.VPA_mode_ia = mode_ia
        self.VPA_difficulte = difficulte

    def VPA_creer_interface(self, cRappel_jouer, cRappel_retour):
        """
        Crée l'interface de configuration avec tous les paramètres personnalisables.

        Args:
            cRappel_jouer (callable): Fonction appelée lors du clic sur "JOUER"
            cRappel_retour (callable): Fonction appelée lors du clic sur "Retour au menu"
        """
        # Nettoyer la fenêtre
        for cWidget in self.VPA_racine.winfo_children():
            cWidget.destroy()

        self.VPA_racine.geometry("550x700")
        self.VPA_racine.configure(bg="white")

        # Titre
        cTitre = tk.Label(
            self.VPA_racine,
            text="PARAMÈTRES",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#333333"
        )
        cTitre.pack(pady=30)

        # Affichage du mode sélectionné
        if self.VPA_mode_ia is None:
            cTexte_mode = "Mode 1v1"
            cCouleur_mode = "#000000"
        else:
            cTexte_difficulte = {1: "Facile", 3: "Moyen", 5: "Difficile"}.get(self.VPA_difficulte, "Moyen")
            cTexte_mode = f"Contre l'IA - {cTexte_difficulte}"
            cCouleur_mode = "#000000"

        cEtiquette_mode = tk.Label(
            self.VPA_racine,
            text=f"Mode de jeu : {cTexte_mode}",
            font=("Arial", 16, "bold"),
            bg=cCouleur_mode,
            fg="white",
            padx=20,
            pady=10,
            relief="raised",
            bd=3
        )
        cEtiquette_mode.pack(pady=20)

        # Variables par défaut pour les paramètres
        cVariable_lignes = tk.StringVar(value="6")
        cVariable_colonnes = tk.StringVar(value="7")
        cVariable_alignes = tk.StringVar(value="4")
        cVariable_premier = tk.StringVar(value="Joueur" if self.VPA_mode_ia else "Rouge")
        cVariable_couleur_joueur = tk.StringVar(value="Rouge")

        # Frame pour les paramètres
        cCadre_parametres = tk.Frame(self.VPA_racine, bg="white")
        cCadre_parametres.pack(pady=20)

        # Nombre de lignes
        tk.Label(cCadre_parametres, text="Nombre de lignes :", font=("Arial", 12), bg="white").grid(row=0, column=0,padx=10,pady=10, sticky="w")
        cCombo_lignes = ttk.Combobox(cCadre_parametres , textvariable=cVariable_lignes, values =list(range(4, 11)), width=15,
                                    font=("Arial", 12), state="readonly")
        cCombo_lignes.grid(row=0, column=1, padx=10, pady=10)

        # Nombre de colonnes
        tk.Label(cCadre_parametres, text="Nombre de colonnes :", font=("Arial", 12), bg="white").grid(row=1, column=0,padx=10,pady=10,sticky="w")
        cCombo_colonnes = ttk.Combobox(cCadre_parametres, textvariable=cVariable_colonnes, values = list(range(4, 11)),width=15,font=("Arial", 12), state="readonly")
        cCombo_colonnes.grid(row=1, column=1, padx=10, pady=10)

        # Nombre de pions alignés
        tk.Label(cCadre_parametres, text="Pions à aligner :" , font=("Arial", 12), bg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        cCombo_alignes = ttk.Combobox(cCadre_parametres, textvariable=cVariable_alignes, values =list(range(3, 7)), width=15, font=("Arial", 12), state="readonly")
        cCombo_alignes.grid(row=2, column=1, padx=10, pady=10)

        # Qui commence en premier
        tk.Label(cCadre_parametres, text="Qui commence :", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        if self.VPA_mode_ia is None:
            cCombo_premier = ttk.Combobox(cCadre_parametres, textvariable=cVariable_premier, values=["Rouge", "Jaune"],width=15, font=("Arial", 12), state="readonly")
        else:
            cCombo_premier = ttk.Combobox(cCadre_parametres , textvariable=cVariable_premier, values=["Joueur", "IA"],width=15,font=("Arial", 12), state="readonly")

        cCombo_premier.grid(row=3, column=1, padx=10, pady=10)

        # Couleur du joueur (seulement en mode IA)
        if self.VPA_mode_ia is not None:
            tk.Label(cCadre_parametres, text="Couleur joueur :", font=("Arial", 12), bg="white").grid(row=4, column=0,padx=10,pady=10,sticky="w")
            cCombo_couleur = ttk.Combobox(cCadre_parametres , textvariable=cVariable_couleur_joueur,values=["Rouge", "Jaune"], width=15,font=("Arial", 12), state="readonly")
            cCombo_couleur.grid(row=4, column=1, padx=10, pady=10)

            # Label pour afficher la couleur de l'IA
            cEtiquette_couleur_ia = tk.Label(cCadre_parametres, text="Couleur IA : Jaune⬤", font=("Arial", 12, "italic"),bg="white",fg="#FFD700")
            cEtiquette_couleur_ia.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

            def cMettre_a_jour_couleur_ia(*args):
                """
                Met à jour l'affichage de la couleur de l'IA en fonction du choix du joueur.

                Args:
                    *args: Arguments automatiques du callback trace de StringVar
                """
                if cVariable_couleur_joueur.get() == "Rouge":
                    cEtiquette_couleur_ia.config(text="Couleur IA : Jaune⬤", fg="#FFD700")
                else:
                    cEtiquette_couleur_ia.config(text="Couleur IA : Rouge⬤" , fg="#FF4444")

            cVariable_couleur_joueur.trace("w", cMettre_a_jour_couleur_ia)

        # Bouton Jouer
        cBouton_jouer = tk.Button(
            self.VPA_racine,
            text="JOUER",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=4,
            cursor="hand2",
            command=lambda: cRappel_jouer(cVariable_lignes, cVariable_colonnes, cVariable_alignes, cVariable_premier,
                                         cVariable_couleur_joueur)
        )
        cBouton_jouer.pack(pady=30)

        # Bouton Retour
        cBouton_retour = tk.Button(
            self.VPA_racine,
            text="Retour au menu",
            font=("Arial", 14),
            bg="#757575",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_retour
        )
        cBouton_retour.pack(pady=10)


class VueActions:
    """
    Vue pour les boutons d'action affiché à côté de la grille de jeu.

    Fournit des boutons pour annuler/refaire des coups, rejouer une partie
    ou retourner au menu principal.
    """

    def __init__(self, racine):
        """
        Initialise la vue des action.

        Args:
            racine (tk.Tk): Fenêtre principale Tkinter
        """
        self.VAT_racine = racine
        self.VAT_cadre_actions = None

    def VAT_creer_interface(self, cRappel_annuler, cRappel_refaire, cRappel_rejouer, cRappel_accueil):
        """
        Crée l'interface des boutons d'action.

        Args:
            cRappel_annuler (callable): Fonction appelée lors du clic sur "Undo"
            cRappel_refaire (callable): Fonction appelée lors du clic sur "Redo"
            cRappel_rejouer (callable): Fonction appelée lors du clic sur "Rejouer"
            cRappel_accueil (callable): Fonction appelée lors du clic sur "Home"
        """
        # Frame pour contenir les boutons d'action
        self.VAT_cadre_actions = tk.Frame(self.VAT_racine, bg="white")
        self.VAT_cadre_actions.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

        # Titre de la section
        cTitre_actions = tk.Label(
            self.VAT_cadre_actions,
            text="ACTIONS",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#333333"
        )
        cTitre_actions.pack(pady=10)

        # Frame pour les boutons Annuler et Refaire (côte à côte)
        cCadre_annuler_refaire = tk.Frame(self.VAT_cadre_actions, bg="white")
        cCadre_annuler_refaire.pack(pady=10)

        # Bouton Annuler
        cBouton_annuler = tk.Button(
            cCadre_annuler_refaire,
            text="Undo",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=8,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_annuler
        )
        cBouton_annuler.pack(side=tk.LEFT, padx=5)

        # Bouton Refaire
        cBouton_refaire = tk.Button(
            cCadre_annuler_refaire,
            text="Redo",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=8,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_refaire
        )
        cBouton_refaire.pack(side=tk.LEFT, padx=5)

        # Bouton Rejouer
        cBouton_rejouer = tk.Button(
            self.VAT_cadre_actions,
            text="Rejouer",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=18,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_rejouer
        )
        cBouton_rejouer.pack(pady=10)

        # Bouton Accueil
        cBouton_accueil = tk.Button(
            self.VAT_cadre_actions,
            text="Home",
            font=("Arial", 14, "bold"),
            bg="#757575",
            fg="white",
            width=18,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=cRappel_accueil
        )
        cBouton_accueil.pack(pady=10)