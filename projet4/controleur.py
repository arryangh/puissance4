from logique import JeuPuissance4
from interface import GrillePuissance4View


class Puissance4Controller:
    def __init__(self, root):
        self.root = root

        self.mode_ia = False
        self.difficulte = 5

        self.modele = None
        self.vue = None
        self.tour_verrouille = False

    # ------------------------------------------------------------------
    # LANCEMENT
    # ------------------------------------------------------------------

    def lancer_application(self):
        self.aller_home()

    # ------------------------------------------------------------------
    # NAVIGATION
    # ------------------------------------------------------------------

    def aller_home(self):
        if self.vue:
            self.vue.detruire()

        self.vue = GrillePuissance4View(self.root, self)
        self.vue.fenetre_home()

    def aller_parametres(self):
        self.vue.fenetre_parametres()

    def lancer_partie(self, mode_ia=False, difficulte=5):
        self.mode_ia = mode_ia
        self.difficulte = difficulte

        self.modele = JeuPuissance4(
            mode_ia=self.mode_ia,
            difficulte=self.difficulte
        )

        self.vue.fenetre_jeu()
        self.rafraichir_vue()

        if self.modele.est_tour_ia():
            self.jouer_ia_si_necessaire()

    # ------------------------------------------------------------------
    # ACTIONS DE JEU
    # ------------------------------------------------------------------

    def jouer_colonne(self, col):
        if self.tour_verrouille:
            return  # IGNORE les clics

        if not self.modele:
            return

        if self.modele.jouer_coup(col):
            self.rafraichir_vue()
            self.tour_suivant()

    def tour_suivant(self):
        gagnant = self.modele.get_gagnant()

        if gagnant != 0:
            self.vue.afficher_message_victoire(gagnant)
            return

        if self.modele.grille_pleine():
            self.vue.afficher_match_nul()
            return

        self.jouer_ia_si_necessaire()

    def jouer_ia_si_necessaire(self):
        if self.modele.est_tour_ia():
            self.tour_verrouille = True
            self.root.after(300, self._tour_ia)

    def _tour_ia(self):
        self.modele.jouer_coup_ia()
        self.rafraichir_vue()

        self.tour_verrouille = False
        self.tour_suivant()

    # ------------------------------------------------------------------
    # UNDO / REDO
    # ------------------------------------------------------------------

    def undo(self):
        if self.tour_verrouille:
            return

        if self.modele and self.modele.annuler_coup():
            self.rafraichir_vue()

    def redo(self):
        if self.tour_verrouille:
            return

        if self.modele and self.modele.refaire_coup():
            self.rafraichir_vue()

    # ------------------------------------------------------------------
    # SYNCHRONISATION
    # ------------------------------------------------------------------

    def rafraichir_vue(self):
        self.vue.afficher_pions(self.modele.get_matrice())
        self.vue.afficher_joueur_actuel(self.modele.get_joueur_actuel())
