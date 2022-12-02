from functools import lru_cache
from colorama import Fore,  Style
from enum import Enum
import random
from typing import Iterable, NamedTuple
import re
import math


# region Faza I

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
    """Stanje table."""

    n: int
    """Broj vrsta na tabli."""

    m: int
    """Broj kolona na tabli."""

    v_played_moves: set[Move]
    """Potezi koje su odigrani vertikalnom pločicom."""

    h_played_moves: set[Move]
    """Potezi koje su odigrani horizontalnom pločicom."""

    v_possible_moves: set[Move]
    """Mogući sledeći potezi za vertikalnu pločicu."""

    h_possible_moves: set[Move]
    """Mogući sledeći potezi za horizontalnu pločicu."""

    to_move: Player
    """Igrač čiji je sledeći potez."""


def create_initial_state(n: int = 8, m: int = 8, initial_to_move=Player.VERTICAL):
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


def parse_move(move: str) -> None | Move:
    result = move_matcher.search(move)
    return (
        int(result.group('xcord'))-1,
        int(ord(result.group('ycord').upper()))-ord('A')) if result else None


def is_valid_move(state: State, move: Move) -> bool:
    return move in (state.h_possible_moves if state.to_move is Player.HORIZONTAL else state.v_possible_moves)


def is_game_over(state: State) -> bool:
    return (len(state.v_possible_moves) == 0 and state.to_move == Player.VERTICAL) or (
        len(state.h_possible_moves) == 0 and state.to_move == Player.HORIZONTAL)

# endregion Faza I

# region Faza II


V_EFFECTS_TO_H = ((0, 0), (1, 0), (1, -1), (0, -1))
V_EFFECTS_TO_V = ((0, 0), (1, 0), (-1, 0))

H_EFFECTS_TO_H = ((0, 0), (0, 1), (0, -1))
H_EFFECTS_TO_V = ((0, 0), (0, 1), (-1, 0), (-1, 1))


def derive_state(state: State, move: Move) -> None | State:
    if not is_valid_move(state, move):
        return None

    (x, y) = move

    v_possible_moves_copy = state.v_possible_moves.copy()
    h_possible_moves_copy = state.h_possible_moves.copy()

    v_played_moves_copy = state.v_played_moves.copy()
    h_played_moves_copy = state.h_played_moves.copy()

    if state.to_move == Player.VERTICAL:
        effects_to_v = V_EFFECTS_TO_V
        effects_to_h = V_EFFECTS_TO_H

        v_played_moves_copy.add((x, y))

        new_to_move = Player.HORIZONTAL
    else:
        effects_to_v = H_EFFECTS_TO_V
        effects_to_h = H_EFFECTS_TO_H

        h_played_moves_copy.add((x, y))

        new_to_move = Player.VERTICAL

    for cx, cy in effects_to_h:
        px, py = x + cx, y + cy
        if (px, py) in h_possible_moves_copy:
            h_possible_moves_copy.discard((px, py))

    for cx, cy in effects_to_v:
        px, py = x + cx, y + cy
        if (x + cx, y + cy) in v_possible_moves_copy:
            v_possible_moves_copy.discard((px, py))

    return State(
        n=state.n,
        m=state.m,
        v_played_moves=v_played_moves_copy,
        h_played_moves=h_played_moves_copy,
        v_possible_moves=v_possible_moves_copy,
        h_possible_moves=h_possible_moves_copy,
        to_move=new_to_move)


def generate_children(state: State) -> Iterable[State]:
    possible_moves = state.v_possible_moves if state.to_move is Player.VERTICAL else state.h_possible_moves
    for move in possible_moves:
        new_state = derive_state(state, move)
        if new_state is not None:
            yield new_state

# endregion Faza II

# region Faza I


def print_state(state: State) -> None:
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


def input_board_dimensions() -> Move:
    n = m = 0
    while not 1 <= n <= 16:
        n = int(input("Enter number of rows:"))

    while not 1 <= m <= 16:
        m = int(input("Enter number of columns:"))

    return (n, m)


def input_move(to_move: Player) -> Move | None:
    move: str = input(
        f"[{'VERTICAL' if to_move is Player.VERTICAL else 'HORIZONTAL'}] enter move: ")
    return parse_move(move)

# region Faza III


def derive_isolated_moves(state: State) -> tuple[set[Move], set[Move]]:
    v_isolated_moves = {
        (x, y) for (x, y) in state.v_possible_moves
        if (x, y) not in state.h_possible_moves
        and (x+1, y) not in state.h_possible_moves
        and (x, y-1) not in state.h_possible_moves
        and (x+1, y-1) not in state.h_possible_moves}

    h_isolated_moves = {
        (x, y) for (x, y) in state.h_possible_moves
        if (x, y) not in state.v_possible_moves
        and (x, y+1) not in state.v_possible_moves
        and (x-1, y) not in state.v_possible_moves
        and (x-1, y+1) not in state.v_possible_moves}

    return (v_isolated_moves, h_isolated_moves)


