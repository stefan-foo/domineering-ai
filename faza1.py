from colorama import Fore,  Style
from enum import Enum
from typing import NamedTuple
import re


move_matcher = re.compile(
    r'\[?(?P<xcord>\d+)(?:[, ])*(?P<ycord>[a-zA-Z])\]?')


class Turn(Enum):
    VERTICAL = True,
    HORIZONTAL = False


class Square(Enum):
    EMPTY = ' '
    VERTICAL = 'x'
    HORIZONTAL = '*'


class Player(Enum):
    HUMAN = True
    AI = False


Move = tuple[int, int]


class State():
    def __init__(self,
                 n: int,
                 m: int,
                 board: list[list[int]],
                 v_possible_moves: set[Move],
                 h_possible_moves: set[Move],
                 to_move: Turn):
        self.n = n
        self.m = m
        self.board = board
        self.v_possible_moves = v_possible_moves
        self.h_possible_moves = h_possible_moves
        self.to_move = to_move

    """
    Stanje table.
    """
    """
    Broj vrsta na tabli.
    """
    n: int
    """
    Broj kolona na tabli.
    """
    m: int
    """
    Matricna reprezentacija table
    """
    board: list[list[int]]
    """
    Mogući sledeći potezi za vertikalnu pločicu.
    """
    v_possible_moves: set[Move]
    """
    Mogući sledeći potezi za horizontalnu pločicu.
    """
    h_possible_moves: set[Move]
    """
    Igrač čiji je sledeći potez.
    """
    to_move: Turn


def input_board_dimensions() -> tuple[int, int]:
    """Korisnički unos dimenzija table."""

    n = m = 0
    while not 1 <= n <= 16:
        n = int(input("Enter number of rows: "))

    while not 1 <= m <= 16:
        m = int(input("Enter number of columns: "))

    return (n, m)


def create_initial_state(n: int = 8, m: int = 8, initial_to_move: Turn = Turn.VERTICAL) -> State:
    """
    Inicijalizuje skupove validnih i odigranih poteza za obe vrste pločice.
    """
    if n < 1 or m < 1:
        raise Exception("Invalid board dimensions")

    v_possible_moves: set[Move] = set({
        (i, j) for j in range(m) for i in range(1, n)
    })
    h_possible_moves: set[Move] = set({
        (i, j) for j in range(m-1) for i in range(n)
    })

    board = [[0 for _ in range(m)] for _ in range(n)]

    return State(n, m, board, v_possible_moves, h_possible_moves, initial_to_move)


def parse_move(move: str) -> Move | None:
    result = move_matcher.search(move)
    return (
        int(result.group('xcord'))-1,
        int(ord(result.group('ycord').upper()))-ord('A')) if result else None


def is_valid_move(state: State, move: Move) -> bool:
    """
    Potez je validan ako je u skupu sa validnim potezima za odgovarajuću pločicu.
    """
    return move in (state.h_possible_moves if state.to_move is Turn.HORIZONTAL else state.v_possible_moves)


def is_valid_move_on_board(board: list[list[int]], move: Move, to_move: Turn) -> bool:
    n, m = len(board), len(board[0])

    x, y = move
    if to_move is Turn.VERTICAL:
        return x >= 1 and y >= 0 and x < n and y < m and board[x][y] == 0 and board[x-1][y] == 0
    else:
        return x >= 0 and y >= 0 and x < n and y < m-1 and board[x][y] == 0 and board[x][y+1] == 0


def is_game_over(state: State) -> bool:
    """
    Igra je završena ako igrač koji je na potezu nema preostalih poteza.
    """
    return (len(state.v_possible_moves) == 0 and state.to_move == Turn.VERTICAL) \
        or (len(state.h_possible_moves) == 0 and state.to_move == Turn.HORIZONTAL)


def print_state(state: State) -> None:
    n = state.n
    m = state.m
    output_arr = list[str]()

    row_output = ["    ".rjust(1 if n > 0 else 0)] + \
        [f"  {chr(ord('A')+x)}" for x in range(0, m)] + ["\n"]

    output_arr.extend(row_output)
    for i in range(n-1, -1, -1):
        output_arr.append(f" {i+1} ".rjust(5))
        for j in range(m):
            if state.board[i][j] == 1:  # HORIZONTAL
                output_arr.append(Fore.BLUE)
                output_arr.append(f"[x]")
            elif state.board[i][j] == 2:  # VERTICAL
                output_arr.append(Fore.RED)
                output_arr.append(f"[*]")
            else:
                output_arr.append(f"[ ]")
            output_arr.append(Style.RESET_ALL)
        output_arr.append(f" {i+1} ")
        output_arr.append("\n")
    output_arr.extend(row_output)

    if is_game_over(state):
        output_arr.append(
            f"{'VERTICAL' if state.to_move is Turn.HORIZONTAL else 'HORIZONTAL'} WON\n")
    else:
        output_arr.append(
            f"{'VERTICAL' if state.to_move is Turn.VERTICAL else 'HORIZONTAL'} to move\n")

    print(str.join("", output_arr))


def input_move(to_move: Turn) -> Move | None:
    """Korisnički unos poteza."""

    move: str = input(
        f"[{'VERTICAL' if to_move is Turn.VERTICAL else 'HORIZONTAL'}] enter move: ")
    return parse_move(move)


def input_player_type(prompt: str = "") -> Player:
    choice = 0
    while not 1 <= choice <= 2:
        choice = int(input(f"{prompt}[HUMAN] - 1 / [AI] - 2: "))
    return Player.HUMAN if choice == 1 else Player.AI


def input_move_order() -> Turn:
    choice = 0
    while not 1 <= choice <= 2:
        choice = int(input(
            f"First to move {Fore.BLUE}[VERTICAL]{Style.RESET_ALL} - 1 / {Fore.RED}[HORIZONTAL]{Style.RESET_ALL} - 2: "))
    return Turn.VERTICAL if choice == 1 else Turn.HORIZONTAL
