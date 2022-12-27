from functools import lru_cache
import math
from faza1 import *
from faza2 import derive_state, input_valid_move


class PlayingMode(Enum):
    PLAYER_VS_PLAYER = 0,
    PLAYER_VS_AI = 1,
    AI_VS_AI = 2


def derive_isolated_moves(state: State) -> tuple[set[Move], set[Move]]:
    v_isolated_moves = {
        (x, y) for (x, y) in state.v_possible_moves
        if (x, y) not in state.h_possible_moves
        and (x-1, y) not in state.h_possible_moves
        and (x, y-1) not in state.h_possible_moves
        and (x-1, y-1) not in state.h_possible_moves}

    h_isolated_moves = {
        (x, y) for (x, y) in state.h_possible_moves
        if (x, y) not in state.v_possible_moves
        and (x, y+1) not in state.v_possible_moves
        and (x+1, y) not in state.v_possible_moves
        and (x+1, y+1) not in state.v_possible_moves}

    return (v_isolated_moves, h_isolated_moves)


# @lru_cache(maxsize=256)
def evaluate_state(state: State) -> int:
    if is_game_over(state):
        return 100 if state.to_move is Turn.HORIZONTAL else -100

    (v_safe_moves, h_safe_moves) = derive_isolated_moves(state)
    return 2*len(state.v_possible_moves) + 3*len(v_safe_moves) - (2*len(state.h_possible_moves) + 3*len(h_safe_moves))


cache_hits = 0
iterations = 0


def alfabeta(state: State, depth: int, alpha: float, beta: float, transposition_table: dict[State, int]) -> tuple[Move, int]:
    global iterations
    iterations += 1

    if depth == 0 or is_game_over(state):
        if state in transposition_table:
            global cache_hits
            cache_hits += 1
            return ((-1, -1), transposition_table[state])
        else:
            value = evaluate_state(state)
            transposition_table[state] = value
            return ((-1, -1), value)

    if state.to_move is Turn.VERTICAL:
        best_move = ((-1, -1), -1001)
        for move in state.v_possible_moves:
            child_state = derive_state(state, move)
            if (child_state):
                candidate = alfabeta(child_state, depth - 1,
                                     alpha, beta, transposition_table)
                if candidate[1] > best_move[1]:
                    best_move = (move, candidate[1])
                alpha = max(alpha, best_move[1])
                if alpha >= beta:
                    break
    else:
        best_move = ((-1, -1), 1001)
        for move in state.h_possible_moves:
            child_state = derive_state(state, move)
            if (child_state):
                (candidate) = alfabeta(child_state, depth -
                                       1, alpha, beta, transposition_table)
                if candidate[1] < best_move[1]:
                    best_move = (move, candidate[1])
                beta = min(beta, best_move[1])
                if alpha >= beta:
                    break

    transposition_table[state] = best_move[1]
    return best_move


MIN_DEPTH = 4


def dynamic_depth(state: State) -> int:
    res = 1 / (len(state.h_possible_moves) + len(state.v_possible_moves)
               ) * state.n * state.m + 8 - (state.n + state.m) / 4
    return max(int(res), MIN_DEPTH)


def game_loop(n: int, m: int, player1: Player, player2: Player, first_to_move: Turn) -> None:
    game_state = create_initial_state(n, m, first_to_move)

    to_move, next_to_move = player1, player2

    transposition_table = dict[State, int]()

    print_state(game_state)
    while not is_game_over(game_state):
        if to_move == Player.AI:
            depth = dynamic_depth(game_state)
            print(depth)
            move, _ = alfabeta(game_state, depth, -math.inf,
                               math.inf, transposition_table)
        else:
            move = input_valid_move(game_state)

        new_state = derive_state(game_state, move)
        if new_state:
            game_state = new_state
            to_move, next_to_move = next_to_move, to_move

        print_state(game_state)
        global cache_hits
        global iterations
        print("Cache hits / iterations: ", cache_hits, " / ",
              iterations, " (" + str(int(cache_hits/iterations*100)) + "%)")


if __name__ == "__main__":
    game_loop(10, 10, Player.AI, Player.AI, Turn.VERTICAL)
