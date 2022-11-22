from enum import Enum
from functools import reduce
from typing import NamedTuple
import re

move_matcher = re.compile(r'\[?(?P<xcord>\d+)(?:[, ])+(?P<ycord>[a-zA-Z])\]?')


class Player(Enum):
    VERTICAL = True,
    HORIZONTAL = False


class Square(Enum):
    EMPTY = ' '
    VERTICAL = 'x'
    HORIZONTAL = '*'


class State(NamedTuple):
    board: list[list[Square]]
    to_move: Player


def get_initial_state(n: int = 8, m: int = 8):
    if n < 1 or m < 1:
        raise Exception("Invalid board dimensions")
    return State(board=[[Square.EMPTY for _ in range(m)] for _ in range(n)], to_move=Player.VERTICAL)


def get_move_coords(move: tuple[int, str]) -> tuple[int, int]:
    (x, y_c) = move
    return (x - 1, ord(str.upper(y_c)) - 65)


def try_parse_move(move: str) -> None | tuple[int, str]:
    result = move_matcher.search(move)
    return (int(result.group('xcord')), result.group('ycord')) if result else None


def is_valid_move(state: State, move: tuple[int, str]) -> bool:
    board, to_move = state
    x, y = get_move_coords(move)
    n = len(board)
    m = len(board[0])

    if x < 0 or y < 0 or board[x][y] is not Square.EMPTY:
        return False
    elif to_move is Player.HORIZONTAL:
        return y + 1 < m and x < n and board[x][y + 1] is Square.EMPTY
    else:
        return x + 1 < n and y < m and board[x + 1][y] is Square.EMPTY


def is_game_over(state: State) -> bool:
    board, to_move = state
    n = len(board)
    m = len(board[0])

    if to_move is Player.VERTICAL:
        for i in range(n - 1):
            for j in range(m):
                if board[i][j] is Square.EMPTY and board[i+1][j] is Square.EMPTY:
                    return False
    else:
        for i in range(n):
            for j in range(m - 1):
                if board[i][j] is Square.EMPTY and board[i][j + 1] is Square.EMPTY:
                    return False
    return True


def derive_state(state: State, move: tuple[int, str]) -> State:
    if not is_valid_move(state, move):
        raise Exception("Invalid move")
    board, to_move = state
    x, y = get_move_coords(move)
    new_board = [row[:] for row in board]

    if to_move is Player.HORIZONTAL:
        new_board[x][y] = new_board[x][y+1] = Square.HORIZONTAL
    else:
        new_board[x][y] = new_board[x + 1][y] = Square.VERTICAL

    new_to_move = Player.HORIZONTAL if to_move is Player.VERTICAL else Player.VERTICAL
    return State(board=new_board, to_move=new_to_move)


def print_state(state: State) -> None:
    (board, to_move) = state
    n = len(board)
    m = len(board[0])
    output_arr = []

    for i in range(n):
        for j in range(m):
            output_arr.append(f"[{board[i][j].value}]")
        output_arr.append("\n")
    print(str.join("", output_arr))


game_state = get_initial_state(8, 8)
while not is_game_over(game_state):
    move = input(
        f"[{'VERTICAL' if game_state.to_move is Player.VERTICAL else 'HORIZONTAL'}] enter move: ")
    move = try_parse_move(move)
    if move and is_valid_move(game_state, move):
        game_state = derive_state(game_state, move)
    print_state(game_state)
print(f"{'VERTICAL' if game_state.to_move is Player.HORIZONTAL else 'HORIZONTAL'} WON")
