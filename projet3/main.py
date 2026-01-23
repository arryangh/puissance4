import tkinter as tk
from controleur import Puissance4Controller


def main():
    root = tk.Tk()
    root.title("Puissance 4")
    controller = Puissance4Controller(root)
    controller.lancer_application()
    root.mainloop()


if __name__ == "__main__":
    main()
