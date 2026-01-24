import tkinter as tk


class GrillePuissance4View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(expand=True, fill="both")

        self.frame_grille = None
        self.labels = []
        self.label_info = None

    # ------------------------------------------------------------------
    # UTILITAIRES
    # ------------------------------------------------------------------

    def detruire(self):
        self.frame_principal.destroy()

    def nettoyer(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------------
    # ÉCRANS
    # ------------------------------------------------------------------

    def fenetre_home(self):
        self.nettoyer()

        tk.Label(
            self.frame_principal,
            text="PUISSANCE 4",
            font=("Arial", 24, "bold")
        ).pack(pady=30)

        tk.Button(
            self.frame_principal,
            text="Joueur vs Joueur",
            width=20,
            command=lambda: self.controller.lancer_partie(mode_ia=False)
        ).pack(pady=10)

        tk.Button(
            self.frame_principal,
            text="Joueur vs IA",
            width=20,
            command=self.controller.aller_parametres
        ).pack(pady=10)

        tk.Button(
            self.frame_principal,
            text="Quitter",
            width=20,
            command=self.root.quit
        ).pack(pady=30)

    def fenetre_parametres(self):
        self.nettoyer()

        tk.Label(
            self.frame_principal,
            text="Paramètres IA",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.frame_principal, text="Difficulté").pack()

        difficulte = tk.IntVar(value=5)

        tk.Scale(
            self.frame_principal,
            from_=3,
            to=7,
            orient="horizontal",
            variable=difficulte
        ).pack(pady=10)

        tk.Button(
            self.frame_principal,
            text="Lancer la partie",
            command=lambda: self.controller.lancer_partie(
                mode_ia=True,
                difficulte=difficulte.get()
            )
        ).pack(pady=20)

        tk.Button(
            self.frame_principal,
            text="Retour",
            command=self.controller.aller_home
        ).pack()

    def fenetre_jeu(self):
        self.nettoyer()

        self.label_info = tk.Label(
            self.frame_principal,
            text="",
            font=("Arial", 14)
        )
        self.label_info.pack(pady=10)

        self.frame_grille = tk.Frame(self.frame_principal)
        self.frame_grille.pack()

        self.labels = []

        for r in range(6):
            ligne = []
            for c in range(7):
                label = tk.Label(
                    self.frame_grille,
                    text="⚪",
                    font=("Arial", 28),
                    borderwidth=2,
                    relief="ridge",
                    width=2
                )
                label.grid(row=r, column=c)

                label.bind(
                    "<Button-1>",
                    lambda e, col=c: self.controller.jouer_colonne(col)
                )

                ligne.append(label)
            self.labels.append(ligne)

        frame_actions = tk.Frame(self.frame_principal)
        frame_actions.pack(pady=15)

        tk.Button(frame_actions, text="Undo", command=self.controller.undo).grid(row=0, column=0, padx=5)
        tk.Button(frame_actions, text="Redo", command=self.controller.redo).grid(row=0, column=1, padx=5)
        tk.Button(frame_actions, text="Menu", command=self.controller.aller_home).grid(row=0, column=2, padx=5)

    # ------------------------------------------------------------------
    # AFFICHAGE
    # ------------------------------------------------------------------

    def afficher_pions(self, matrice):
        for r in range(len(matrice)):
            for c in range(len(matrice[0])):
                val = matrice[r][c]
                symbole = "⚪"
                if val == 1:
                    symbole = "🔴"
                elif val == -1:
                    symbole = "🟡"
                self.labels[r][c].config(text=symbole)

    def afficher_joueur_actuel(self, joueur):
        texte = "Tour : 🔴 Rouge" if joueur == 1 else "Tour : 🟡 Jaune"
        self.label_info.config(text=texte)

    def afficher_message_victoire(self, joueur):
        couleur = "🔴 Rouge" if joueur == 1 else "🟡 Jaune"
        self.label_info.config(text=f"🎉 Victoire {couleur} !")

    def afficher_match_nul(self):
        self.label_info.config(text="🤝 Match nul !")
