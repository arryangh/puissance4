
import tkinter as tk
from controleur import ControleurApplication


def Main():
    """Point d'entrée de l'application"""
    TKroot = tk.Tk()
    TKroot.title("Puissance 4 - Menu")
    ControleurApplication(TKroot)
    TKroot.mainloop()


if __name__ == "__main__":
    Main() #test