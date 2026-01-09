import tkinter as tk
from PIL import Image, ImageTk
import math
from functools import lru_cache

# =========================================================
# ===================== LOGIQUE IA =========================
# =========================================================

ROWS = 6
COLS = 7
MOVE_ORDER = [3, 4, 2, 5, 1, 6, 0]


def createMatrice(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]


def afficherMatrice(m):
    for r in m:
        print(r)


def ajouter_pion(matrice, joueur, col):
    for row in range(len(matrice) - 1, -1, -1):
        if matrice[row][col] == 0:
            matrice[row][col] = joueur
            return 0
    return -1


def verifier_victoire(matrice, n):
    rows, cols = len(matrice), len(matrice[0])
    for r in range(rows):
        for c in range(cols):
            if matrice[r][c] == 0:
                continue
            joueur = matrice[r][c]
            for dr, dc in [(1,0),(0,1),(1,1),(1,-1)]:
                if all(
                    0 <= r+dr*i < rows and
                    0 <= c+dc*i < cols and
                    matrice[r+dr*i][c+dc*i] == joueur
                    for i in range(n)
                ):
                    return joueur
    return 0


class Bitboard:
    def __init__(self, player=0, mask=0):
        self.player = player
        self.mask = mask

    def can_play(self, col):
        return not (self.mask & (1 << (col * 7 + ROWS)))

    def play(self, col):
        move = self.mask + (1 << (col * 7))
        self.player ^= self.mask
        self.mask = move

    def is_win(self, board):
        for shift in (1, 7, 6, 8):
            m = board & (board >> shift)
            if m & (m >> (2 * shift)):
                return True
        return False


def matrix_to_bitboard(matrice, joueur):
    player = 0
    mask = 0
    for col in range(COLS):
        for row in range(ROWS):
            cell = matrice[ROWS - 1 - row][col]
            if cell != 0:
                bit = 1 << (col * 7 + row)
                mask |= bit
                if cell == joueur:
                    player |= bit
    return Bitboard(player, mask)


@lru_cache(None)
def negamax(player, mask, depth, alpha, beta):
    board = Bitboard(player, mask)

    if board.is_win(player):
        return -(42 - bin(mask).count("1")) // 2

    if depth == 0:
        return 0

    for col in MOVE_ORDER:
        if board.can_play(col):
            b2 = Bitboard(board.player, board.mask)
            b2.play(col)
            score = -negamax(b2.player, b2.mask, depth - 1, -beta, -alpha)
            if score >= beta:
                return score
            alpha = max(alpha, score)

    return alpha


def meilleur_coup_ia(matrice, joueur, profondeur, _):
    board = matrix_to_bitboard(matrice, joueur)
    best_score = -math.inf
    best_col = None

    for col in MOVE_ORDER:
        if board.can_play(col):
            b2 = Bitboard(board.player, board.mask)
            b2.play(col)
            score = -negamax(
                b2.player, b2.mask,
                profondeur,
                -math.inf, math.inf
            )
            if score > best_score:
                best_score = score
                best_col = col

    return best_col


# =========================================================
# ===================== INTERFACE ==========================
# =========================================================

