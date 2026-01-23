import tkinter as tk
from tkinter import messagebox
import time
from numba import njit


# =====================
# OPENING BOOK

# =====================

BOOK_MAX_MOVES = 10   # nombre de demi-coups couverts

BOOK = {
    0x0000000000000000: 3,  # position initiale -> centre
}

def position_hash(board0, board1):
    return (board0 * 6364136223846793005 + board1) & 0xFFFFFFFFFFFFFFFF



# =====================
# CONSTANTES
# =====================
ROWS = 6
COLS = 7
MAX_MOVES = ROWS * COLS
WIN_SCORE = 100000
MAX_DEPTH = 18
MOVE_ORDER = (3, 2, 4, 1, 5, 0, 6)

CELL = 80
RADIUS = 34

# =====================
# BITBOARD CORE
# =====================

@njit
def check_win(bb):
    m = bb & (bb >> 1)
    if m & (m >> 2):
        return True
    m = bb & (bb >> 7)
    if m & (m >> 14):
        return True
    m = bb & (bb >> 6)
    if m & (m >> 12):
        return True
    m = bb & (bb >> 8)
    if m & (m >> 16):
        return True
    return False


@njit
def can_play(mask, col):
    return (mask & (1 << (col * 7 + 5))) == 0


@njit
def play(board, mask, col):
    for r in range(ROWS):
        bit = 1 << (col * 7 + r)
        if (mask & bit) == 0:
            return board | bit, mask | bit
    return board, mask


@njit
def winning_move(board, mask, col):
    for r in range(ROWS):
        bit = 1 << (col * 7 + r)
        if (mask & bit) == 0:
            return check_win(board | bit)
    return False


@njit
def evaluate(board, opp):
    score = 0
    center = 3
    for r in range(ROWS):
        bit = 1 << (center * 7 + r)
        if board & bit:
            score += 3
        elif opp & bit:
            score -= 3
    return score


@njit
def negamax(board, opp, mask, depth, alpha, beta, moves):
    if check_win(opp):
        return -(WIN_SCORE - moves)

    if moves == MAX_MOVES:
        return 0

    if depth == 0:
        return evaluate(board, opp)

    for col in MOVE_ORDER:
        if can_play(mask, col) and winning_move(board, mask, col):
            return WIN_SCORE - moves

    best = -WIN_SCORE
    for col in MOVE_ORDER:
        if can_play(mask, col):
            b2, m2 = play(board, mask, col)
            score = -negamax(opp, b2, m2, depth - 1, -beta, -alpha, moves + 1)
            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
    return best


def best_move(board0, board1, mask, turn, moves):
    if moves <= BOOK_MAX_MOVES:
        h = position_hash(board0, board1)
        if h in BOOK:
            return BOOK[h]

    board = board0 if turn == 0 else board1
    opp = board1 if turn == 0 else board0

    for col in MOVE_ORDER:
        if can_play(mask, col) and winning_move(board, mask, col):
            return col

    for col in MOVE_ORDER:
        if can_play(mask, col) and winning_move(opp, mask, col):
            return col

    best_score = -WIN_SCORE
    best_col = 3

    for col in MOVE_ORDER:
        if can_play(mask, col):
            b2, m2 = play(board, mask, col)
            score = -negamax(opp, b2, m2, MAX_DEPTH - 1,
                             -WIN_SCORE, WIN_SCORE, moves + 1)
            if score > best_score:
                best_score = score
                best_col = col

    return best_col


# =====================
# TKINTER GUI
# =====================

class Connect4GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4 – IA Numba")

        self.canvas = tk.Canvas(
            self.root,
            width=COLS * CELL,
            height=ROWS * CELL,
            bg="#0066cc"
        )
        self.canvas.pack()

        self.info = tk.Label(self.root, text="À toi de jouer 🟡", font=("Arial", 14))
        self.info.pack()

        tk.Button(self.root, text="Rejouer", command=self.reset).pack(pady=5)

        self.canvas.bind("<Button-1>", self.click)

        self.reset()
        self.draw()

        self.root.mainloop()

    def reset(self):
        self.board = [0, 0]
        self.mask = 0
        self.turn = 0
        self.moves = 0
        self.game_over = False
        self.info.config(text="À toi de jouer 🟡")

    def draw(self):
        self.canvas.delete("all")
        for c in range(COLS):
            for r in range(ROWS):
                x = c * CELL + CELL // 2
                y = (ROWS - 1 - r) * CELL + CELL // 2
                color = "white"

                bit = 1 << (c * 7 + r)
                if self.board[0] & bit:
                    color = "gold"
                elif self.board[1] & bit:
                    color = "red"

                self.canvas.create_oval(
                    x - RADIUS, y - RADIUS,
                    x + RADIUS, y + RADIUS,
                    fill=color, outline="black"
                )

    def click(self, event):
        if self.game_over or self.turn != 0:
            return

        col = event.x // CELL
        if col < 0 or col >= COLS or not can_play(self.mask, col):
            return

        self.make_move(col)
        self.root.after(50, self.ai_move)

    def make_move(self, col):
        board = self.board[self.turn]
        board, self.mask = play(board, self.mask, col)
        self.board[self.turn] = board
        self.moves += 1

        if check_win(board):
            self.draw()
            self.game_over = True
            messagebox.showinfo("Fin de partie", "🟡 Tu as gagné !")
            return

        if self.moves == MAX_MOVES:
            self.draw()
            self.game_over = True
            messagebox.showinfo("Fin de partie", "Match nul")
            return

        self.turn ^= 1
        self.draw()

    def ai_move(self):
        if self.game_over:
            return

        self.info.config(text="L'IA réfléchit...")
        self.root.update()

        col = best_move(
            self.board[0],
            self.board[1],
            self.mask,
            self.turn,
            self.moves
        )

        self.make_move(col)
        self.info.config(text="À toi de jouer 🟡")


# =====================
# LANCEMENT
# =====================

if __name__ == "__main__":
    Connect4GUI()
