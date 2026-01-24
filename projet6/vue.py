import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class VueGrille:
    """
    Vue (=Interface graphique) pour afficher et gérer l'interface graphique de la grille de jeu puissance 4.

    Gère l'affichage de la grille, l'animation des pions qui tombent dans la grille, les effets de survol
    et les messages de victoire de fin de partie.
    """

    def __init__(self, racine, lignes, colonnes, taille_cellule):
        """
        Initialise la vue de la grille de jeu (en fonction des dimensions de la grille)

        Args:
            racine (tk.Tk): Fenêtre principale Tkinter
            lignes (int): Nombre de lignes de la grille
            colonnes (int): Nombre de colonnes de la grille
            taille_cellule (int): Taille en pixels d'une cellule
        """
        self.VGR_racine = racine
        self.VGR_lignes = lignes
        self.VGR_colonnes = colonnes
        self.VGR_taille_cellule = taille_cellule

        self.VGR_colonne_survol = None
        self.VGR_pions_affiches = {}

        # Couleurs des joueurs
        self.VGR_couleurs = {
            1: "#FF4444",  # Rouge pour joueur 1
            -1: "#FFD700"  # Jaune pour joueur -1
        }

        # Chargement et redimensionnement des images (les images peuvent être générées par le programme "AUTOgenerate.py"
        self.VGR_img_normale = Image.open("../affichage/exportAuto/normalCELL.png")
        self.VGR_img_bas = Image.open("../affichage/exportAuto/bottomCELL.png")

        self.VGR_img_normale = self.VGR_img_normale.resize((self.VGR_taille_cellule, self.VGR_taille_cellule), Image.LANCZOS)
        self.VGR_img_bas = self.VGR_img_bas.resize((self.VGR_taille_cellule, self.VGR_taille_cellule), Image.LANCZOS)

        self.VGR_tk_img_normale = ImageTk.PhotoImage(self.VGR_img_normale)
        self.VGR_tk_img_bas = ImageTk.PhotoImage(self.VGR_img_bas)

        # Configuration de la fenêtre
        largeur_fenetre = self.VGR_colonnes * self.VGR_taille_cellule + 340
        hauteur_fenetre = self.VGR_lignes * self.VGR_taille_cellule + 40
        self.VGR_racine.geometry(f"{largeur_fenetre}x{hauteur_fenetre}")
        self.VGR_racine.title("Puissance 4")

        # Canvas pour afficher la grille
        self.VGR_canvas = tk.Canvas(
            racine,
            width=self.VGR_colonnes * self.VGR_taille_cellule,
            height=self.VGR_lignes * self.VGR_taille_cellule,
            bg="white",
            highlightthickness=0
        )
        self.VGR_canvas.pack(side=tk.LEFT, padx=20, pady=20)

        self.afficher_grille()

    def afficher_grille(self):
        """
        Affiche toutes les cellules de la grille avec les images appropriées.

        Utilise une image différente pour la ligne du bas (bottomCELL) (avec le trait noir en bas du carré)
        et une image normale pour les autres lignes. (sans le trait noi en bas du carré)
        """
        self.VGR_canvas.delete("grille")

        for ligne in range(self.VGR_lignes):
            for colonne in range(self.VGR_colonnes):
                x = colonne * self.VGR_taille_cellule
                y = ligne * self.VGR_taille_cellule

                if ligne == self.VGR_lignes - 1:
                    self.VGR_canvas.create_image(x, y, image=self.VGR_tk_img_bas, anchor="nw", tags="grille")
                else:
                    self.VGR_canvas.create_image(x, y, image=self.VGR_tk_img_normale, anchor="nw", tags="grille")

        self.VGR_canvas.tag_raise("grille")

    def afficher_effet_survol(self, colonne):
        """
        Affiche un effet d'ombre grise (hachuré) sur la colonne survolée par la souris.

        Args:
            colonne (int): L'indice de la colonne à surligner
        """
        self.VGR_canvas.delete("survol")
        self.VGR_colonne_survol = colonne

        for ligne in range(self.VGR_lignes):
            x = colonne * self.VGR_taille_cellule
            y = ligne * self.VGR_taille_cellule

            self.VGR_canvas.create_rectangle(
                x, y, x + self.VGR_taille_cellule, y + self.VGR_taille_cellule,
                fill="gray", stipple="gray50", tags="survol"
            )

    def effacer_effet_survol(self):
        """
        Efface l'effet de survol de la grille.
        """
        self.VGR_canvas.delete("survol")
        self.VGR_colonne_survol = None

    def animer_chute_pion(self, colonne, ligne_finale, joueur, rappel):
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
        couleur = self.VGR_couleurs[joueur]
        x_centre = colonne * self.VGR_taille_cellule + self.VGR_taille_cellule // 2
        y_finale = ligne_finale * self.VGR_taille_cellule + self.VGR_taille_cellule // 2

        y = -self.VGR_taille_cellule // 2
        VELOCITE = 0
        GRAVITE = 3
        AMORTISSEMENT = 0.2
        rayon = self.VGR_taille_cellule // 2

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
                    self.VGR_pions_affiches[(ligne_finale, colonne)] = pion
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

    def afficher_message(self, message):
        """
        Affiche un message au centre de la grille (typiquement pour la fin de partie).

        Args:
            message (str): Le texte du message à afficher
        """
        largeur = self.VGR_colonnes * self.VGR_taille_cellule
        hauteur = self.VGR_lignes * self.VGR_taille_cellule

        self.VGR_canvas.create_rectangle(
            largeur // 4, hauteur // 2 - 40,
            3 * largeur // 4, hauteur // 2 + 40,
            fill="white", outline="black", width=3, tags="message"
        )

        self.VGR_canvas.create_text(
            largeur // 2, hauteur // 2,
            text=message, font=("Arial", 20, "bold"),
            tags="message"
        )

    def rafraichir_grille(self, matrice):
        """
        Rafraîchit complètement l'affichage de la grille à partir de la matrice.

        Efface tous les pions et messages existants, puis redessine tous les pions
        présents dans la matrice. Utilisé principalement pour les fonctions undo/redo.

        Args:
            matrice (list): La matrice de jeu à afficher
        """
        self.VGR_canvas.delete("pion")
        self.VGR_canvas.delete("message")  # Supprimer le message de victoire
        self.VGR_pions_affiches.clear()

        for ligne in range(self.VGR_lignes):
            for colonne in range(self.VGR_colonnes):
                valeur = matrice[ligne][colonne]
                if valeur != 0:
                    couleur = self.VGR_couleurs[valeur]
                    x = colonne * self.VGR_taille_cellule + self.VGR_taille_cellule // 2
                    y = ligne * self.VGR_taille_cellule + self.VGR_taille_cellule // 2
                    rayon = self.VGR_taille_cellule // 2
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

    def creer_interface(self, rappel_1v1, rappel_facile, rappel_moyen, rappel_difficile):
        """
        Crée l'interface du menu d'accueil avec tous les boutons de sélection.

        Args:
            rappel_1v1 (callable): Fonction appelée lors du clic sur "Mode 1v1"
            rappel_facile (callable): Fonction appelée lors du clic sur "Facile"
            rappel_moyen (callable): Fonction appelée lors du clic sur "Moyen"
            rappel_difficile (callable): Fonction appelée lors du clic sur "Difficile"
        """
        # Nettoyer la fenêtre
        for widget in self.VAC_racine.winfo_children():
            widget.destroy()

        # Titre
        titre = tk.Label(
            self.VAC_racine,
            text="PUISSANCE 4",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#333333"
        )
        titre.pack(pady=40)

        # Sous-titre
        sous_titre = tk.Label(
            self.VAC_racine,
            text="Choisissez votre mode de jeu",
            font=("Arial", 14),
            bg="white",
            fg="#666666"
        )
        sous_titre.pack(pady=10)

        # Bouton 1v1
        bouton_1v1 = tk.Button(
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
            command=rappel_1v1
        )
        bouton_1v1.pack(pady=15)

        # Séparateur
        separateur = tk.Label(
            self.VAC_racine,
            text="─── Contre l'IA ───",
            font=("Arial", 12),
            bg="white",
            fg="#999999"
        )
        separateur.pack(pady=10)

        # Bouton Facile
        bouton_facile = tk.Button(
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
            command=rappel_facile
        )
        bouton_facile.pack(pady=10)

        # Bouton Moyen
        bouton_moyen = tk.Button(
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
            command=rappel_moyen
        )
        bouton_moyen.pack(pady=10)

        # Bouton Difficile
        bouton_difficile = tk.Button(
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
            command=rappel_difficile
        )
        bouton_difficile.pack(pady=10)


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

    def creer_interface(self, rappel_jouer, rappel_retour):
        """
        Crée l'interface de configuration avec tous les paramètres personnalisables.

        Args:
            rappel_jouer (callable): Fonction appelée lors du clic sur "JOUER"
            rappel_retour (callable): Fonction appelée lors du clic sur "Retour au menu"
        """
        # Nettoyer la fenêtre
        for widget in self.VPA_racine.winfo_children():
            widget.destroy()

        self.VPA_racine.geometry("550x700")
        self.VPA_racine.configure(bg="white")

        # Titre
        titre = tk.Label(
            self.VPA_racine,
            text="PARAMÈTRES",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#333333"
        )
        titre.pack(pady=30)

        # Affichage du mode sélectionné
        if self.VPA_mode_ia is None:
            texte_mode = "Mode 1v1"
            couleur_mode = "#000000"
        else:
            texte_difficulte = {1: "Facile", 3: "Moyen", 5: "Difficile"}.get(self.VPA_difficulte, "Moyen")
            texte_mode = f"Contre l'IA - {texte_difficulte}"
            couleur_mode = "#000000"

        etiquette_mode = tk.Label(
            self.VPA_racine,
            text=f"Mode de jeu : {texte_mode}",
            font=("Arial", 16, "bold"),
            bg=couleur_mode,
            fg="white",
            padx=20,
            pady=10,
            relief="raised",
            bd=3
        )
        etiquette_mode.pack(pady=20)

        # Variables pour les paramètres
        variable_lignes = tk.StringVar(value="6")
        variable_colonnes = tk.StringVar(value="7")
        variable_alignes = tk.StringVar(value="4")
        variable_premier = tk.StringVar(value="Joueur" if self.VPA_mode_ia else "Rouge")
        variable_couleur_joueur = tk.StringVar(value="Rouge")

        # Frame pour les paramètres
        cadre_parametres = tk.Frame(self.VPA_racine, bg="white")
        cadre_parametres.pack(pady=20)

        # Nombre de lignes
        tk.Label(cadre_parametres, text="Nombre de lignes :", font=("Arial", 12), bg="white").grid(row=0, column=0,
                                                                                                   padx=10,
                                                                                                   pady=10, sticky="w")
        combo_lignes = ttk.Combobox(cadre_parametres, textvariable=variable_lignes, values=list(range(4, 11)), width=15,
                                    font=("Arial", 12), state="readonly")
        combo_lignes.grid(row=0, column=1, padx=10, pady=10)

        # Nombre de colonnes
        tk.Label(cadre_parametres, text="Nombre de colonnes :", font=("Arial", 12), bg="white").grid(row=1, column=0,
                                                                                                     padx=10,
                                                                                                     pady=10,
                                                                                                     sticky="w")
        combo_colonnes = ttk.Combobox(cadre_parametres, textvariable=variable_colonnes, values=list(range(4, 11)),
                                      width=15,
                                      font=("Arial", 12), state="readonly")
        combo_colonnes.grid(row=1, column=1, padx=10, pady=10)

        # Nombre de pions alignés
        tk.Label(cadre_parametres, text="Pions à aligner :", font=("Arial", 12), bg="white").grid(row=2, column=0,
                                                                                                  padx=10,
                                                                                                  pady=10, sticky="w")
        combo_alignes = ttk.Combobox(cadre_parametres, textvariable=variable_alignes, values=list(range(3, 7)),
                                     width=15,
                                     font=("Arial", 12), state="readonly")
        combo_alignes.grid(row=2, column=1, padx=10, pady=10)

        # Qui commence en premier
        tk.Label(cadre_parametres, text="Qui commence :", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10,
                                                                                               pady=10, sticky="w")
        if self.VPA_mode_ia is None:
            combo_premier = ttk.Combobox(cadre_parametres, textvariable=variable_premier, values=["Rouge", "Jaune"],
                                         width=15,
                                         font=("Arial", 12), state="readonly")
        else:
            combo_premier = ttk.Combobox(cadre_parametres, textvariable=variable_premier, values=["Joueur", "IA"],
                                         width=15,
                                         font=("Arial", 12), state="readonly")
        combo_premier.grid(row=3, column=1, padx=10, pady=10)

        # Couleur du joueur (seulement en mode IA)
        if self.VPA_mode_ia is not None:
            tk.Label(cadre_parametres, text="Couleur joueur :", font=("Arial", 12), bg="white").grid(row=4, column=0,
                                                                                                     padx=10,
                                                                                                     pady=10,
                                                                                                     sticky="w")
            combo_couleur = ttk.Combobox(cadre_parametres, textvariable=variable_couleur_joueur,
                                         values=["Rouge", "Jaune"], width=15,
                                         font=("Arial", 12), state="readonly")
            combo_couleur.grid(row=4, column=1, padx=10, pady=10)

            # Label pour afficher la couleur de l'IA
            etiquette_couleur_ia = tk.Label(cadre_parametres, text="Couleur IA : Jaune⬤", font=("Arial", 12, "italic"),
                                            bg="white",
                                            fg="#FFD700")
            etiquette_couleur_ia.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

            def mettre_a_jour_couleur_ia(*args):
                """
                Met à jour l'affichage de la couleur de l'IA en fonction du choix du joueur.

                Args:
                    *args: Arguments automatiques du callback trace de StringVar
                """
                if variable_couleur_joueur.get() == "Rouge":
                    etiquette_couleur_ia.config(text="Couleur IA : Jaune⬤", fg="#FFD700")
                else:
                    etiquette_couleur_ia.config(text="Couleur IA : Rouge⬤", fg="#FF4444")

            variable_couleur_joueur.trace("w", mettre_a_jour_couleur_ia)

        # Bouton Jouer
        bouton_jouer = tk.Button(
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
            command=lambda: rappel_jouer(variable_lignes, variable_colonnes, variable_alignes, variable_premier,
                                         variable_couleur_joueur)
        )
        bouton_jouer.pack(pady=30)

        # Bouton Retour
        bouton_retour = tk.Button(
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
            command=rappel_retour
        )
        bouton_retour.pack(pady=10)


