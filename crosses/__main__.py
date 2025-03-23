# ruff: noqa: T201, PLR2004 Allow prints and constants


from crosses.board import Board, InvalidMarkError, Mark, Outcome

RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RESET = "\033[0m"


def main() -> None:
    board = Board(width=20, height=20)
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
            error = ""
        except InvalidMarkError:
            error = "Invalid mark!"


def clear_screen() -> None:
    print("\033c", end="")


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
