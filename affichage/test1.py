import tkinter as tk

# Fenêtre principale
root = tk.Tk()
root.title("Affichage simple")
root.geometry("800x800")  # taille fenêtre

# Canvas plein écran
canvas = tk.Canvas(root, width=800, height=800, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Dimensions
size = 500
x0 = (800 - size) // 2
y0 = (800 - size) // 2
x1 = x0 + size
y1 = y0 + size

# Couleurs proches de l'image
beige = "#FFF4CC"
gold = "#D4B24C"

# Carré
canvas.create_rectangle(
    x0, y0, x1, y1,
    fill=beige,
    outline=gold,
    width=12
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
