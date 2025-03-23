# ruff: noqa: T201 Allow prints

from crosses.board import Board, InvalidMarkError, Mark, Outcome
from crosses.engine import engine_mark

RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RESET = "\033[0m"


def main() -> None:
    board = Board()
    error = ""

    while True:
        clear_screen()
        print_board(board)

        if board.outcome == Outcome.X_WON:
            print(f"{RED}X won!{RESET}")
            break
        if board.outcome == Outcome.O_WON:
            print(f"{BLUE}O won!{RESET}")
            break
        if board.outcome == Outcome.TIE:
            print(f"{YELLOW}Tie!{RESET}")
            break

        print()
        if error:
            print(f"{RED}{error}{RESET}")

        index = int(input())
        try:
            board.mark(index - 1)
            engine_mark(board)
            error = ""
        except InvalidMarkError:
            error = "Invalid mark!"


def clear_screen() -> None:
    print("\033c", end="")


def print_board(board: Board) -> None:
    for index in range(9):
        mark = board[index]

        if mark == Mark.X:
            print(f"{RED}{mark}{RESET} ", end="")
        elif mark == Mark.O:
            print(f"{BLUE}{mark}{RESET} ", end="")
        else:
            print(f"{GRAY}{index + 1}{RESET} ", end="")

        if (index + 1) % 3 == 0:
            print()


if __name__ == "__main__":
    main()
