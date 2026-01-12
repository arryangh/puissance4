import math
import time

ROWS = 6
COLS = 7
MAX_DEPTH = 8  # profondeur raisonnable pour performance
MOVE_ORDER = [3, 2, 4, 1, 5, 0, 6]


class Connect4:
    def __init__(self):
        self.board = [0, 0]  # bitboards pour les deux joueurs
        self.mask = 0  # cases occupées
        self.turn = 0  # 0 = joueur, 1 = IA
        self.moves = 0

    def copy(self):
        g = Connect4()
        g.board = self.board[:]
        g.mask = self.mask
        g.turn = self.turn
        g.moves = self.moves
        return g

    def can_play(self, col):
        return (self.mask & (1 << (col * 7 + ROWS - 1))) == 0

    def play(self, col):
        for r in range(ROWS):
            bit = 1 << (col * 7 + r)
            if not (self.mask & bit):
                self.board[self.turn] |= bit
                self.mask |= bit
                self.turn ^= 1
                self.moves += 1
                return True
        return False  # colonne pleine

    def is_win(self, bb):
        # Vertical
        m = bb & (bb >> 1)
        if m & (m >> 2):
            return True
        # Horizontal
        m = bb & (bb >> 7)
        if m & (m >> 14):
            return True
        # Diagonale \
        m = bb & (bb >> 8)
        if m & (m >> 16):
            return True
        # Diagonale /
        m = bb & (bb >> 6)
        if m & (m >> 12):
            return True
        return False

    def is_draw(self):
        return self.moves >= ROWS * COLS

    def winning_move(self, col, turn=None):
        """Vérifie si le joueur turn gagne en jouant col"""
        if turn is None:
            turn = self.turn
        if not self.can_play(col):
            return False
        # trouver où le pion tombera
        for r in range(ROWS):
            bit = 1 << (col * 7 + r)
            if not (self.mask & bit):
                return self.is_win(self.board[turn] | bit)

    def evaluate_position(self):
        score = 0
        current = self.board[self.turn]
        opponent = self.board[self.turn ^ 1]

        # Bonus pour centre
        center_col = 3
        for r in range(ROWS):
            bit = 1 << (center_col * 7 + r)
            if current & bit:
                score += 3
            elif opponent & bit:
                score -= 3

        return score


def negamax(game, depth, alpha, beta):
    opp = game.turn ^ 1
    if game.is_win(game.board[opp]):
        return -(50000 - game.moves)
    if game.is_draw():
        return 0
    if depth == 0:
        return game.evaluate_position()

    # Vérifier les coups gagnants immédiats
    for col in MOVE_ORDER:
        if game.can_play(col) and game.winning_move(col):
            return 50000 - game.moves

    best = -math.inf
    for col in MOVE_ORDER:
        if game.can_play(col):
            child = game.copy()
            child.play(col)
            score = -negamax(child, depth - 1, -beta, -alpha)
            if score > best:
                best = score
            alpha = max(alpha, score)
            if alpha >= beta:
                break
    return best


def best_move(game):
    # Vérifier d'abord les coups gagnants
    for col in MOVE_ORDER:
        if game.can_play(col) and game.winning_move(col):
            return col

    # Bloquer coups gagnants de l'adversaire
    for col in MOVE_ORDER:
        if game.can_play(col) and game.winning_move(col, turn=game.turn ^ 1):
            return col

    # Sinon, chercher meilleur coup via negamax
    best_score = -math.inf
    best_col = None
    for col in MOVE_ORDER:
        if game.can_play(col):
            child = game.copy()
            child.play(col)
            score = -negamax(child, MAX_DEPTH - 1, -math.inf, math.inf)
            if score > best_score:
                best_score = score
                best_col = col
    if best_col is None:
        # fallback
        for col in MOVE_ORDER:
            if game.can_play(col):
                return col
        return 3
    return best_col


def print_board(game):
    grid = [["⚪" for _ in range(COLS)] for _ in range(ROWS)]
    for c in range(COLS):
        for r in range(ROWS):
            bit = 1 << (c * 7 + r)
            if game.board[0] & bit:
                grid[r][c] = "🟡"
            elif game.board[1] & bit:
                grid[r][c] = "🔴"

    for row in reversed(grid):
        print("  " + " ".join(row))
    print("  0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣\n")


def play_game():
    game = Connect4()
    print("Qui commence? (0 = Toi 🟡, 1 = IA 🔴)")
    try:
        starter = int(input())
        if starter == 1:
            game.turn = 1
    except:
        pass

    while True:
        print_board(game)

        if game.turn == 0:
            try:
                col = int(input("Ton coup (0-6): "))
                if col < 0 or col >= COLS or not game.can_play(col):
                    print("Coup invalide - colonne pleine ou hors limites")
                    continue
            except ValueError:
                print("Entrée invalide")
                continue
        else:
            start = time.time()
            col = best_move(game)
            print(f"IA joue colonne {col} ({time.time() - start:.2f}s)")

        game.play(col)

        if game.is_win(game.board[game.turn ^ 1]):
            print_board(game)
            winner = "🟡 Toi" if game.turn == 1 else "🔴 IA"
            print(f"Victoire de {winner}!")
            break

        if game.is_draw():
            print_board(game)
            print("Match nul!")
            break


if __name__ == "__main__":
    play_game()
