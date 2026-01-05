import tkinter as tk

root = tk.Tk()

# Méthode 1 : Taille totale de l'écran
largeur_totale = root.winfo_screenwidth()
hauteur_totale = root.winfo_screenheight()

# Méthode 2 : Taille sans la barre des tâches (Windows)
largeur_utilisable = root.winfo_screenmmwidth()
hauteur_utilisable = root.winfo_screenmmheight()

print(f"Taille totale écran : {largeur_totale}x{hauteur_totale}")
print(f"Taille utilisable : {largeur_utilisable}x{hauteur_utilisable}")

root.destroy()