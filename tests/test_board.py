import pytest

from crosses.board import Board, InvalidUnmarkError, Mark, Outcome


def test_board_is_initialized_empty() -> None:
    board = Board()
    for index in range(9):
        assert board[index] == Mark.NONE


def test_board_marks_and_unmarks_squares() -> None:
    board = Board()
    assert board[0] == Mark.NONE
    assert board.turn == Mark.X
    board.mark(0)
    assert board[0] == Mark.X
    assert board.turn == Mark.O
    board.unmark(0)
    assert board[0] == Mark.NONE
    assert board.turn == Mark.X


def test_board_invalid_unmark() -> None:
    board = Board()
    board.mark(0)
    board.mark(1)
    with pytest.raises(InvalidUnmarkError):
        board.unmark(0)


def test_board_determines_no_outcome() -> None:
    board = Board()
    assert board.outcome is None


def test_board_determines_winner() -> None:
    board = Board()

    board.set_str(
        "X . .",
        ". X .",
        ". . X",
    )
    assert board.outcome == Outcome.X_WON

    board.set_str(
        ". . O",
        ". O .",
        "O . .",
    )
    assert board.outcome == Outcome.O_WON


def test_board_determines_tie() -> None:
    board = Board()
    board.set_str(
        "X O X",
        "O X O",
        "X O X",
    )
    assert board.outcome == Outcome.TIE
