import copy


class JeuPuissance4:
    def __init__(self, rows=6, cols=7, nb_aligned=4, mode_ia=False, difficulte=5):
        self.rows = rows
        self.cols = cols
        self.nb_aligned = nb_aligned
        self.mode_ia = mode_ia
        self.profondeur_ia = difficulte

        self.matrice = self._create_matrice()
        self.joueur_actuel = 1
        self.gagnant = 0

        # Historique (undo / redo)
        self.historique = []
        self.index_historique = -1
        self._sauvegarder_etat()

    # ------------------------------------------------------------------
    # ÉTAT
    # ------------------------------------------------------------------

    def _create_matrice(self):
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def reset_partie(self):
        self.matrice = self._create_matrice()
        self.joueur_actuel = 1
        self.gagnant = 0
        self.historique = []
        self.index_historique = -1
        self._sauvegarder_etat()

    def _sauvegarder_etat(self):
        if self.index_historique < len(self.historique) - 1:
            self.historique = self.historique[:self.index_historique + 1]

        self.historique.append(copy.deepcopy(self.matrice))
        self.index_historique += 1

    # ------------------------------------------------------------------
    # ACTIONS DE JEU
    # ------------------------------------------------------------------

    def coup_valide(self, col):
        return 0 <= col < self.cols and self.matrice[0][col] == 0

    def jouer_coup(self, col):
        if not self.coup_valide(col) or self.gagnant != 0:
            return False

        for row in range(self.rows - 1, -1, -1):
            if self.matrice[row][col] == 0:
                self.matrice[row][col] = self.joueur_actuel
                break

        self._sauvegarder_etat()

        self.gagnant = self.verifier_victoire()
        if self.gagnant == 0:
            self.joueur_actuel *= -1

        return True

    # ------------------------------------------------------------------
    # UNDO / REDO
    # ------------------------------------------------------------------

    def annuler_coup(self):
        pas = 2 if self.mode_ia else 1
        if self.index_historique - pas < 0:
            return False

        self.index_historique -= pas
        self._restaurer_etat()
        return True

    def refaire_coup(self):
        pas = 2 if self.mode_ia else 1
        if self.index_historique + pas >= len(self.historique):
            return False

        self.index_historique += pas
        self._restaurer_etat()
        return True

    def _restaurer_etat(self):
        etat = self.historique[self.index_historique]
        self.matrice = copy.deepcopy(etat)
        self.gagnant = self.verifier_victoire()

    # ------------------------------------------------------------------
    # RÈGLES
    # ------------------------------------------------------------------

    def verifier_victoire(self):
        m = self.matrice
        n = self.nb_aligned

        for r in range(self.rows):
            for c in range(self.cols - n + 1):
                if m[r][c] != 0 and all(m[r][c + i] == m[r][c] for i in range(n)):
                    return m[r][c]

        for r in range(self.rows - n + 1):
            for c in range(self.cols):
                if m[r][c] != 0 and all(m[r + i][c] == m[r][c] for i in range(n)):
                    return m[r][c]

        for r in range(self.rows - n + 1):
            for c in range(self.cols - n + 1):
                if m[r][c] != 0 and all(m[r + i][c + i] == m[r][c] for i in range(n)):
                    return m[r][c]

        for r in range(n - 1, self.rows):
            for c in range(self.cols - n + 1):
                if m[r][c] != 0 and all(m[r - i][c + i] == m[r][c] for i in range(n)):
                    return m[r][c]

        return 0

    def grille_pleine(self):
        return all(self.matrice[0][c] != 0 for c in range(self.cols))

    # ------------------------------------------------------------------
    # IA
    # ------------------------------------------------------------------

    def est_tour_ia(self):
        return self.mode_ia and self.joueur_actuel == -1

    def jouer_coup_ia(self):
        col = self.meilleur_coup_ia()
        if col is not None:
            self.jouer_coup(col)

    def meilleur_coup_ia(self):
        coups = [c for c in range(self.cols) if self.coup_valide(c)]
        if not coups:
            return None

        for col in coups:
            temp = copy.deepcopy(self.matrice)
            self._ajouter_pion_temp(temp, -1, col)
            if self._verifier_victoire_temp(temp) == -1:
                return col

        meilleur_col = coups[0]
        meilleure_valeur = float("-inf")

        for col in coups:
            temp = copy.deepcopy(self.matrice)
            self._ajouter_pion_temp(temp, -1, col)
            val = self._minimax(temp, self.profondeur_ia - 1, False)
            if val > meilleure_valeur:
                meilleure_valeur = val
                meilleur_col = col

        return meilleur_col

    # ------------------------------------------------------------------
    # IA — OUTILS INTERNES (repris tels quels)
    # ------------------------------------------------------------------

    def _ajouter_pion_temp(self, matrice, joueur, col):
        for r in range(self.rows - 1, -1, -1):
            if matrice[r][col] == 0:
                matrice[r][col] = joueur
                return

    def _verifier_victoire_temp(self, matrice):
        self_temp = self.matrice
        self.matrice = matrice
        res = self.verifier_victoire()
        self.matrice = self_temp
        return res

    def _minimax(self, matrice, profondeur, est_max):
        victoire = self._verifier_victoire_temp(matrice)
        if profondeur == 0 or victoire != 0:
            return victoire * 1000

        coups = [c for c in range(self.cols) if matrice[0][c] == 0]

        if est_max:
            return max(
                self._minimax(self._simuler(matrice, -1, c), profondeur - 1, False)
                for c in coups
            )
        else:
            return min(
                self._minimax(self._simuler(matrice, 1, c), profondeur - 1, True)
                for c in coups
            )

    def _simuler(self, matrice, joueur, col):
        temp = copy.deepcopy(matrice)
        self._ajouter_pion_temp(temp, joueur, col)
        return temp

    # ------------------------------------------------------------------
    # ACCESSEURS (POUR LA VUE)
    # ------------------------------------------------------------------

    def get_matrice(self):
        return self.matrice

    def get_joueur_actuel(self):
        return self.joueur_actuel

    def get_gagnant(self):
        return self.gagnant
