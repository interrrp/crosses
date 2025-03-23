from __future__ import annotations

from enum import Enum


class Mark(Enum):
    NONE = "."
    X = "X"
    O = "O"  # noqa: E741

    def __str__(self) -> str:
        return self.value


class Outcome(Enum):
    X_WON = 0
    O_WON = 1
    TIE = 2

    @staticmethod
    def from_mark(mark: Mark) -> Outcome:
        return Outcome.X_WON if mark == Mark.X else Outcome.O_WON


class InvalidUnmarkError(Exception):
    pass


class Board:
    def __init__(self) -> None:
        self._board = [Mark.NONE] * 9
        self._turn = Mark.X

    @property
    def turn(self) -> Mark:
        return self._turn

    @property
    def outcome(self) -> Outcome | None:
        if not any(self.legal_indices):
            return Outcome.TIE

        for row in range(3):
            if self[row, 0] != Mark.NONE and self[row, 0] == self[row, 1] == self[row, 2]:
                return Outcome.from_mark(self[row, 0])

        for col in range(3):
            if self[0, col] != Mark.NONE and self[0, col] == self[1, col] == self[2, col]:
                return Outcome.from_mark(self[0, col])

        if self[0, 0] != Mark.NONE and self[0, 0] == self[1, 1] == self[2, 2]:
            return Outcome.from_mark(self[0, 0])

        if self[0, 2] != Mark.NONE and self[0, 2] == self[1, 1] == self[2, 0]:
            return Outcome.from_mark(self[0, 2])

        return None

    @property
    def legal_indices(self) -> list[int]:
        indices: list[int] = []
        for index, mark in enumerate(self._board):
            if mark == Mark.NONE:
                indices.append(index)
        return indices

    def __getitem__(self, index: int | tuple[int, int]) -> Mark:
        if isinstance(index, tuple):
            row = index[0]
            col = index[1]
            return self._board[row * 3 + col]
        return self._board[index]

    def mark(self, index: int) -> None:
        self._board[index] = self._turn
        self._invert_turn()

    def unmark(self, index: int) -> None:
        if self._board[index] == self._turn:
            raise InvalidUnmarkError

        self._board[index] = Mark.NONE
        self._invert_turn()

    def set_state(self, row_1: str, row_2: str, row_3: str) -> None:
        all_rows = f"{row_1} {row_2} {row_3}".split()
        for index, row in enumerate(all_rows):
            self._board[index] = Mark(row)

    def _invert_turn(self) -> None:
        if self._turn == Mark.X:
            self._turn = Mark.O
        elif self._turn == Mark.O:
            self._turn = Mark.X