class GrillePuissance4:
    def __init__(self, root, rows=6, cols=7, nb_aligned=4,
                 mode_ia="jaune", difficulte=5):

        self.root = root
        self.rows = rows
        self.cols = cols
        self.nb_aligned = nb_aligned
        self.mode_ia = mode_ia
        self.difficulte = difficulte

        self.cell_size = 90
        self.colonne_survol = None
        self.animation_en_cours = False
        self.pions_affiches = {}
        self.partie_terminee = False

        self.matrice = createMatrice(rows, cols)
        self.joueur_actuel = 1

        self.couleurs = {1: "#FF4444", -1: "#FFD700"}

        self.img_normal = Image.open("images/normalCELL.png").resize(
            (self.cell_size, self.cell_size), Image.LANCZOS)
        self.img_bottom = Image.open("images/bottomCELL.png").resize(
            (self.cell_size, self.cell_size), Image.LANCZOS)

        self.tk_img_normal = ImageTk.PhotoImage(self.img_normal)
        self.tk_img_bottom = ImageTk.PhotoImage(self.img_bottom)

        self.root.geometry(
            f"{cols * self.cell_size + 40}x{rows * self.cell_size + 40}")
        self.root.title("Puissance 4")

        self.canvas = tk.Canvas(
            root,
            width=cols * self.cell_size,
            height=rows * self.cell_size,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        self.afficher_grille()

        self.canvas.bind("<Motion>", self.sur_mouvement_souris)
        self.canvas.bind("<Button-1>", self.sur_clic)
        self.canvas.bind("<Leave>", lambda e: self.canvas.delete("survol"))

        if self.mode_ia == "rouge":
            self.root.after(500, self.tour_ia)

    def afficher_grille(self):
        for r in range(self.rows):
            for c in range(self.cols):
                img = self.tk_img_bottom if r == self.rows - 1 else self.tk_img_normal
                self.canvas.create_image(
                    c * self.cell_size, r * self.cell_size,
                    image=img, anchor="nw", tags="grille")

    def sur_mouvement_souris(self, event):
        if self.animation_en_cours or self.partie_terminee:
            return
        if self.mode_ia and self.est_tour_ia():
            return

        col = event.x // self.cell_size
        self.canvas.delete("survol")

        if 0 <= col < self.cols:
            for r in range(self.rows):
                self.canvas.create_rectangle(
                    col * self.cell_size, r * self.cell_size,
                    (col + 1) * self.cell_size, (r + 1) * self.cell_size,
                    fill="gray", stipple="gray50", tags="survol"
                )

    def sur_clic(self, event):
        if self.animation_en_cours or self.partie_terminee:
            return
        if self.mode_ia and self.est_tour_ia():
            return

        col = event.x // self.cell_size
        if 0 <= col < self.cols:
            self.jouer_coup(col)

    def est_tour_ia(self):
        return (self.mode_ia == "rouge" and self.joueur_actuel == 1) or \
               (self.mode_ia == "jaune" and self.joueur_actuel == -1)

    def tour_ia(self):
        col = meilleur_coup_ia(
            self.matrice, self.joueur_actuel, self.difficulte, self.nb_aligned)
        self.jouer_coup(col)

    def jouer_coup(self, col):
        for r in range(self.rows - 1, -1, -1):
            if self.matrice[r][col] == 0:
                ajouter_pion(self.matrice, self.joueur_actuel, col)
                self.animer_pion(col, r)
                break

    def animer_pion(self, col, row):
        self.animation_en_cours = True
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        r = self.cell_size // 2 - 4

        pion = self.canvas.create_oval(
            x - r, -r, x + r, r,
            fill=self.couleurs[self.joueur_actuel],
            outline="black", width=2)

        def drop(y_pos=-r):
            if y_pos < y:
                self.canvas.move(pion, 0, 20)
                self.root.after(16, lambda: drop(y_pos + 20))
            else:
                self.canvas.coords(pion, x-r, y-r, x+r, y+r)
                self.animation_en_cours = False
                self.fin_tour()

        drop()

    def fin_tour(self):
        res = verifier_victoire(self.matrice, self.nb_aligned)
        if res != 0:
            self.partie_terminee = True
            afficherMatrice(self.matrice)
            print("Victoire", "ROUGE" if res == 1 else "JAUNE")
            return

        self.joueur_actuel *= -1
        if self.mode_ia and self.est_tour_ia():
            self.root.after(300, self.tour_ia)


# =========================================================
# ======================== MAIN =============================
# =========================================================

if __name__ == "__main__":
    root = tk.Tk()
    GrillePuissance4(root, mode_ia="jaune", difficulte=5)
    root.mainloop()
