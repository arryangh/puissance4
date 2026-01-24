
import tkinter as tk
from controleur import ControleurApplication


def main():
    """Point d'entrée de l'application"""
    root = tk.Tk()
    root.title("Puissance 4 - Menu")
    app = ControleurApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main() #lolllllll