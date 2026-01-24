import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class VueGrille:
    """Vue pour la grille de jeu Puissance 4"""

    def __init__(self, root, rows, cols, cell_size):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        self.colonne_survol = None
        self.pions_affiches = {}

        # Couleurs des joueurs
        self.couleurs = {
            1: "#FF4444",  # Rouge pour joueur 1
            -1: "#FFD700"  # Jaune pour joueur -1
        }

        # Chargement et redimensionnement des images
        self.img_normal = Image.open("../affichage/exportAuto/normalCELL.png")
        self.img_bottom = Image.open("../affichage/exportAuto/bottomCELL.png")

        self.img_normal = self.img_normal.resize((self.cell_size, self.cell_size), Image.LANCZOS)
        self.img_bottom = self.img_bottom.resize((self.cell_size, self.cell_size), Image.LANCZOS)

        self.tk_img_normal = ImageTk.PhotoImage(self.img_normal)
        self.tk_img_bottom = ImageTk.PhotoImage(self.img_bottom)

        # Configuration de la fenêtre
        window_width = self.cols * self.cell_size + 340
        window_height = self.rows * self.cell_size + 40
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.title("Puissance 4")

        # Canvas pour afficher la grille
        self.canvas = tk.Canvas(
            root,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)

        self.afficher_grille()

    def afficher_grille(self):
        """Affiche toutes les cellules de la grille"""
        self.canvas.delete("grille")

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size

                if row == self.rows - 1:
                    self.canvas.create_image(x, y, image=self.tk_img_bottom, anchor="nw", tags="grille")
                else:
                    self.canvas.create_image(x, y, image=self.tk_img_normal, anchor="nw", tags="grille")

        self.canvas.tag_raise("grille")

    def afficher_effet_survol(self, col):
        """Affiche un effet d'ombre sur la colonne survolée"""
        self.canvas.delete("survol")
        self.colonne_survol = col

        for row in range(self.rows):
            x = col * self.cell_size
            y = row * self.cell_size

            self.canvas.create_rectangle(
                x, y, x + self.cell_size, y + self.cell_size,
                fill="gray", stipple="gray50", tags="survol"
            )

    def effacer_effet_survol(self):
        """Efface l'effet de survol"""
        self.canvas.delete("survol")
        self.colonne_survol = None

    def animer_chute_pion(self, col, row_final, joueur, callback):
        """Anime la chute du pion avec effet de gravité et rebond"""
        couleur = self.couleurs[joueur]
        x_center = col * self.cell_size + self.cell_size // 2
        y_final = row_final * self.cell_size + self.cell_size // 2

        y = -self.cell_size // 2
        VELOCITY = 0
        GRAVITY = 3
        DAMPING  = 0.2
        rayon = self.cell_size // 2

        pion = self.canvas.create_oval(
            x_center - rayon, y - rayon,
            x_center + rayon, y + rayon,
            fill=couleur, outline="#8B4513", width=3, tags="pion"
        )

        def animer():
            nonlocal y, VELOCITY

            VELOCITY += GRAVITY
            y += VELOCITY

            if y >= y_final:
                y = y_final
                VELOCITY = -VELOCITY * DAMPING

                if abs(VELOCITY) < 0.5:
                    self.canvas.coords(
                        pion,
                        x_center - rayon, y_final - rayon,
                        x_center + rayon, y_final + rayon
                    )
                    self.pions_affiches[(row_final, col)] = pion
                    self.canvas.tag_raise("grille")
                    callback()
                    return

            self.canvas.coords(
                pion,
                x_center - rayon, y - rayon,
                x_center + rayon, y + rayon
            )

            self.canvas.tag_raise("grille")
            self.root.after(16, animer)

        animer()

    def afficher_message(self, message):
        """Affiche un message de fin de partie"""
        width = self.cols * self.cell_size
        height = self.rows * self.cell_size

        self.canvas.create_rectangle(
            width // 4, height // 2 - 40,
            3 * width // 4, height // 2 + 40,
            fill="white", outline="black", width=3, tags="message"
        )

        self.canvas.create_text(
            width // 2, height // 2,
            text=message, font=("Arial", 20, "bold"),
            tags="message"
        )

    def rafraichir_grille(self, matrice):
        """Rafraîchit l'affichage de la grille à partir de la matrice"""
        self.canvas.delete("pion")
        self.canvas.delete("message")  # Supprimer le message de victoire (
        self.pions_affiches.clear()

        for r in range(self.rows):
            for c in range(self.cols):
                val = matrice[r][c]
                if val != 0:
                    couleur = self.couleurs[val]
                    x = c * self.cell_size + self.cell_size // 2
                    y = r * self.cell_size + self.cell_size // 2
                    rayon = self.cell_size // 2
                    self.canvas.create_oval(
                        x - rayon, y - rayon,
                        x + rayon, y + rayon,
                        fill=couleur, outline="#8B4513", width=3, tags="pion"
                    )
        self.canvas.tag_raise("grille")


