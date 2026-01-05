import tkinter as tk

# Fenêtre principale
root = tk.Tk()
root.title("Affichage simple")
root.geometry("800x800")

# Canvas
canvas = tk.Canvas(root, width=800, height=800, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Dimensions
size = 700
x0 = (800 - size) // 2
y0 = (800 - size) // 2
x1 = x0 + size
y1 = y0 + size

# Couleurs
beige = "#FFF4CC"
gold = "#D4B24C"
border_width = 12

# Carré SANS contour
canvas.create_rectangle(
    x0, y0, x1, y1,
    fill=beige,
    outline=""
)

# Bordure gauche
canvas.create_line(
    x0, y0, x0, y1,
    fill=gold,
    width=border_width
)

# Bordure droite
canvas.create_line(
    x1, y0, x1, y1,
    fill=gold,
    width=border_width
)

# Cercle centré
margin = 70
canvas.create_oval(
    x0 + margin,
    y0 + margin,
    x1 - margin,
    y1 - margin,
    fill="white",
    outline=gold,
    width=12
)

root.mainloop()
