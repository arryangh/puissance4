import tkinter as tk
from PIL import Image, ImageTk
import sys

sys.path.append('..')  # Pour importer depuis le dossier parent
from Logiquev3 import *


class GrillePuissance4:
    def __init__(self, root, rows=6, cols=7, nb_aligned=4, mode_ia=None, difficulte=None):
        """
        Affiche une grille Puissance 4 interactive avec animations

        Args:
            root: fenêtre Tkinter
            rows: nombre de lignes (6 par défaut)
            cols: nombre de colonnes (7 par défaut)
            nb_aligned: nombre de jetons alignés pour gagner (4 par défaut)
            mode_ia: None pour 1v1, "rouge" ou "jaune" pour jouer contre l'IA
            difficulte: profondeur de l'IA (3, 5 ou 7)
        """
        self.root = root
        self.rows = rows
        self.cols = cols
        self.nb_aligned = nb_aligned
        self.mode_ia = mode_ia
        self.difficulte = difficulte

        # Calcul dynamique de la taille des cellules
        max_dim = max(rows, cols)
        if max_dim <= 7:
            self.cell_size = (2560 // 20)
        else:
            self.cell_size = int((1600 // 14) * (7 / max_dim))

        self.colonne_survol = None
        self.animation_en_cours = False
        self.pions_affiches = {}
        self.partie_terminee = False

        # Création de la matrice de jeu
        self.matrice = createMatrice(rows, cols)
        reset_historique(self.matrice) # ajout du système d'historique
        self.joueur_actuel = 1  # 1 pour rouge, -1 pour jaune

        # Couleurs des joueurs
        self.couleurs = {
            1: "#FF4444",  # Rouge pour joueur 1
            -1: "#FFD700"  # Jaune pour joueur -1
        }

        # Chargement et redimensionnement des images
        """
        self.img_normal = Image.open("images/normalCELL.png")
        self.img_bottom = Image.open("images/bottomCELL.png")
        """
        self.img_normal = Image.open("../affichage/exportAuto/normalCELL.png")
        self.img_bottom = Image.open("../affichage/exportAuto/bottomCELL.png"
                                     "")

        self.img_normal = self.img_normal.resize((self.cell_size, self.cell_size), Image.LANCZOS)
        self.img_bottom = self.img_bottom.resize((self.cell_size, self.cell_size), Image.LANCZOS)

        self.tk_img_normal = ImageTk.PhotoImage(self.img_normal)
        self.tk_img_bottom = ImageTk.PhotoImage(self.img_bottom)

        # Configuration de la fenêtre - MODIFIÉ ICI ↓
        window_width = self.cols * self.cell_size + 340  # +340 au lieu de +40
        window_height = self.rows * self.cell_size + 40
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.title("Puissance 4")

        # Canvas pour afficher la grille - MODIFIÉ ICI ↓
        self.canvas = tk.Canvas(
            root,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)  # ← Ajout de side=tk.LEFT

        # Affichage de la grille
        self.afficher_grille()

        # Binding des événements souris
        self.canvas.bind("<Motion>", self.sur_mouvement_souris)
        self.canvas.bind("<Button-1>", self.sur_clic)
        self.canvas.bind("<Leave>", self.sur_sortie_souris)

        # ⚠️ CORRECTION : Ne plus appeler tour_ia() automatiquement ici
        # C'est maintenant géré dans lancer_jeu()

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





    def sur_mouvement_souris(self, event):
        """Gère le survol de la souris pour afficher l'effet d'ombre"""
        if self.animation_en_cours or self.partie_terminee:
            return

        # Bloquer le survol si c'est le tour de l'IA
        if self.mode_ia and self.est_tour_ia():
            return

        col = event.x // self.cell_size

        if 0 <= col < self.cols:
            if col != self.colonne_survol:
                self.colonne_survol = col
                self.afficher_effet_survol(col)
        else:
            self.effacer_effet_survol()

    def sur_sortie_souris(self, event):
        """Efface l'effet de survol quand la souris quitte le canvas"""
        self.effacer_effet_survol()

    def afficher_effet_survol(self, col):
        """Affiche un effet d'ombre sur la colonne survolée"""
        self.canvas.delete("survol")

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
        sauvegarder_etat(self.matrice) # sauvegarder le coup dans l'historique

        if resultat == 0:
            self.animer_chute_pion(col, row_destination, self.joueur_actuel)

    def animer_chute_pion(self, col, row_final, joueur):
        """Anime la chute du pion avec effet de gravité et rebond"""
        self.animation_en_cours = True
        self.effacer_effet_survol()

        couleur = self.couleurs[joueur]
        x_center = col * self.cell_size + self.cell_size // 2
        y_final = row_final * self.cell_size + self.cell_size // 2

        y = -self.cell_size // 2
        velocity = 0
        gravity = 3
        damping = 0.2
        rayon = self.cell_size // 2

        pion = self.canvas.create_oval(
            x_center - rayon, y - rayon,
            x_center + rayon, y + rayon,
            fill=couleur, outline="#8B4513", width=3, tags="pion"
        )

        def animer():
            nonlocal y, velocity

            velocity += gravity
            y += velocity

            if y >= y_final:
                y = y_final
                velocity = -velocity * damping

                if abs(velocity) < 0.5:
                    self.canvas.coords(
                        pion,
                        x_center - rayon, y_final - rayon,
                        x_center + rayon, y_final + rayon
                    )
                    self.pions_affiches[(row_final, col)] = pion
                    self.canvas.tag_raise("grille")
                    self.animation_en_cours = False
                    self.verifier_fin_partie()
                    return

            self.canvas.coords(
                pion,
                x_center - rayon, y - rayon,
                x_center + rayon, y + rayon
            )

            self.canvas.tag_raise("grille")
            self.root.after(16, animer)

        animer()

    def verifier_fin_partie(self):
        """Vérifie si la partie est terminée"""
        resultat = verifier_victoire(self.matrice, self.nb_aligned)

        if resultat == 1:
            self.partie_terminee = True
            self.effacer_effet_survol()
            self.afficher_message("🎉 Victoire du joueur ROUGE ! 🎉")
        elif resultat == -1:
            self.partie_terminee = True
            self.effacer_effet_survol()
            self.afficher_message("🎉 Victoire du joueur JAUNE ! 🎉")
        elif self.grille_pleine():
            self.partie_terminee = True
            self.effacer_effet_survol()
            self.afficher_message("Match nul !")
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

        print("\n" + "=" * 50)
        afficherMatrice(self.matrice)
        print(message)
        print("=" * 50)


def fenetre_parametres(root, mode_ia, difficulte):
    """
    Page de paramètres avant de lancer le jeu

    Args:
        root: fenêtre Tkinter
        mode_ia: None pour 1v1, "rouge" ou "jaune" pour jouer contre l'IA
        difficulte: profondeur de l'IA (1, 3 ou 5)
    """
    from tkinter import ttk

    # Nettoyer la fenêtre
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("550x700")
    root.configure(bg="white")

    # Titre
    titre = tk.Label(
        root,
        text="⚙️ PARAMÈTRES ⚙️",
        font=("Arial", 28, "bold"),
        bg="white",
        fg="#333333"
    )
    titre.pack(pady=30)

    # Affichage du mode sélectionné
    if mode_ia is None:
        mode_text = "Mode 1v1"
        mode_color = "#4CAF50"
    else:
        difficulte_text = {1: "Facile", 3: "Moyen", 5: "Difficile"}.get(difficulte, "Moyen")
        mode_text = f"Contre l'IA - {difficulte_text}"
        mode_color = "#2196F3"

    mode_label = tk.Label(
        root,
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
    var_premier = tk.StringVar(value="Joueur" if mode_ia else "Rouge")
    var_couleur_joueur = tk.StringVar(value="Rouge")

    # Frame pour les paramètres
    frame_params = tk.Frame(root, bg="white")
    frame_params.pack(pady=20)

    # Nombre de lignes
    tk.Label(frame_params, text="Nombre de lignes :", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=10,
                                                                                           pady=10, sticky="w")
    combo_rows = ttk.Combobox(frame_params, textvariable=var_rows, values=list(range(4, 11)), width=15,
                              font=("Arial", 12), state="readonly")
    combo_rows.grid(row=0, column=1, padx=10, pady=10)

    # Nombre de colonnes
    tk.Label(frame_params, text="Nombre de colonnes :", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=10,
                                                                                             pady=10, sticky="w")
    combo_cols = ttk.Combobox(frame_params, textvariable=var_cols, values=list(range(4, 11)), width=15,
                              font=("Arial", 12), state="readonly")
    combo_cols.grid(row=1, column=1, padx=10, pady=10)

    # Nombre de pions alignés
    tk.Label(frame_params, text="Pions à aligner :", font=("Arial", 12), bg="white").grid(row=2, column=0, padx=10,
                                                                                          pady=10, sticky="w")
    combo_aligned = ttk.Combobox(frame_params, textvariable=var_aligned, values=list(range(3, 7)), width=15,
                                 font=("Arial", 12), state="readonly")
    combo_aligned.grid(row=2, column=1, padx=10, pady=10)

    # Qui commence en premier
    tk.Label(frame_params, text="Qui commence :", font=("Arial", 12), bg="white").grid(row=3, column=0, padx=10,
                                                                                       pady=10, sticky="w")
    if mode_ia is None:
        # Mode 1v1
        combo_premier = ttk.Combobox(frame_params, textvariable=var_premier, values=["Rouge", "Jaune"], width=15,
                                     font=("Arial", 12), state="readonly")
    else:
        # Mode contre IA
        combo_premier = ttk.Combobox(frame_params, textvariable=var_premier, values=["Joueur", "IA"], width=15,
                                     font=("Arial", 12), state="readonly")
    combo_premier.grid(row=3, column=1, padx=10, pady=10)

    # Couleur du joueur (seulement en mode IA)
    if mode_ia is not None:
        tk.Label(frame_params, text="Couleur joueur :", font=("Arial", 12), bg="white").grid(row=4, column=0, padx=10,
                                                                                             pady=10, sticky="w")
        combo_couleur = ttk.Combobox(frame_params, textvariable=var_couleur_joueur, values=["Rouge", "Jaune"], width=15,
                                     font=("Arial", 12), state="readonly")
        combo_couleur.grid(row=4, column=1, padx=10, pady=10)

        # Label pour afficher la couleur de l'IA
        label_couleur_ia = tk.Label(frame_params, text="Couleur IA : Jaune", font=("Arial", 12, "italic"), bg="white",
                                    fg="#FF9800")
        label_couleur_ia.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        def update_couleur_ia(*args):
            """Met à jour la couleur de l'IA en fonction de la couleur du joueur"""
            if var_couleur_joueur.get() == "Rouge":
                label_couleur_ia.config(text="Couleur IA : Jaune", fg="#FF9800")
            else:
                label_couleur_ia.config(text="Couleur IA : Rouge", fg="#FF4444")

        var_couleur_joueur.trace("w", update_couleur_ia)

    # Bouton Jouer
    def lancer_jeu():
        for widget in root.winfo_children():
            widget.destroy()

        rows = int(var_rows.get())
        cols = int(var_cols.get())
        nb_aligned = int(var_aligned.get())

        # Déterminer qui commence et les couleurs
        if mode_ia is None:
            # Mode 1v1
            premier = var_premier.get()  # "Rouge" ou "Jaune"
            mode_ia_final = None
            couleur_joueur = None
        else:
            # Mode contre IA
            couleur_joueur = var_couleur_joueur.get()
            premier = var_premier.get()  # "Joueur" ou "IA"

            # Déterminer le mode_ia en fonction de la couleur du joueur
            if couleur_joueur == "Rouge":
                mode_ia_final = "jaune"  # L'IA est jaune
            else:
                mode_ia_final = "rouge"  # L'IA est rouge

        # Créer le jeu
        jeu = GrillePuissance4(root, rows=rows, cols=cols, nb_aligned=nb_aligned,
                               mode_ia=mode_ia_final if mode_ia else None, difficulte=difficulte)

        # ⚠️ CORRECTION : Déterminer qui commence de manière claire
        if mode_ia is None:
            # Mode 1v1
            if premier == "Jaune":
                jeu.joueur_actuel = -1
            else:
                jeu.joueur_actuel = 1
        else:
            # Mode contre IA
            if premier == "IA":
                # L'IA commence
                if mode_ia_final == "rouge":
                    jeu.joueur_actuel = 1
                else:
                    jeu.joueur_actuel = -1
                # Faire jouer l'IA après un délai
                root.after(500, jeu.tour_ia)
            else:
                # Le joueur commence
                if couleur_joueur == "Rouge":
                    jeu.joueur_actuel = 1
                else:
                    jeu.joueur_actuel = -1

        print("ici le jeu est lancé")
        fenetre_action(root, jeu, lancer_jeu) # fenetre à cauté de la grille de jeu

    btn_jouer = tk.Button(
        root,
        text="🎮 JOUER",
        font=("Arial", 18, "bold"),
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        relief="raised",
        bd=4,
        cursor="hand2",
        command=lancer_jeu
    )
    btn_jouer.pack(pady=30)

    # Bouton Retour
    btn_retour = tk.Button(
        root,
        text="⬅️ Retour au menu",
        font=("Arial", 14),
        bg="#757575",
        fg="white",
        width=20,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda: fenetre_home(root)
    )
    btn_retour.pack(pady=10)




def fenetre_action(root, jeu, lancer_jeu):
    """
    Crée une section d'actions à côté de la grille avec des boutons

    Args:
        root: fenêtre Tkinter principale
        canvas: le canvas de la grille de jeu
    """
    # Frame pour contenir les boutons d'action
    frame_actions = tk.Frame(root, bg="white")
    frame_actions.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

    # Titre de la section
    titre_actions = tk.Label(
        frame_actions,
        text="🎮 ACTIONS",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#333333"
    )
    titre_actions.pack(pady=10)

    # Frame pour les boutons Undo et Redo (côte à côte)
    frame_undo_redo = tk.Frame(frame_actions, bg="white")
    frame_undo_redo.pack(pady=10)

    # Bouton Undo
    btn_undo = tk.Button(
        frame_undo_redo,
        text="↶ Undo",
        font=("Arial", 12, "bold"),
        bg="#FF9800",
        fg="white",
        width=8,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda: undo_gui(jeu) # undo côté GUI
    )
    btn_undo.pack(side=tk.LEFT, padx=5)

    # Bouton Redo
    btn_redo = tk.Button(
        frame_undo_redo,
        text="↷ Redo",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=8,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda: redo_gui(jeu) # redo côté GUI
    )
    btn_redo.pack(side=tk.LEFT, padx=5)

    # Bouton Rejouer
    btn_rejouer = tk.Button(
        frame_actions,
        text="🔄 Rejouer",
        font=("Arial", 14, "bold"),
        bg="#4CAF50",
        fg="white",
        width=18,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lancer_jeu
    )
    btn_rejouer.pack(pady=10)

    # Bouton Home
    btn_home = tk.Button(
        frame_actions,
        text="🏠 Home",
        font=("Arial", 14, "bold"),
        bg="#757575",
        fg="white",
        width=18,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda:fenetre_home(root) #retourner dans home
    )
    btn_home.pack(pady=10)

def fenetre_home(root=None):
    """
    Fenêtre d'accueil avec sélection du mode de jeu
    """
    if root is None:
        root = tk.Tk()
        root.title("Puissance 4 - Menu")
    else:
        # Nettoyer la fenêtre
        for widget in root.winfo_children():
            widget.destroy()

    root.geometry("400x500")
    root.configure(bg="white")

    # Titre
    titre = tk.Label(
        root,
        text="🎮 PUISSANCE 4 🎮",
        font=("Arial", 28, "bold"),
        bg="white",
        fg="#333333"
    )
    titre.pack(pady=40)

    # Sous-titre
    sous_titre = tk.Label(
        root,
        text="Choisissez votre mode de jeu",
        font=("Arial", 14),
        bg="white",
        fg="#666666"
    )
    sous_titre.pack(pady=10)

    # Bouton 1v1
    btn_1v1 = tk.Button(
        root,
        text="👥 Mode 1v1",
        font=("Arial", 16, "bold"),
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda: fenetre_parametres(root, mode_ia=None, difficulte=None)
    )
    btn_1v1.pack(pady=15)

    # Séparateur
    separateur = tk.Label(
        root,
        text="─── Contre l'IA ───",
        font=("Arial", 12),
        bg="white",
        fg="#999999"
    )
    separateur.pack(pady=10)

    # Bouton Facile
    btn_facile = tk.Button(
        root,
        text="😊 Facile",
        font=("Arial", 16, "bold"),
        bg="#2196F3",
        fg="white",
        width=20,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda: fenetre_parametres(root, mode_ia="jaune", difficulte=1)
    )
    btn_facile.pack(pady=10)

    # Bouton Moyen
    btn_moyen = tk.Button(
        root,
        text="😐 Moyen",
        font=("Arial", 16, "bold"),
        bg="#FF9800",
        fg="white",
        width=20,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda: fenetre_parametres(root, mode_ia="jaune", difficulte=3)
    )
    btn_moyen.pack(pady=10)

    # Bouton Difficile
    btn_difficile = tk.Button(
        root,
        text="😈 Difficile",
        font=("Arial", 16, "bold"),
        bg="#F44336",
        fg="white",
        width=20,
        height=2,
        relief="raised",
        bd=3,
        cursor="hand2",
        command=lambda: fenetre_parametres(root, mode_ia="jaune", difficulte=5)
    )
    btn_difficile.pack(pady=10)

    if root.winfo_exists():
        root.mainloop()





# fonctions undo / Redo côté GUI:

def rafraichir_grille(jeu):
    jeu.canvas.delete("pion")
    jeu.pions_affiches.clear()

    for r in range(jeu.rows):
        for c in range(jeu.cols):
            val = jeu.matrice[r][c]
            if val != 0:
                couleur = jeu.couleurs[val]
                x = c * jeu.cell_size + jeu.cell_size // 2
                y = r * jeu.cell_size + jeu.cell_size // 2
                rayon = jeu.cell_size // 2
                jeu.canvas.create_oval(
                    x - rayon, y - rayon,
                    x + rayon, y + rayon,
                    fill=couleur, outline="#8B4513", width=3, tags="pion"
                )
    jeu.canvas.tag_raise("grille")


def undo_gui(jeu):
    if undo_redo(jeu.matrice, "u", jeu.mode_ia) == 0:

        # En mode IA on recule de 2 coups → le joueur rejoue
        if jeu.mode_ia is not None:
            # Le joueur reste le même
            pass
        else:
            # En 1v1 on change de joueur
            jeu.joueur_actuel *= -1

        jeu.partie_terminee = False
        rafraichir_grille(jeu)


def redo_gui(jeu):
    if undo_redo(jeu.matrice, "r", jeu.mode_ia) == 0:

        # En mode IA on rejoue un tour complet → le joueur reste le même
        if jeu.mode_ia is not None:
            pass
        else:
            jeu.joueur_actuel *= -1

        rafraichir_grille(jeu)





# Lancement de l'application
if __name__ == "__main__":
    fenetre_home()