def evaluate_state(state: State) -> int:
    if is_game_over(state):
        return 100 if state.to_move is Player.HORIZONTAL else -100

    (v_safe_moves, h_safe_moves) = derive_isolated_moves(state)
    return len(state.v_possible_moves) + len(v_safe_moves) - (len(state.h_possible_moves) + len(h_safe_moves))


# @lru_cache(maxsize=256)
def alfabeta(state: State, depth: int, alpha: float, beta: float) -> tuple[Move | None, int]:
    if depth == 0 or is_game_over(state):
        return ((-1, -1), evaluate_state(state))

    if state.to_move is Player.VERTICAL:
        best_move = (None, -1001)
        for move in state.v_possible_moves:
            child_state = derive_state(state, move)
            if (child_state):
                candidate = alfabeta(child_state,  depth - 1, alpha, beta)
                if candidate[1] > best_move[1]:
                    best_move = (move, candidate[1])
                alpha = max(alpha, best_move[1])
                if alpha >= beta:
                    break
    else:
        best_move = (None, 1001)
        for move in state.h_possible_moves:
            child_state = derive_state(state, move)
            if (child_state):
                (candidate) = alfabeta(child_state, depth - 1, alpha, beta)
                if candidate[1] < best_move[1]:
                    best_move = (move, candidate[1])
                beta = min(beta, best_move[1])
                if alpha >= beta:
                    break
    return best_move


# @lru_cache(maxsize=256)
def negalfabeta(state: State, depth: int, alpha: float, beta: float) -> tuple[Move | None, int]:
    if depth == 0 or is_game_over(state):  # O(1)
        return ((-1, -1), evaluate_state(state))  # najskuplja operacija

    possible_next_moves = state.v_played_moves if state.to_move is Player.VERTICAL else state.h_played_moves

    best_move = (None, -100)
    for next_move in possible_next_moves:
        child_state = derive_state(state, next_move)
        if (child_state):
            (_new_move, new_eval) = negalfabeta(
                child_state,  depth - 1, -alpha, -beta)
            new_eval = -new_eval
            if new_eval > best_move[1]:
                best_move = (next_move, new_eval)
                alpha = max(alpha, new_eval)
                if alpha >= beta:
                    break
    return best_move

# endregion Faza III


TESTING = True


def game_loop() -> None:
    if not TESTING:
        n, m = input_board_dimensions()
    else:
        n, m = 8, 8

    game_state: State = create_initial_state(n, m)

    last_move = None
    eval = 0
    while not is_game_over(game_state):
        print_state(game_state)
        if last_move:
            print(
                f"\nMove played: {(last_move[0] + 1, chr(ord('A') + last_move[1]))} [{eval}]\n")
        if not TESTING:
            move = input_move(game_state.to_move)
            if move:
                new_game_state = derive_state(game_state, move)
                if new_game_state:
                    game_state = new_game_state
                else:
                    print("Invalid move")
            else:
                print("Enter move in format ROW COLUMN")
        else:  # if TESTING
            if (game_state.to_move is Player.VERTICAL):
                move, eval = alfabeta(game_state, 4, -math.inf, math.inf)
            else:
                move, eval = alfabeta(game_state, 4, -math.inf, math.inf)
                # move = input_move(game_state.to_move)

            last_move = move
            if move:
                new_game_state = derive_state(game_state, move)
            else:
                break
            if new_game_state is not None:
                game_state = new_game_state

    last_state = game_state
    alfabeta(last_state, 4, -math.inf, math.inf)
    print_state(game_state)
    print(
        f"{'VERTICAL' if game_state.to_move is Player.HORIZONTAL else 'HORIZONTAL'} WON")


game_loop()

# endregion Faza I

# region Faza III


# @lru_cache(maxsize=256)
def maxmin(state: State, move: Move, depth: int, alpha: float, beta: float) -> tuple[Move, float]:
    if depth == 0 or is_game_over(state):  # O(1)
        return (move, evaluate_state(state))  # najskuplja operacija
    new_state = derive_state(state, move)  # O(1)
    if new_state is None:
        return ((-1, -1), 0)  # invalid

    if new_state.to_move is Player.VERTICAL:
        best_move = ((-1, -1), -math.inf)
        for move in state.v_possible_moves:
            candidate = maxmin(state, move, depth - 1, alpha, beta)
            if candidate[1] > best_move[1]:
                best_move = candidate
            alpha = max(alpha, best_move[1])
            if alpha >= beta:
                break
    else:
        best_move = ((-1, -1), math.inf)
        for move in state.h_possible_moves:
            (candidate) = maxmin(state, move, depth - 1, alpha, beta)
            if candidate[1] < best_move[1]:
                best_move = candidate
            beta = min(beta, best_move[1])
            if alpha >= beta:
                break
    return best_move


# endregion Faza III