class VueHome:
    """Vue pour le menu d'accueil"""

    def __init__(self, root):
        self.root = root
        self.root.geometry("400x500")
        self.root.configure(bg="white")

    def creer_interface(self, callback_1v1, callback_facile, callback_moyen, callback_difficile):
        """Crée l'interface du menu d'accueil"""
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()

        # Titre
        titre = tk.Label(
            self.root,
            text="PUISSANCE 4",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#333333"
        )
        titre.pack(pady=40)

        # Sous-titre
        sous_titre = tk.Label(
            self.root,
            text="Choisissez votre mode de jeu",
            font=("Arial", 14),
            bg="white",
            fg="#666666"
        )
        sous_titre.pack(pady=10)

        # Bouton 1v1
        btn_1v1 = tk.Button(
            self.root,
            text="Mode 1v1",
            font=("Arial", 16, "bold"),
            bg="#2196F3",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_1v1
        )
        btn_1v1.pack(pady=15)

        # Séparateur
        separateur = tk.Label(
            self.root,
            text="─── Contre l'IA ───",
            font=("Arial", 12),
            bg="white",
            fg="#999999"
        )
        separateur.pack(pady=10)

        # Bouton Facile
        btn_facile = tk.Button(
            self.root,
            text="Facile ★",
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_facile
        )
        btn_facile.pack(pady=10)

        # Bouton Moyen
        btn_moyen = tk.Button(
            self.root,
            text="Moyen ★★",
            font=("Arial", 16, "bold"),
            bg="#FF9800",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_moyen
        )
        btn_moyen.pack(pady=10)

        # Bouton Difficile
        btn_difficile = tk.Button(
            self.root,
            text="Difficile ★★★",
            font=("Arial", 16, "bold"),
            bg="#F44336",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_difficile
        )
        btn_difficile.pack(pady=10)


