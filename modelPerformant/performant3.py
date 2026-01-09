import math
import time

ROWS = 6
COLS = 7
MAX_DEPTH = 10
MOVE_ORDER = [3, 2, 4, 1, 5, 0, 6]


class Connect4:
    def __init__(self):
        self.board = [0, 0]
        self.mask = 0
        self.turn = 0
        self.moves = 0

    def copy(self):
        g = Connect4()
        g.board = self.board[:]
        g.mask = self.mask
        g.turn = self.turn
        g.moves = self.moves
        return g

    def can_play(self, col):
        # Vérifie si la case du haut de la colonne est libre
        top = 1 << (col * 7 + ROWS - 1)
        return (self.mask & top) == 0

    def play(self, col):
        # Trouve la première case libre dans la colonne
        for r in range(ROWS):
            bit = 1 << (col * 7 + r)
            if not (self.mask & bit):
                self.board[self.turn] |= bit
                self.mask |= bit
                self.turn ^= 1
                self.moves += 1
                return

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

    def winning_move(self, col):
        """Vérifie si le joueur actuel gagne en jouant dans col"""
        if not self.can_play(col):
            return False

        # Trouver où le pion tombera
        for r in range(ROWS):
            bit = 1 << (col * 7 + r)
            if not (self.mask & bit):
                # Simuler le coup
                test_board = self.board[self.turn] | bit
                return self.is_win(test_board)

    def count_threats(self, bb):
        """Compte le nombre de menaces de victoire (3 alignés avec case libre)"""
        threats = 0

        # Vertical
        m = bb & (bb >> 1) & (bb >> 2)
        threats += bin(m).count('1')

        # Horizontal
        m = bb & (bb >> 7) & (bb >> 14)
        threats += bin(m).count('1')

        # Diagonale \
        m = bb & (bb >> 8) & (bb >> 16)
        threats += bin(m).count('1')

        # Diagonale /
        m = bb & (bb >> 6) & (bb >> 12)
        threats += bin(m).count('1')

        return threats

    def evaluate_position(self):
        """Évaluation heuristique de la position"""
        score = 0
        current = self.board[self.turn]
        opponent = self.board[self.turn ^ 1]

        # Compter les menaces
        score += self.count_threats(current) * 10
        score -= self.count_threats(opponent) * 10

        # Bonus pour contrôle du centre
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

    # Victoire de l'adversaire
    if game.is_win(game.board[opp]):
        return -(50000 - game.moves)

    if game.is_draw():
        return 0

    # Profondeur max atteinte
    if depth == 0:
        return game.evaluate_position()

    # Vérifier les coups gagnants immédiatement
    for col in MOVE_ORDER:
        if game.can_play(col) and game.winning_move(col):
            return 50000 - game.moves

    best = -math.inf

    for col in MOVE_ORDER:
        if game.can_play(col):
            child = game.copy()
            child.play(col)
            score = -negamax(child, depth - 1, -beta, -alpha)
            best = max(best, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break

    return best


def best_move(game):
    best_score = -math.inf
    best_col = None

    # Trouver une colonne jouable par défaut
    for col in MOVE_ORDER:
        if game.can_play(col):
            best_col = col
            break

    if best_col is None:
        return 3  # Fallback

    # Vérifier d'abord les coups gagnants
    for col in MOVE_ORDER:
        if game.can_play(col) and game.winning_move(col):
            return col

    # Bloquer les coups gagnants de l'adversaire
    # On simule que l'adversaire joue et on vérifie s'il peut gagner
    opp_game = game.copy()
    opp_game.turn ^= 1  # Inverser pour simuler le tour de l'adversaire

    for col in range(COLS):
        if opp_game.can_play(col) and opp_game.winning_move(col):
            # L'adversaire peut gagner en jouant ici, on bloque
            return col

    # Sinon, chercher le meilleur coup
    for col in MOVE_ORDER:
        if game.can_play(col):
            child = game.copy()
            child.play(col)
            score = -negamax(child, MAX_DEPTH - 1, -math.inf, math.inf)
            if score > best_score:
                best_score = score
                best_col = col

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
    print("  0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣")
    print()


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