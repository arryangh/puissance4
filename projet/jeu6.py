import tkinter as tk
from PIL import Image, ImageTk
import sys
import time

sys.path.append('..')  # Pour importer depuis le dossier parent
from Logiquev1 import *


class InfoPanel:
    """Panel d'information modulaire affiché à droite du jeu"""

    def __init__(self, parent, rows, cols, mode_ia, difficulte):
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.mode_ia = mode_ia
        self.difficulte = difficulte

        # Statistiques du jeu
        self.nb_coups = 0
        self.temps_reflection_start = None
        self.temps_reflection_actuel = 0.0

        # Créer le frame principal du panel
        self.frame = tk.Frame(parent, bg="#f0f0f0", relief="ridge", bd=2)
        self.frame.pack(side="right", padx=(0, 20), pady=20, anchor="n")

        # Largeur fixe pour le panel
        self.panel_width = 200

        self.creer_widgets()

    def creer_widgets(self):
        """Crée tous les widgets du panel"""
        # Titre
        titre = tk.Label(
            self.frame,
            text="📊 INFOS",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        titre.pack(pady=(10, 15))

        # Séparateur
        self._creer_separateur()

        # Dimensions
        self._creer_info_label("Dimensions:", f"{self.rows}x{self.cols}")

        # Difficulté
        difficulte_text = self._get_difficulte_text()
        self._creer_info_label("Difficulté:", difficulte_text)

        # Nombre de coups
        self.label_coups = self._creer_info_label("Coups joués:", "0")

        self._creer_separateur()

        # Section IA (uniquement si mode IA)
        if self.mode_ia:
            ia_titre = tk.Label(
                self.frame,
                text="🤖 IA",
                font=("Arial", 11, "bold"),
                bg="#f0f0f0",
                fg="#333333"
            )
            ia_titre.pack(pady=(5, 10))

            # Temps de réflexion
            temps_label = tk.Label(
                self.frame,
                text="Temps réflexion:",
                font=("Arial", 9, "bold"),
                bg="#f0f0f0",
                fg="#555555",
                anchor="w"
            )
            temps_label.pack(fill="x", padx=15, pady=(0, 2))

            self.label_temps = tk.Label(
                self.frame,
                text="0.000s",
                font=("Arial", 10),
                bg="#f0f0f0",
                fg="#333333",
                anchor="w"
            )
            self.label_temps.pack(fill="x", padx=20, pady=(0, 15))

    def _creer_separateur(self):
        """Crée une ligne de séparation"""
        sep = tk.Frame(self.frame, height=2, bg="#cccccc")
        sep.pack(fill="x", padx=15, pady=10)

    def _creer_info_label(self, titre, valeur):
        """Crée un couple titre/valeur"""
        frame = tk.Frame(self.frame, bg="#f0f0f0")
        frame.pack(fill="x", padx=15, pady=5)

        label_titre = tk.Label(
            frame,
            text=titre,
            font=("Arial", 9, "bold"),
            bg="#f0f0f0",
            fg="#555555",
            anchor="w"
        )
        label_titre.pack(anchor="w")

        label_valeur = tk.Label(
            frame,
            text=valeur,
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#333333",
            anchor="w"
        )
        label_valeur.pack(anchor="w", padx=(10, 0))

        return label_valeur

    def _get_difficulte_text(self):
        """Retourne le texte de difficulté"""
        if not self.mode_ia:
            return "1v1"

        difficulte_map = {
            3: "😊 Facile",
            5: "😐 Moyen",
            7: "😈 Difficile"
        }
        return difficulte_map.get(self.difficulte, "?")

    def incrementer_coups(self):
        """Incrémente le compteur de coups"""
        self.nb_coups += 1
        self.label_coups.config(text=str(self.nb_coups))

    def demarrer_reflexion(self):
        """Démarre le chronomètre de réflexion de l'IA"""
        if not self.mode_ia:
            return

        self.temps_reflection_start = time.time()
        self._animer_reflexion()

    def _animer_reflexion(self):
        """Met à jour le temps de réflexion"""
        if self.temps_reflection_start is None:
            return

        # Calculer le temps écoulé
        temps_ecoule = time.time() - self.temps_reflection_start
        self.temps_reflection_actuel = temps_ecoule

        # Mettre à jour le label de temps
        self.label_temps.config(text=f"{temps_ecoule:.3f}s")

        # Continuer l'animation
        if self.temps_reflection_start is not None:
            self.parent.after(50, self._animer_reflexion)

    def arreter_reflexion(self):
        """Arrête le chronomètre de réflexion"""
        if not self.mode_ia or self.temps_reflection_start is None:
            return

        # Calculer le temps final
        temps_final = time.time() - self.temps_reflection_start
        self.temps_reflection_actuel = temps_final
        self.label_temps.config(text=f"{temps_final:.3f}s")

        # Arrêter l'animation
        self.temps_reflection_start = None

    def destroy(self):
        """Détruit le panel"""
        self.frame.destroy()


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
        self.joueur_actuel = 1  # 1 pour rouge, -1 pour jaune

        # Couleurs des joueurs
        self.couleurs = {
            1: "#FF4444",  # Rouge pour joueur 1
            -1: "#FFD700"  # Jaune pour joueur -1
        }

        # Chargement et redimensionnement des images
        self.img_normal = Image.open("images/normalCELL.png")
        self.img_bottom = Image.open("images/bottomCELL.png")

        self.img_normal = self.img_normal.resize((self.cell_size, self.cell_size), Image.LANCZOS)
        self.img_bottom = self.img_bottom.resize((self.cell_size, self.cell_size), Image.LANCZOS)

        self.tk_img_normal = ImageTk.PhotoImage(self.img_normal)
        self.tk_img_bottom = ImageTk.PhotoImage(self.img_bottom)

        # Configuration de la fenêtre
        window_width = self.cols * self.cell_size + 300  # +300 pour le panel
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
        self.canvas.pack(side="left", padx=20, pady=20)

        # Créer le panel d'information
        self.info_panel = InfoPanel(root, rows, cols, mode_ia, difficulte)

        # Affichage de la grille
        self.afficher_grille()

        # Binding des événements souris
        self.canvas.bind("<Motion>", self.sur_mouvement_souris)
        self.canvas.bind("<Button-1>", self.sur_clic)
        self.canvas.bind("<Leave>", self.sur_sortie_souris)

        # Si l'IA commence (joueur rouge), jouer son coup
        if self.mode_ia == "rouge":
            self.root.after(500, self.tour_ia)

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

        # Démarrer le chronomètre
        self.info_panel.demarrer_reflexion()

        joueur_ia = 1 if self.mode_ia == "rouge" else -1
        col = meilleur_coup_ia(self.matrice, joueur_ia, self.difficulte, self.nb_aligned)

        # Arrêter le chronomètre
        self.info_panel.arreter_reflexion()

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

        if resultat == 0:
            # Incrémenter le compteur de coups
            self.info_panel.incrementer_coups()
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


def fenetre_home():
    """
    Fenêtre d'accueil avec sélection du mode de jeu
    """
    root = tk.Tk()
    root.title("Puissance 4 - Menu")
    root.geometry("400x500")
    root.configure(bg="white")

    def lancer_jeu(mode_ia=None, difficulte=None):
        """Lance le jeu avec les paramètres choisis"""
        # Détruire tous les widgets de la fenêtre home
        for widget in root.winfo_children():
            widget.destroy()

        # Créer le jeu
        GrillePuissance4(root, rows=6, cols=7, nb_aligned=4, mode_ia=mode_ia, difficulte=difficulte)

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
        command=lambda: lancer_jeu(mode_ia=None, difficulte=None)
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
        command=lambda: lancer_jeu(mode_ia="jaune", difficulte=3)
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
        command=lambda: lancer_jeu(mode_ia="jaune", difficulte=5)
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
        command=lambda: lancer_jeu(mode_ia="jaune", difficulte=7)
    )
    btn_difficile.pack(pady=10)

    root.mainloop()


# Lancement de l'application
if __name__ == "__main__":
    fenetre_home()