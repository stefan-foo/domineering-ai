import math
from faza1 import *
from faza2 import *
from time import time
from tt import *
from _collections_abc import Callable


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


def evaluate_state(state: State) -> int:
    if is_game_over(state):
        return 300 if state.to_move is Turn.HORIZONTAL else -300

    (v_safe_moves, h_safe_moves) = derive_isolated_moves(state)
    return 2*len(state.v_possible_moves) + 3*len(v_safe_moves) - (2*len(state.h_possible_moves) + 3*len(h_safe_moves))


def weight_state(state: State) -> int:
    if is_game_over(state):
        return 300 if state.to_move is Turn.HORIZONTAL else -300

    return len(state.v_possible_moves) - len(state.h_possible_moves)


def evaluation_function_generator_lc(a: int, b: int, c: int, d: int) -> Callable[[State], int]:
    def evaluate_state(state: State) -> int:
        if is_game_over(state):
            return 300 if state.to_move is Turn.HORIZONTAL else -300

        (v_safe_moves, h_safe_moves) = derive_isolated_moves(state)
        return a*len(state.v_possible_moves) + b*len(v_safe_moves) - (c*len(state.h_possible_moves) + d*len(h_safe_moves))
    return evaluate_state


tt_cutoff = 0
ab_cutoff = 0

ENABLE_TT = True


def alfabeta(state: State, depth: int, alpha: float, beta: float, evaluation_function: Callable[[State], int], tt: TranspositionTable) -> tuple[Move, int]:
    if depth == 0 or is_game_over(state):
        value = evaluation_function(state)
        return ((-1, -1), value)

    global ab_cutoff
    if ENABLE_TT:
        global tt_cutoff

        tt_val = tt.retrieve(state.board)
        if tt_val is not None:
            tt_move, tt_depth = tt_val
            if depth <= tt_depth:
                tt_cutoff += 1
                return tt_move

    if state.to_move is Turn.VERTICAL:
        best_move = ((-1, -1), -1001)

        sorted_moves = []
        for move in set(state.v_possible_moves):
            modify_state(state, move)

            # tt_val = tt.retrieve(state.board)
            move_eval = weight_state(state)

            undo_move(state, move)

            sorted_moves.append((move_eval, move))
        sorted_moves.sort(reverse=True)

        for _, move in sorted_moves:
            # for move in set(state.v_possible_moves):
            child_state = modify_state(state, move)
            if (child_state):
                candidate = alfabeta(child_state, depth - 1,
                                     alpha, beta, evaluation_function, tt)
                if candidate[1] > best_move[1]:
                    best_move = (move, candidate[1])
                alpha = max(alpha, best_move[1])
                if alpha >= beta:
                    undo_move(state, move)

                    # global ab_cutoff
                    ab_cutoff += 1
                    break
            undo_move(state, move)
    else:
        best_move = ((-1, -1), 1001)

        sorted_moves = []
        for move in set(state.h_possible_moves):
            modify_state(state, move)

            # tt_val = tt.retrieve(state.board)
            move_eval = weight_state(state)

            undo_move(state, move)

            sorted_moves.append((move_eval, move))
        sorted_moves.sort()

        for _, move in sorted_moves:
            # for move in set(state.h_possible_moves):
            child_state = modify_state(state, move)
            # child_state = derive_state(state, move)
            if (child_state):
                candidate = alfabeta(child_state, depth -
                                     1, alpha, beta,  evaluation_function, tt)
                if candidate[1] < best_move[1]:
                    best_move = (move, candidate[1])
                beta = min(beta, best_move[1])
                if alpha >= beta:
                    undo_move(state, move)

                    # global ab_cutoff
                    ab_cutoff += 1
                    break
            undo_move(state, move)

    if ENABLE_TT:
        tt.store(state.board, best_move, depth)

    return best_move


MIN_DEPTH = 5


def dynamic_depth(state: State) -> int:
    res = 1 / (len(state.h_possible_moves) + len(state.v_possible_moves)
               ) * state.n * state.m + 8 - (state.n + state.m) / 4
    return max(int(res), MIN_DEPTH)


move_duration_list = []


def game_loop(n: int, m: int, player1: Player, player2: Player, first_to_move: Turn) -> None:
    tt = TranspositionTable(n, m)
    game_state = create_initial_state(n, m, first_to_move)

    to_move, next_to_move = player1, player2

    player1_evaluator = evaluation_function_generator_lc(2, 3, 2, 3)
    player2_evaluator = evaluation_function_generator_lc(2, 3, 2, 3)

    to_evaluate, next_to_evaluate = player1_evaluator, player2_evaluator

    move_number = 1
    print_state(game_state)
    while not is_game_over(game_state):
        if to_move == Player.AI:
            depth = dynamic_depth(game_state)
            print(depth)

            start_time = time()
            move, _ = alfabeta(game_state, depth, -math.inf,
                               math.inf, to_evaluate, tt)

            move_duration_list.append((move_number, time() - start_time))
        else:
            move = input_valid_move(game_state)

        new_state = derive_state(game_state, move)
        if new_state:
            game_state = new_state
            to_move, next_to_move = next_to_move, to_move
            # to_evaluate, next_to_evaluate = next_to_evaluate, to_evaluate
            move_number += 1

        print_state(game_state)

    print("Hits: ", tt.hits, " Misses: ", tt.misses,
          " Used: ", tt_cutoff, " AB cutoffs: ", ab_cutoff)


if __name__ == "__main__":
    game_loop(8, 8, Player.AI, Player.AI, Turn.VERTICAL)

    ttAppend = "_tt" if ENABLE_TT else ""

    with open(f"moves_duration_8x8_depth_{MIN_DEPTH}_two_sets_board_undo_move{ttAppend}.txt", "w") as f:
        for t in move_duration_list:
            f.write(f"{t}\n")
