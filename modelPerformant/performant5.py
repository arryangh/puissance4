import time
from numba import njit

ROWS = 6
COLS = 7
MAX_MOVES = ROWS * COLS
WIN_SCORE = 100000
MOVE_ORDER = (3, 2, 4, 1, 5, 0, 6)

# =========================
# BITBOARD CORE
# =========================

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


# =========================
# NEGAMAX ULTRA RAPIDE
# =========================

@njit
def negamax(board, opp, mask, depth, alpha, beta, moves):
    if check_win(opp):
        return -(WIN_SCORE - moves)

    if moves == MAX_MOVES:
        return 0

    if depth == 0:
        return evaluate(board, opp)

    # win immédiat
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


# =========================
# BEST MOVE
# =========================

def best_move(board0, board1, mask, turn, moves, depth):
    board = board0 if turn == 0 else board1
    opp = board1 if turn == 0 else board0

    # victoire immédiate
    for col in MOVE_ORDER:
        if can_play(mask, col) and winning_move(board, mask, col):
            return col

    # blocage immédiat
    for col in MOVE_ORDER:
        if can_play(mask, col) and winning_move(opp, mask, col):
            return col

    best_score = -WIN_SCORE
    best_col = 3

    for col in MOVE_ORDER:
        if can_play(mask, col):
            b2, m2 = play(board, mask, col)
            score = -negamax(opp, b2, m2, depth - 1, -WIN_SCORE, WIN_SCORE, moves + 1)
            if score > best_score:
                best_score = score
                best_col = col

    return best_col
