import tkinter as tk
from PIL import Image, ImageTk
import sys

sys.path.append('..')  # Pour importer depuis le dossier parent
from Logiquev1 import *


class GrillePuissance4:
    def __init__(self, root, rows=6, cols=7, cell_size=100):
        """
        Affiche une grille Puissance 4 interactive avec animations

        Args:
            root: fenêtre Tkinter
            rows: nombre de lignes (6 par défaut)
            cols: nombre de colonnes (7 par défaut)
            cell_size: taille d'une cellule en pixels
        """
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.colonne_survol = None
        self.animation_en_cours = False
        self.pions_affiches = {}

        # Création de la matrice de jeu
        self.matrice = createMatrice(rows, cols)
        self.joueur_actuel = 1  # 1 pour rouge, -1 pour jaune

        # Couleurs des joueurs
        self.couleurs = {
            1: "#FF4444",  # Rouge pour joueur 1
            -1: "#FFD700"  # Jaune pour joueur -1
        }

        # Chargement et redimensionnement des images
        self.img_normal = Image.open("images/normalCELL.png")
        self.img_bottom = Image.open("images/bottomCELL.png")

        self.img_normal = self.img_normal.resize((cell_size, cell_size), Image.LANCZOS)
        self.img_bottom = self.img_bottom.resize((cell_size, cell_size), Image.LANCZOS)

        self.tk_img_normal = ImageTk.PhotoImage(self.img_normal)
        self.tk_img_bottom = ImageTk.PhotoImage(self.img_bottom)

        # Configuration de la fenêtre
        window_width = cols * cell_size + 40
        window_height = rows * cell_size + 40
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.title("Puissance 4")

        # Canvas pour afficher la grille
        self.canvas = tk.Canvas(
            root,
            width=cols * cell_size,
            height=rows * cell_size,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        # Affichage de la grille
        self.afficher_grille()

        # Binding des événements souris
        self.canvas.bind("<Motion>", self.sur_mouvement_souris)
        self.canvas.bind("<Button-1>", self.sur_clic)
        self.canvas.bind("<Leave>", self.sur_sortie_souris)

    def afficher_grille(self):
        """Affiche toutes les cellules de la grille"""
        self.canvas.delete("grille")

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size

                # Dernière ligne : utilise bottomCELL
                if row == self.rows - 1:
                    self.canvas.create_image(x, y, image=self.tk_img_bottom, anchor="nw", tags="grille")
                else:
                    self.canvas.create_image(x, y, image=self.tk_img_normal, anchor="nw", tags="grille")

    def sur_mouvement_souris(self, event):
        """Gère le survol de la souris pour afficher l'effet d'ombre"""
        if self.animation_en_cours:
            return

        # Calcul de la colonne survolée
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

            # Rectangle semi-transparent pour l'effet d'ombre
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
        if self.animation_en_cours:
            return

        col = event.x // self.cell_size

        if 0 <= col < self.cols:
            self.jouer_coup(col)

    def jouer_coup(self, col):
        """Tente de jouer un coup dans la colonne donnée"""
        # Trouve d'abord la ligne où le pion va tomber AVANT d'ajouter
        row_destination = None
        for row in range(self.rows - 1, -1, -1):
            if self.matrice[row][col] == 0:
                row_destination = row
                break

        if row_destination is None:
            print("Colonne pleine !")
            return  # Colonne pleine

        # Utilise la fonction ajouter_pion de Logiquev1
        resultat = ajouter_pion(self.matrice, self.joueur_actuel, col)

        if resultat == 0:  # Coup valide
            self.animer_chute_pion(col, row_destination, self.joueur_actuel)

    def animer_chute_pion(self, col, row_final, joueur):
        """Anime la chute du pion avec effet de gravité et rebond"""
        self.animation_en_cours = True
        self.effacer_effet_survol()

        couleur = self.couleurs[joueur]
        x_center = col * self.cell_size + self.cell_size // 2
        y_final = row_final * self.cell_size + self.cell_size // 2

        # Paramètres de l'animation
        y = -self.cell_size // 2  # Commence au-dessus de la grille
        velocity = 0
        gravity = 3
        damping = 0.2
        rayon_cercle = self.cell_size // 2 - 14

        # Créer le pion
        pion = self.canvas.create_oval(
            x_center - rayon_cercle, y - rayon_cercle,
            x_center + rayon_cercle, y + rayon_cercle,
            fill=couleur, outline="#8B4513", width=3, tags="pion"
        )

        def animer():
            nonlocal y, velocity

            # Physique de la chute
            velocity += gravity
            y += velocity

            # Rebond au sol
            if y >= y_final:
                y = y_final
                velocity = -velocity * damping

                # Arrêt si rebond trop faible
                if abs(velocity) < 0.5:
                    self.canvas.coords(
                        pion,
                        x_center - rayon_cercle, y_final - rayon_cercle,
                        x_center + rayon_cercle, y_final + rayon_cercle
                    )
                    # Stocker le pion affiché
                    self.pions_affiches[(row_final, col)] = pion
                    self.animation_en_cours = False
                    self.verifier_fin_partie()
                    return

            # Mise à jour de la position
            self.canvas.coords(
                pion,
                x_center - rayon_cercle, y - rayon_cercle,
                x_center + rayon_cercle, y + rayon_cercle
            )

            # Continuer l'animation
            self.root.after(16, animer)  # ~60 FPS

        animer()

    def verifier_fin_partie(self):
        """Vérifie si la partie est terminée"""
        # Utilise la fonction verifier_victoire de Logiquev1
        resultat = verifier_victoire(self.matrice)

        if resultat == 1:
            self.afficher_message("Victoire du joueur ROUGE !")
        elif resultat == -1:
            self.afficher_message("Victoire du joueur JAUNE !")
        elif self.grille_pleine():
            self.afficher_message("Match nul !")
        else:
            # Pas de victoire, changer de joueur
            self.joueur_actuel *= -1

    def grille_pleine(self):
        """Vérifie si la grille est pleine"""
        for col in range(self.cols):
            if self.matrice[0][col] == 0:
                return False
        return True

    def afficher_message(self, message):
        """Affiche un message de fin de partie"""
        # Rectangle de fond
        width = self.cols * self.cell_size
        height = self.rows * self.cell_size

        self.canvas.create_rectangle(
            width // 4, height // 2 - 40,
            3 * width // 4, height // 2 + 40,
            fill="white", outline="black", width=3, tags="message"
        )

        # Texte
        self.canvas.create_text(
            width // 2, height // 2,
            text=message, font=("Arial", 20, "bold"),
            tags="message"
        )

        # Afficher aussi dans la console
        print("\n" + "=" * 50)
        afficherMatrice(self.matrice)
        print(message)
        print("=" * 50)


# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    grille = GrillePuissance4(root, rows=10, cols=10, cell_size=100)
    root.mainloop()