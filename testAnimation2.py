import tkinter as tk
from PIL import Image, ImageTk

IMG_FILE = "instagram.png"
TARGET_SIZE = (50, 50)

root = tk.Tk()
root.title("Animation image")

canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# --- Chargement + redimensionnement (compatible Pillow 10+) ---
image_original = Image.open(IMG_FILE)
image_resized = image_original.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(image_resized)

# --- Ajouter l'image ---
obj = canvas.create_image(300, 100, image=img)

# Animation
dy = 5
y_min = 100
y_max = 500

def animate():
    global dy
    canvas.move(obj, 0, dy)
    x, y = canvas.coords(obj)

    if y <= y_min or y >= y_max:
        dy = -dy

    canvas.after(10, animate)

animate()
root.mainloop()
