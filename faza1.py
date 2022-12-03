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
    EMPTY = '[ ]'
    VERTICAL = Fore.BLUE + '[x]' + Style.RESET_ALL
    HORIZONTAL = Fore.RED + '[*]' + Style.RESET_ALL


class Player(Enum):
    HUMAN = True
    AI = False


Move = tuple[int, int]


class State(NamedTuple):
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
    Potezi koji su odigrani vertikalnom pločicom.
    """
    v_played_moves: set[Move]
    """
    Potezi koji su odigrani horizontalnom pločicom.
    """
    h_played_moves: set[Move]
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

    v_possible_moves: set[Move] = {
        (i, j) for j in range(m) for i in range(1, n)
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


def is_game_over(state: State) -> bool:
    """
    Igra je završena ako igrač koji je na potezu nema preostalih poteza.
    """
    return (len(state.v_possible_moves) == 0 and state.to_move == Turn.VERTICAL) \
        or (len(state.h_possible_moves) == 0 and state.to_move == Turn.HORIZONTAL)


def print_state(state: State) -> None:
    (n, m, *_) = state
    output_arr = list[str]()

    row_output = ["    ".rjust(1 if n > 0 else 0)] + \
        [f"  {chr(ord('A')+x)}" for x in range(0, m)] + ["\n"]

    output_arr.extend(row_output)
    for i in range(n-1, -1, -1):
        output_arr.append(f" {i+1} ".rjust(5))
        for j in range(m):
            square = Square.EMPTY

            if (i+1, j) in state.v_played_moves:
                square = Square.VERTICAL
            if (i, j-1) in state.h_played_moves:
                square = Square.HORIZONTAL
            if (i, j) in state.h_played_moves:
                square = Square.HORIZONTAL
            if (i, j) in state.v_played_moves:
                square = Square.VERTICAL

            output_arr.append(f"{square.value}")
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


def game_loop() -> None:
    n, m = input_board_dimensions()
    initial_turn = input_move_order()
    player1 = input_player_type()
    player2 = input_player_type()

    print_state(create_initial_state(n, m, initial_turn))

    return None


if __name__ == "__main__":
    game_loop()
