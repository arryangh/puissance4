import tkinter as tk

# Fenêtre
root = tk.Tk()
root.title("Animation cercle")

# Canvas
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()

# Création du cercle
obj = canvas.create_oval(130, 0, 170, 40, fill="red")

# Variables de mouvement
dy = 3  # vitesse verticale
y_min = 0
y_max = 200


def animate():
    global dy

    # Déplacer le cercle
    canvas.move(obj, 0, dy)

    # Position actuelle du cercle
    x1, y1, x2, y2 = canvas.coords(obj)

    # Si on touche les limites, on inverse la direction
    if y1 <= y_min or y1 >= y_max:
        dy = -dy

    # rappeller animate toutes les 10ms
    canvas.after(10, animate)


# Lancer l’animation
animate()

root.mainloop()
