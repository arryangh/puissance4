# https://univtoursfr-my.sharepoint.com/:w:/g/personal/romain_blaquart_etu_univ-tours_fr/IQDjbnF5vXxIQLbgv-k0blpYAXK2CnF8Hn0lJXNrlifLY8M?email=aryan.ghalehnoee%40etu.univ-tours.fr&e=VIhnDH

import tkinter as tk
from controleur import ControleurApplication


def main():
    """Point d'entrée de l'application"""
    root = tk.Tk()
    root.title("Puissance 4 - Menu")
    app = ControleurApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main() #test