class VueActions:
    """
    Vue pour les boutons d'action affichés à côté de la grille de jeu.

    Fournit des boutons pour annuler/refaire des coups, rejouer une partie
    ou retourner au menu principal.
    """

    def __init__(self, racine):
        """
        Initialise la vue des actions.

        Args:
            racine (tk.Tk): Fenêtre principale Tkinter
        """
        self.VAT_racine = racine
        self.VAT_cadre_actions = None

    def creer_interface(self, rappel_annuler, rappel_refaire, rappel_rejouer, rappel_accueil):
        """
        Crée l'interface des boutons d'action.

        Args:
            rappel_annuler (callable): Fonction appelée lors du clic sur "Undo"
            rappel_refaire (callable): Fonction appelée lors du clic sur "Redo"
            rappel_rejouer (callable): Fonction appelée lors du clic sur "Rejouer"
            rappel_accueil (callable): Fonction appelée lors du clic sur "Home"
        """
        # Frame pour contenir les boutons d'action
        self.VAT_cadre_actions = tk.Frame(self.VAT_racine, bg="white")
        self.VAT_cadre_actions.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

        # Titre de la section
        titre_actions = tk.Label(
            self.VAT_cadre_actions,
            text="ACTIONS",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#333333"
        )
        titre_actions.pack(pady=10)

        # Frame pour les boutons Annuler et Refaire (côte à côte)
        cadre_annuler_refaire = tk.Frame(self.VAT_cadre_actions, bg="white")
        cadre_annuler_refaire.pack(pady=10)

        # Bouton Annuler
        bouton_annuler = tk.Button(
            cadre_annuler_refaire,
            text="Undo",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=8,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=rappel_annuler
        )
        bouton_annuler.pack(side=tk.LEFT, padx=5)

        # Bouton Refaire
        bouton_refaire = tk.Button(
            cadre_annuler_refaire,
            text="Redo",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=8,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=rappel_refaire
        )
        bouton_refaire.pack(side=tk.LEFT, padx=5)

        # Bouton Rejouer
        bouton_rejouer = tk.Button(
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
            command=rappel_rejouer
        )
        bouton_rejouer.pack(pady=10)

        # Bouton Accueil
        bouton_accueil = tk.Button(
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
            command=rappel_accueil
        )
        bouton_accueil.pack(pady=10)