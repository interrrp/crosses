from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class Mark(Enum):
    NONE = "."
    X = "X"
    O = "O"  # noqa: E741

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Outcome(Enum):
    X_WON = 0
    O_WON = 1
    TIE = 2

    @staticmethod
    def from_mark(mark: Mark) -> Outcome:
        return Outcome.X_WON if mark == Mark.X else Outcome.O_WON


class InvalidMarkError(Exception):
    pass


class InvalidUnmarkError(Exception):
    pass


class Board:
    def __init__(self, *, width: int = 3, height: int = 3, cross_length: int = 3) -> None:
        self._width = width
        self._height = height
        self._cross_length = cross_length
        self._board = [Mark.NONE] * (width * height)
        self._turn = Mark.X

    @property
    def turn(self) -> Mark:
        return self._turn

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def __iter__(self) -> Generator[tuple[int, Mark]]:
        yield from enumerate(self._board)

    @property
    def outcome(self) -> Outcome | None:
        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal down-right
            (1, -1),  # Diagonal down-left
        ]

        for row in range(self._height):
            for col in range(self._width):
                mark = self[row, col]
                if mark == Mark.NONE:
                    continue

                for dr, dc in directions:
                    if (
                        row + (self._cross_length - 1) * dr >= self._height
                        or col + (self._cross_length - 1) * dc >= self._width
                        or col + (self._cross_length - 1) * dc < 0
                    ):
                        continue

                    win = True
                    for i in range(1, self._cross_length):
                        if self[row + i * dr, col + i * dc] != mark:
                            win = False
                            break

                    if win:
                        return Outcome.from_mark(mark)

        if not any(self.legal_indices):
            return Outcome.TIE

        return None

    @property
    def legal_indices(self) -> list[int]:
        indices: list[int] = []
        for index, mark in self:
            if mark == Mark.NONE:
                indices.append(index)
        return indices

    def __getitem__(self, index: int | tuple[int, int]) -> Mark:
        if isinstance(index, tuple):
            row = index[0]
            col = index[1]
            return self._board[row * self._width + col]
        return self._board[index]

    def mark(self, index: int) -> None:
        if self._board[index] != Mark.NONE:
            raise InvalidMarkError

        self._board[index] = self._turn
        self._invert_turn()

    def unmark(self, index: int) -> None:
        if self._board[index] == self._turn:
            raise InvalidUnmarkError

        self._board[index] = Mark.NONE
        self._invert_turn()

    def set_str(self, *rows: str) -> None:
        all_rows = " ".join(rows).split()
        for index, row in enumerate(all_rows):
            self._board[index] = Mark(row)

    def _invert_turn(self) -> None:
        if self._turn == Mark.X:
            self._turn = Mark.O
        elif self._turn == Mark.O:
            self._turn = Mark.X
