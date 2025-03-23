# ruff: noqa: T201, PLR2004 Allow prints and constants


from crosses.board import Board, InvalidMarkError, Mark, Outcome
from crosses.engine import engine_mark

RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RESET = "\033[0m"


def main() -> None:
    board = Board(width=4, height=4)
    error = ""

    engine_mark(board)

    while True:
        clear_screen()
        print_board(board)

        print()
        if error:
            print(f"{RED}{error}{RESET}")

        try:
            index = int(input())
            board.mark(index - 1)
            if board.outcome:
                handle_outcome(board)
                break

            engine_mark(board)
            if board.outcome:
                handle_outcome(board)
                break

            error = ""
        except InvalidMarkError:
            error = "Invalid mark!"


def clear_screen() -> None:
    print("\033c", end="")


def handle_outcome(board: Board) -> None:
    clear_screen()
    print_board(board)
    if board.outcome == Outcome.X_WON:
        print(f"{RED}X won!{RESET}")
    elif board.outcome == Outcome.O_WON:
        print(f"{BLUE}O won!{RESET}")
    elif board.outcome == Outcome.TIE:
        print(f"{YELLOW}Tie!{RESET}")


def print_board(board: Board) -> None:
    n_pad = len(str(board.width * board.height))

    for index, mark in board:
        if mark == Mark.X:
            print(f"{RED}{'X':X>{n_pad}}{RESET} ", end="")
        elif mark == Mark.O:
            print(f"{BLUE}{'O':O>{n_pad}}{RESET} ", end="")
        else:
            print(f"{GRAY}{str(index + 1).zfill(n_pad)}{RESET} ", end="")

        if (index + 1) % board.width == 0:
            print()


if __name__ == "__main__":
    main()
