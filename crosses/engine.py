from crosses.board import Board, Mark, Outcome

INF = float("inf")

GOOD_ENDGAMES = [
    (Outcome.X_WON, Mark.X),
    (Outcome.O_WON, Mark.O),
]
BAD_ENDGAMES = [
    (Outcome.X_WON, Mark.O),
    (Outcome.O_WON, Mark.X),
]


def engine_mark(board: Board) -> None:
    best_score = -INF
    best_index = 0

    for index in board.legal_indices:
        board.mark(index)
        score = -1 if _opponent_can_win_next(board) else -_search(board)
        board.unmark(index)

        if score > best_score:
            best_score = score
            best_index = index

    board.mark(best_index)


def _search(board: Board, depth: int = 4, alpha: float = -INF, beta: float = INF) -> float:
    if board.outcome:
        if board.outcome == Outcome.TIE:
            return 0

        endgame = (board.outcome, board.turn)
        if endgame in GOOD_ENDGAMES:
            return 1
        if endgame in BAD_ENDGAMES:
            return -1

    if depth == 0:
        return 0

    for index in board.legal_indices:
        board.mark(index)
        alpha = max(alpha, -_search(board, depth - 1, -beta, -alpha))
        board.unmark(index)

        if alpha > beta:
            break

    return alpha


def _opponent_can_win_next(board: Board) -> bool:
    for index in board.legal_indices:
        board.mark(index)
        if board.outcome and board.outcome != Outcome.TIE:
            board.unmark(index)
            return True
        board.unmark(index)
    return False
