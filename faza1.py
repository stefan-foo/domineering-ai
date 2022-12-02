from colorama import Fore,  Style
from enum import Enum
from typing import NamedTuple
import re


move_matcher = re.compile(
    r'\[?(?P<xcord>\d+)(?:[, ])*(?P<ycord>[a-zA-Z])\]?')


class Player(Enum):
    VERTICAL = True,
    HORIZONTAL = False


class Square(Enum):
    EMPTY = Fore.WHITE + '[ ]'
    VERTICAL = Fore.BLUE + '[x]'
    HORIZONTAL = Fore.RED + '[*]'


Move = tuple[int, int]


class State(NamedTuple):
    """
    Stanje table.
    """
    n: int
    """
    Broj vrsta na tabli.
    """
    m: int
    """
    Broj kolona na tabli.
    """
    v_played_moves: set[Move]
    """
    Potezi koji su odigrani vertikalnom pločicom.
    """
    h_played_moves: set[Move]
    """
    Potezi koji su odigrani horizontalnom pločicom.
    """
    v_possible_moves: set[Move]
    """
    Mogući sledeći potezi za vertikalnu pločicu.
    """
    h_possible_moves: set[Move]
    """
    Mogući sledeći potezi za horizontalnu pločicu.
    """
    to_move: Player
    """
    Igrač čiji je sledeći potez.
    """


def input_board_dimensions() -> Move:
    """Korisnički unos dimenzija table."""

    n = m = 0
    while not 1 <= n <= 16:
        n = int(input("Enter number of rows:"))

    while not 1 <= m <= 16:
        m = int(input("Enter number of columns:"))

    return (n, m)


def create_initial_state(n: int = 8, m: int = 8, initial_to_move=Player.VERTICAL) -> State:
    """
        Inicijalizuje skupove validnih i odigranih poteza za obe vrste pločice.
    """
    if n < 1 or m < 1:
        raise Exception("Invalid board dimensions")

    v_possible_moves: set[Move] = {
        (i, j) for j in range(m) for i in range(n-1)
    }
    h_possible_moves: set[Move] = {
        (i, j) for j in range(m-1) for i in range(n)
    }

    v_played_moves = set[Move]()
    h_played_moves = set[Move]()

    return State(n, m,
                 v_played_moves, h_played_moves,
                 v_possible_moves, h_possible_moves,
                 initial_to_move)


def is_game_over(state: State) -> bool:
    """
    Igra je završena ako igrač koji je na potezu nema preostalih poteza.
    """
    return (len(state.v_possible_moves) == 0 and state.to_move == Player.VERTICAL) \
        or (len(state.h_possible_moves) == 0 and state.to_move == Player.HORIZONTAL)


def print_state(state: State) -> None:
    """Štampa tablu na standardni izlaz."""

    (n, m, *_) = state
    output_arr = list[str]()

    output_arr.append("   A")
    output_arr.extend([f"  {chr(ord('A')+x)}" for x in range(1, m)])
    output_arr.append("\n")
    for i in range(n):
        output_arr.append(f"{i+1} ")
        for j in range(m):
            square = Square.EMPTY

            if (i-1, j) in state.v_played_moves:
                square = Square.VERTICAL
            if (i, j-1) in state.h_played_moves:
                square = Square.HORIZONTAL
            if (i, j) in state.h_played_moves:
                square = Square.HORIZONTAL
            if (i, j) in state.v_played_moves:
                square = Square.VERTICAL

            output_arr.append(f"{square.value}")
        output_arr.append(f" {i+1}")
        output_arr.append("\n")
    output_arr.append("   A")
    output_arr.extend([f"  {chr(ord('A')+x)}" for x in range(1, m)])
    output_arr.append("\n")
    print(str.join("", output_arr), flush=True)

    print(Style.RESET_ALL)
    print("V left moves:", len(state.v_possible_moves),
          "\nH left moves:", len(state.h_possible_moves),
          "\nV played moves:",  len(state.v_played_moves),
          "\nH played moves", len(state.h_played_moves), flush=True)


def parse_move(move: str) -> None | Move:
    result = move_matcher.search(move)
    return (
        int(result.group('xcord'))-1,
        int(ord(result.group('ycord').upper()))-ord('A')) if result else None


def input_move(to_move: Player) -> Move | None:
    """Korisnički unos poteza."""

    move: str = input(
        f"[{'VERTICAL' if to_move is Player.VERTICAL else 'HORIZONTAL'}] enter move: ")
    return parse_move(move)


def is_valid_move(state: State, move: Move) -> bool:
    """
    Potez je validan ako je u skupu sa validnim potezima za odgovarajuću pločicu.
    """
    return move in (state.h_possible_moves if state.to_move is Player.HORIZONTAL else state.v_possible_moves)
