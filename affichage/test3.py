import tkinter as tk

# Couleurs
beige = "#FFF4CC"
gold = "#D4B24C"
border_width = 3


def CreateNormalCell(canvas, x0, y0, cell_size):
    """Cellule avec contours gauche et droite uniquement"""
    x1 = x0 + cell_size
    y1 = y0 + cell_size
    margin = 12

    # Carré beige sans contour
    canvas.create_rectangle(x0, y0, x1, y1, fill=beige, outline="")

    # Bordure gauche
    canvas.create_line(x0, y0, x0, y1, fill=gold, width=border_width)

    # Bordure droite
    canvas.create_line(x1, y0, x1, y1, fill=gold, width=border_width)

    # Cercle blanc centré
    canvas.create_oval(
        x0 + margin, y0 + margin,
        x1 - margin, y1 - margin,
        fill="white", outline=gold, width=3
    )


def CreateBottomCell(canvas, x0, y0, cell_size):
    """Cellule avec contours gauche, droite ET bas"""
    x1 = x0 + cell_size
    y1 = y0 + cell_size
    margin = 12

    # Carré beige sans contour
    canvas.create_rectangle(x0, y0, x1, y1, fill=beige, outline="")

    # Bordure gauche
    canvas.create_line(x0, y0, x0, y1, fill=gold, width=border_width)

    # Bordure droite
    canvas.create_line(x1, y0, x1, y1, fill=gold, width=border_width)

    # Bordure bas
    canvas.create_line(x0, y1, x1, y1, fill=gold, width=border_width)

    # Cercle blanc centré
    canvas.create_oval(
        x0 + margin, y0 + margin,
        x1 - margin, y1 - margin,
        fill="white", outline=gold, width=3
    )


def AfficherGrille(canvas, cols, rows, cell_size=80, start_x=50, start_y=50):
    """Génère une grille Puissance 4 de dimensions cols x rows"""
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * cell_size
            y = start_y + row * cell_size

            # Dernière ligne : cellules avec bordure du bas
            if row == rows - 1:
                CreateBottomCell(canvas, x, y, cell_size)
            else:
                CreateNormalCell(canvas, x, y, cell_size)


# Interface Tkinter
root = tk.Tk()
root.title("Grille Puissance 4")
root.geometry("700x700")

canvas = tk.Canvas(root, width=700, height=700, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Exemple : grille 7 colonnes × 6 lignes (Puissance 4 classique)
AfficherGrille(canvas, cols=7, rows=6, cell_size=80, start_x=50, start_y=50)

root.mainloop()