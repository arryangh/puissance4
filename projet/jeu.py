import tkinter as tk
from PIL import Image, ImageTk
import math


class GrillePuissance4:
    def __init__(self, root, logique, rows=6, cols=7, cell_size=100):
        """
        Affiche une grille Puissance 4 interactive avec animations

        Args:
            root: fenêtre Tkinter
            logique: instance de la classe Logique du jeu
            rows: nombre de lignes (6 par défaut)
            cols: nombre de colonnes (7 par défaut)
            cell_size: taille d'une cellule en pixels
        """
        self.root = root
        self.logique = logique
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.colonne_survol = None
        self.animation_en_cours = False

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
        joueur_actuel = self.logique.joueurActuel
        resultat = self.logique.ajouterPillon(col)

        if resultat:  # Coup valide
            # Trouve la ligne où le pion est tombé
            for row in range(self.rows - 1, -1, -1):
                if self.logique.grille[row][col] == joueur_actuel:
                    self.animer_chute_pion(col, row, joueur_actuel)
                    break

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
        rayon = self.cell_size // 2 - 20

        # Créer le pion
        pion = self.canvas.create_oval(
            x_center - rayon, y - rayon,
            x_center + rayon, y + rayon,
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
                        x_center - rayon, y_final - rayon,
                        x_center + rayon, y_final + rayon
                    )
                    self.animation_en_cours = False
                    self.verifier_fin_partie()
                    return

            # Mise à jour de la position
            self.canvas.coords(
                pion,
                x_center - rayon, y - rayon,
                x_center + rayon, y + rayon
            )

            # Continuer l'animation
            self.root.after(16, animer)  # ~60 FPS

        animer()

    def verifier_fin_partie(self):
        """Vérifie si la partie est terminée"""
        if self.logique.verifierVictoire():
            gagnant = -self.logique.joueurActuel  # Le joueur qui vient de jouer
            couleur = "Rouge" if gagnant == 1 else "Jaune"
            self.afficher_message(f"Victoire du joueur {couleur} !")
        elif self.logique.grillePleine():
            self.afficher_message("Match nul !")

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
            text=message, font=("Arial", 24, "bold"),
            tags="message"
        )


# Exemple d'utilisation (à adapter selon votre fichier Logiquev1.py)
if __name__ == "__main__":
    # Import de votre classe Logique
    # from Logiquev1 import Logique  # À décommenter

    # Classe temporaire pour tester (remplacer par votre vraie classe)
    class LogiqueTest:
        def __init__(self):
            self.grille = [[0] * 7 for _ in range(6)]
            self.joueurActuel = 1

        def ajouterPillon(self, col):
            for row in range(5, -1, -1):
                if self.grille[row][col] == 0:
                    self.grille[row][col] = self.joueurActuel
                    self.joueurActuel *= -1
                    return True
            return False

        def verifierVictoire(self):
            # Simplified victory check
            return False

        def grillePleine(self):
            return all(self.grille[0][col] != 0 for col in range(7))


    root = tk.Tk()
    logique = LogiqueTest()  # Remplacer par: logique = Logique()
    grille = GrillePuissance4(root, logique, rows=6, cols=7, cell_size=100)
    root.mainloop()