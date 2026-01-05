import tkinter as tk
from PIL import Image, ImageTk


class GrillePuissance4:
    def __init__(self, root, rows=6, cols=7, cell_size=100):
        """
        Affiche une grille Puissance 4 avec les images de cellules

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

    def afficher_grille(self):
        """Affiche toutes les cellules de la grille"""
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size

                # Dernière ligne : utilise bottomCELL
                if row == self.rows - 1:
                    self.canvas.create_image(x, y, image=self.tk_img_bottom, anchor="nw")
                else:
                    self.canvas.create_image(x, y, image=self.tk_img_normal, anchor="nw")


# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    grille = GrillePuissance4(root, rows=6, cols=7, cell_size=100)
    root.mainloop()