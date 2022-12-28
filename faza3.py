from functools import lru_cache
import itertools
import time
from faza1 import *
from faza2 import derive_state, generate_possible_states, input_valid_move


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


# @lru_cache(maxsize=16*1024)
def evaluate_state(state: State) -> int:
    if is_game_over(state):
        return 100 if state.to_move is Turn.HORIZONTAL else -100

    (v_safe_moves, h_safe_moves) = derive_isolated_moves(state)
    return 2*len(state.v_possible_moves) + 3*len(v_safe_moves) - (2*len(state.h_possible_moves) + 3*len(h_safe_moves))


TIME_LIMIT = 2  # seconds
MIN_DEPTH = 4

cutoffs_per_level = {}
visited_nodes_count = 0


def alfabeta_iterative_deepening(state: State, time_at_start: float) -> tuple[Move, int]:
    current_depth = 1
    if state.to_move is Turn.VERTICAL:
        best_move = ((-1, -1), -1001)
    else:
        best_move = ((-1, -1), 1001)

    while True:
        print("Called with depth", current_depth)
        if state.to_move is Turn.VERTICAL:
            best_move = alfabeta(
                state, current_depth, best_move[1], 1001, time_at_start)
        else:
            best_move = alfabeta(
                state, current_depth, -1001, best_move[1], time_at_start)

        if time.time() - time_at_start > TIME_LIMIT:
            break
        current_depth += 1

    return best_move


killer_moves = dict[int, Move]()


def alfabeta(state: State, depth: int, alpha: float, beta: float, time_at_start: float) -> tuple[Move, int]:
    global cutoffs_per_level, visited_nodes_count
    visited_nodes_count += 1

    if time.time() - time_at_start > 1.5*TIME_LIMIT or depth == 0 or is_game_over(state):
        return ((-1, -1), evaluate_state(state))

    if state.to_move is Turn.VERTICAL:
        best_move = ((-1, -1), -1001)

        resulting_iter = generate_possible_states(state)
        if depth in killer_moves:
            killer_move = killer_moves[depth]
            killer_state = derive_state(state, killer_moves[depth])

            prepend = (killer_state, killer_move)
            resulting_iter = itertools.chain((prepend,), generate_possible_states(state))

        for child_state, move in resulting_iter:
            if (child_state):
                candidate = alfabeta(child_state, depth - 1, alpha, beta, time_at_start)
                if candidate[1] > best_move[1]:
                    best_move = (move, candidate[1])
                alpha = max(alpha, best_move[1])
                if alpha >= beta:
                    if depth in cutoffs_per_level:
                        cutoffs_per_level[depth] += 1
                    else:
                        cutoffs_per_level[depth] = 0
                    break
    else:
        best_move = ((-1, -1), 1001)

        resulting_iter = generate_possible_states(state)
        if depth in killer_moves:
            killer_move = killer_moves[depth]
            killer_state = derive_state(state, killer_moves[depth])

            prepend = (killer_state, killer_move)
            resulting_iter = itertools.chain(
                (prepend,), generate_possible_states(state))

        for child_state, move in resulting_iter:
            if (child_state):
                (candidate) = alfabeta(child_state, depth - 1, alpha, beta, time_at_start)
                if candidate[1] < best_move[1]:
                    best_move = (move, candidate[1])
                beta = min(beta, best_move[1])
                if alpha >= beta:
                    if depth in cutoffs_per_level:
                        cutoffs_per_level[depth] += 1
                    else:
                        cutoffs_per_level[depth] = 0
                    break

    killer_moves[depth] = best_move[0]
    return best_move


def dynamic_depth(state: State) -> int:
    res = 1 / (len(state.h_possible_moves) + len(state.v_possible_moves)) * state.n * state.m + 8 - (state.n + state.m) / 4
    return max(int(res), MIN_DEPTH)


def game_loop(n: int, m: int, player1: Player, player2: Player, first_to_move: Turn) -> None:
    game_state = create_initial_state(n, m, first_to_move)

    to_move, next_to_move = player1, player2

    print_state(game_state)
    while not is_game_over(game_state):
        start_time = time.time()

        if to_move == Player.AI:
            depth = MIN_DEPTH  # dynamic_depth(game_state)
            # print("Chosen depth: ", depth)
            # move, _ = alfabeta(game_state, MIN_DEPTH, -
            #                    math.inf, math.inf, start_time)
            move, _ = alfabeta_iterative_deepening(game_state, start_time)
        else:
            move = input_valid_move(game_state)

        new_state = derive_state(game_state, move)
        if new_state:
            game_state = new_state
            to_move, next_to_move = next_to_move, to_move

        global cutoffs_per_level, visited_nodes_count

        print_state(game_state)
        print("Time to move: ", int(time.time() - start_time), "s")
        print("Visited ", visited_nodes_count, " nodes")
        print("Cutoffs: ", cutoffs_per_level)
        # print(evaluate_state.cache_info())
        # evaluate_state.cache_clear()
        visited_nodes_count = 0
        cutoffs_per_level = {}


if __name__ == "__main__":
    full_game_time = time.time()
    game_loop(8, 8, Player.AI, Player.AI, Turn.VERTICAL)
    print("Full game time: ", int(time.time() - full_game_time), "s")