class VueParametres:
    """Vue pour la page des paramètres"""

    def __init__(self, root, mode_ia, difficulte):
        self.root = root
        self.mode_ia = mode_ia
        self.difficulte = difficulte

    def creer_interface(self, callback_jouer, callback_retour):
        """Crée l'interface des paramètres"""
        # Nettoyer la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("550x700")
        self.root.configure(bg="white")

        # Titre
        titre = tk.Label(
            self.root,
            text="PARAMÈTRES",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#333333"
        )
        titre.pack(pady=30)

        # Affichage du mode sélectionné
        if self.mode_ia is None:
            mode_text = "Mode 1v1"
            mode_color = "#000000"
        else:
            difficulte_text = {1: "Facile", 3: "Moyen", 5: "Difficile"}.get(self.difficulte, "Moyen")
            mode_text = f"Contre l'IA - {difficulte_text}"
            mode_color = "#000000"

        mode_label = tk.Label(
            self.root,
            text=f"Mode de jeu : {mode_text}",
            font=("Arial", 16, "bold"),
            bg=mode_color,
            fg="white",
            padx=20,
            pady=10,
            relief="raised",
            bd=3
        )
        mode_label.pack(pady=20)

        # Variables pour les paramètres
        var_rows = tk.StringVar(value="6")
        var_cols = tk.StringVar(value="7")
        var_aligned = tk.StringVar(value="4")
        var_premier = tk.StringVar(value="Joueur" if self.mode_ia else "Rouge")
        var_couleur_joueur = tk.StringVar(value="Rouge")

        # Frame pour les paramètres
        frame_params = tk.Frame(self.root, bg="white")
        frame_params.pack(pady=20)

        # Nombre de lignes
        tk.Label(frame_params, text="Nombre de lignes :", font=("Arial", 12), bg="white").grid(row=0, column=0,
                                                                                                padx=10,
                                                                                                pady=10, sticky="w")
        combo_rows = ttk.Combobox(frame_params, textvariable=var_rows, values=list(range(4, 11)), width=15,
                                  font=("Arial", 12), state="readonly")
        combo_rows.grid(row=0, column=1, padx=10, pady=10)

        # Nombre de colonnes
        tk.Label(frame_params, text="Nombre de colonnes :", font=("Arial", 12), bg="white").grid(row=1, column=0,
                                                                                                  padx=10,
                                                                                                  pady=10, sticky="w")
        combo_cols = ttk.Combobox(frame_params, textvariable=var_cols, values=list(range(4, 11)), width=15,
                                  font=("Arial", 12), state="readonly")
        combo_cols.grid(row=1, column=1, padx=10, pady=10)

        # Nombre de pions alignés
        tk.Label(frame_params, text="Pions à aligner :", font=("Arial", 12), bg="white").grid(row=2, column=0,
                                                                                               padx=10,
                                                                                               pady=10, sticky="w")
        combo_aligned = ttk.Combobox(frame_params, textvariable=var_aligned, values=list(range(3, 7)), width=15,
                                     font=("Arial", 12), state="readonly")
        combo_aligned.grid(row=2, column=1, padx=10, pady=10)

        # Qui commence en premier
        tk.Label(frame_params, text="Qui commence :", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10,
                                                                                            pady=10, sticky="w")
        if self.mode_ia is None:
            combo_premier = ttk.Combobox(frame_params, textvariable=var_premier, values=["Rouge", "Jaune"], width=15,
                                         font=("Arial", 12), state="readonly")
        else:
            combo_premier = ttk.Combobox(frame_params, textvariable=var_premier, values=["Joueur", "IA"], width=15,
                                         font=("Arial", 12), state="readonly")
        combo_premier.grid(row=3, column=1, padx=10, pady=10)

        # Couleur du joueur (seulement en mode IA)
        if self.mode_ia is not None:
            tk.Label(frame_params, text="Couleur joueur :", font=("Arial", 12), bg="white").grid(row=4, column=0,
                                                                                                  padx=10,
                                                                                                  pady=10, sticky="w")
            combo_couleur = ttk.Combobox(frame_params, textvariable=var_couleur_joueur,
                                         values=["Rouge", "Jaune"], width=15,
                                         font=("Arial", 12), state="readonly")
            combo_couleur.grid(row=4, column=1, padx=10, pady=10)

            # Label pour afficher la couleur de l'IA
            label_couleur_ia = tk.Label(frame_params, text="Couleur IA : Jaune⬤", font=("Arial", 12, "italic"),
                                        bg="white",
                                        fg="#FFD700")
            label_couleur_ia.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

            def update_couleur_ia(*args):
                """Met à jour la couleur de l'IA en fonction de la couleur du joueur"""
                if var_couleur_joueur.get() == "Rouge":
                    label_couleur_ia.config(text="Couleur IA : Jaune⬤", fg="#FFD700")
                else:
                    label_couleur_ia.config(text="Couleur IA : Rouge⬤", fg="#FF4444")

            var_couleur_joueur.trace("w", update_couleur_ia)

        # Bouton Jouer
        btn_jouer = tk.Button(
            self.root,
            text="JOUER",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=4,
            cursor="hand2",
            command=lambda: callback_jouer(var_rows, var_cols, var_aligned, var_premier, var_couleur_joueur)
        )
        btn_jouer.pack(pady=30)

        # Bouton Retour
        btn_retour = tk.Button(
            self.root,
            text="Retour au menu",
            font=("Arial", 14),
            bg="#757575",
            fg="white",
            width=20,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_retour
        )
        btn_retour.pack(pady=10)


class VueActions:
    """Vue pour les boutons d'action à côté de la grille"""

    def __init__(self, root):
        self.root = root
        self.frame_actions = None

    def creer_interface(self, callback_undo, callback_redo, callback_rejouer, callback_home):
        """Crée l'interface des actions"""
        # Frame pour contenir les boutons d'action
        self.frame_actions = tk.Frame(self.root, bg="white")
        self.frame_actions.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

        # Titre de la section
        titre_actions = tk.Label(
            self.frame_actions,
            text="ACTIONS",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#333333"
        )
        titre_actions.pack(pady=10)

        # Frame pour les boutons Undo et Redo (côte à côte)
        frame_undo_redo = tk.Frame(self.frame_actions, bg="white")
        frame_undo_redo.pack(pady=10)

        # Bouton Undo
        btn_undo = tk.Button(
            frame_undo_redo,
            text="Undo",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=8,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_undo
        )
        btn_undo.pack(side=tk.LEFT, padx=5)

        # Bouton Redo
        btn_redo = tk.Button(
            frame_undo_redo,
            text="Redo",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=8,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_redo
        )
        btn_redo.pack(side=tk.LEFT, padx=5)

        # Bouton Rejouer
        btn_rejouer = tk.Button(
            self.frame_actions,
            text="Rejouer",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            width=18,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_rejouer
        )
        btn_rejouer.pack(pady=10)

        # Bouton Home
        btn_home = tk.Button(
            self.frame_actions,
            text="Home",
            font=("Arial", 14, "bold"),
            bg="#757575",
            fg="white",
            width=18,
            height=2,
            relief="raised",
            bd=3,
            cursor="hand2",
            command=callback_home
        )
        btn_home.pack(pady=10)