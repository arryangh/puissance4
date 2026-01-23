import os
import time
import pickle
from numba import njit

# =====================
# PARAMÈTRES
# =====================

BOOK_MAX_TIME = 600          # 10 minutes
BOOK_MAX_PLIES = 10
OUT_FILE = "opening_book.bin"

CHECKPOINT_INTERVAL = 10     # sauvegarde toutes les 10 secondes

BOOK = {}
nodes = 0
last_print = 0
last_save = 0


# =====================
# CONSTANTES IA
# =====================

ROWS = 6
COLS = 7
MAX_MOVES = ROWS * COLS
WIN_SCORE = 100000
MAX_DEPTH = 18
MOVE_ORDER = (3, 2, 4, 1, 5, 0, 6)


# =====================
# HASH
# =====================

def position_hash(board0, board1):
    return (board0 * 6364136223846793005 + board1) & 0xFFFFFFFFFFFFFFFF


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
            score = -negamax(opp, b2, m2, depth - 1,
                             -beta, -alpha, moves + 1)
            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
    return best


def best_move(board0, board1, mask, turn, moves):
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
            score = -negamax(
                opp, b2, m2,
                MAX_DEPTH - 1,
                -WIN_SCORE, WIN_SCORE,
                moves + 1
            )
            if score > best_score:
                best_score = score
                best_col = col

    return best_col


# =====================
# CHECKPOINT SAFE
# =====================

def save_book():
    tmp = OUT_FILE + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump(BOOK, f)
    os.replace(tmp, OUT_FILE)  # écriture atomique


# =====================
# PROGRESS BAR
# =====================

def show_progress(start_time):
    global last_print

    now = time.time()
    if now - last_print < 1:
        return

    elapsed = now - start_time
    ratio = min(elapsed / BOOK_MAX_TIME, 1.0)

    bar_len = 30
    filled = int(bar_len * ratio)
    bar = "█" * filled + "░" * (bar_len - filled)

    speed = nodes / elapsed if elapsed > 0 else 0

    print(
        f"\r[{bar}] {elapsed:4.0f}s | "
        f"{nodes:7d} pos | "
        f"{speed:6.0f} pos/s",
        end="",
        flush=True
    )

    last_print = now


# =====================
# GÉNÉRATION
# =====================

def generate(board0, board1, mask, turn, moves, start_time):
    global nodes, last_save

    if moves >= BOOK_MAX_PLIES:
        return
    if time.time() - start_time > BOOK_MAX_TIME:
        return

    h = position_hash(board0, board1)

    if h not in BOOK:
        BOOK[h] = best_move(board0, board1, mask, turn, moves)
        nodes += 1

        now = time.time()
        if now - last_save >= CHECKPOINT_INTERVAL:
            save_book()
            last_save = now

        show_progress(start_time)

    for c in range(COLS):
        if can_play(mask, c):
            b = board0 if turn == 0 else board1
            b2, m2 = play(b, mask, c)

            if turn == 0:
                generate(b2, board1, m2, 1, moves + 1, start_time)
            else:
                generate(board0, b2, m2, 0, moves + 1, start_time)



# =====================
# MAIN
# =====================

def main():
    global last_save

    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, "rb") as f:
            BOOK.update(pickle.load(f))
        print(f"Book existant chargé : {len(BOOK)} positions")

    last_save = time.time()
    start = time.time()

    print("Génération du opening book...\n")

    generate(0, 0, 0, 0, 0, start)

    save_book()

    elapsed = time.time() - start
    print("\n\nTerminé")
    print(f"Temps total : {elapsed:.1f}s")
    print(f"Positions : {len(BOOK)}")
    print("Book sauvegardé :", OUT_FILE)


if __name__ == "__main__":
    main()
