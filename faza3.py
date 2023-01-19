import math
from faza1 import *
from faza2 import *
from time import time
from tt import *


def count_isolated_moves(state: State) -> tuple[int, int]:
    v_isolated_count = 0
    h_isolated_count = 0

    for j in range(0, state.m):
        i = 1
        while i < state.n:
            if state.board[i][j] == 0 and state.board[i-1][j] == 0 \
                    and (i, j) not in state.h_possible_moves \
                    and (i-1, j) not in state.h_possible_moves \
                    and (i, j-1) not in state.h_possible_moves \
                    and (i-1, j-1) not in state.h_possible_moves:
                v_isolated_count += 1
                i += 1
            i += 1

    for i in range(0, state.n):
        j = 0
        while j < state.m - 1:
            if state.board[i][j] == 0 and state.board[i][j+1] == 0 \
                    and (i, j) not in state.v_possible_moves \
                    and (i, j+1) not in state.v_possible_moves \
                    and (i+1, j) not in state.v_possible_moves \
                    and (i+1, j+1) not in state.v_possible_moves:
                h_isolated_count += 1
                j += 1
            j += 1

    return (v_isolated_count, h_isolated_count)


def evaluate_state(state: State) -> int:
    if is_game_over(state):
        return 1000 if state.to_move is Turn.HORIZONTAL else -1000

    value = 0

    v_im_count, h_im_count = count_isolated_moves(state)

    value += 3 * (v_im_count - h_im_count)
    value += 2 * (len(state.v_possible_moves) - len(state.h_possible_moves))

    return value


tt_cutoff = 0


def alfabeta(state: State, depth: int, alpha: float, beta: float, tt: TranspositionTable) -> tuple[Move, int]:
    if depth == 0 or is_game_over(state):
        value = evaluate_state(state)
        return ((-1, -1), value)

    global tt_cutoff

    tt_val = tt.retrieve(state.board)
    if tt_val is not None:
        tt_move, tt_depth = tt_val
        if depth <= tt_depth:
            tt_cutoff += 1
            return tt_move

    if state.to_move is Turn.VERTICAL:
        best_move = ((-1, -1), -1001)
        for move in set(state.v_possible_moves):
            child_state = derive_state(state, move)
            candidate = alfabeta(child_state, depth - 1, alpha, beta, tt)
            if candidate[1] > best_move[1]:
                best_move = (move, candidate[1])
            alpha = max(alpha, best_move[1])
            if alpha >= beta:
                break
    else:
        best_move = ((-1, -1), 1001)
        for move in set(state.h_possible_moves):
            child_state = derive_state(state, move)
            candidate = alfabeta(child_state, depth - 1, alpha, beta, tt)
            if candidate[1] < best_move[1]:
                best_move = (move, candidate[1])
            beta = min(beta, best_move[1])
            if alpha >= beta:
                break

    tt.store(state.board, (best_move), depth)
    return best_move


def alfabeta_bt(state: State, depth: int, alpha: float, beta: float, tt: TranspositionTable) -> tuple[Move, int]:
    if depth == 0 or is_game_over(state):
        value = evaluate_state(state)
        return ((-1, -1), value)

    global tt_cutoff

    tt_val = tt.retrieve(state.board)
    if tt_val is not None:
        tt_move, tt_depth = tt_val
        if depth <= tt_depth:
            tt_cutoff += 1
            return tt_move

    sorted_moves = list[tuple[int, Move]]()
    for move in list(state.v_possible_moves if state.to_move is Turn.VERTICAL else state.h_possible_moves):
        modify_state(state, move)

        move_eval = evaluate_state(state)

        undo_move(state, move)

        sorted_moves.append((move_eval, move))
    sorted_moves.sort(
        reverse=(True if state.to_move is Turn.VERTICAL else False), key=lambda x: x[0])

    if state.to_move is Turn.VERTICAL:
        best_move = ((-1, -1), -1001)
        for _, move in sorted_moves:
            modify_state(state, move)
            candidate = alfabeta_bt(state, depth - 1, alpha, beta, tt)
            if candidate[1] > best_move[1]:
                best_move = (move, candidate[1])
            alpha = max(alpha, best_move[1])
            if alpha >= beta:
                undo_move(state, move)
                break
            undo_move(state, move)
    else:
        best_move = ((-1, -1), 1001)
        for _, move in sorted_moves:
            modify_state(state, move)
            candidate = alfabeta_bt(state, depth - 1, alpha, beta, tt)
            if candidate[1] < best_move[1]:
                best_move = (move, candidate[1])
            beta = min(beta, best_move[1])
            if alpha >= beta:
                undo_move(state, move)
                break
            undo_move(state, move)

    tt.store(state.board, (best_move), depth)
    return best_move


def dynamic_depth(state: State) -> int:
    rm = len(state.h_possible_moves) + len(state.v_possible_moves)

    return int(1.5 + 32 / math.sqrt(max(rm - 10, 10)))


move_duration_list = []


def game_loop(n: int, m: int, player1: Player, player2: Player, first_to_move: Turn) -> None:
    tt = TranspositionTable(n, m)
    game_state = create_initial_state(n, m, first_to_move)

    to_move, next_to_move = player1, player2

    move_number = 1
    print_state(game_state)
    while not is_game_over(game_state):
        if to_move == Player.AI:
            depth = dynamic_depth(game_state)
            print(depth)

            start_time = time()

            move, _ = alfabeta_bt(game_state, depth, -math.inf, math.inf, tt)

            move_duration_list.append((move_number, time() - start_time))
        else:
            move = input_valid_move(game_state)

        game_state = derive_state(game_state, move)
        to_move, next_to_move = next_to_move, to_move
        move_number += 1

        print_state(game_state)

    print("Hits: ", tt.hits, " Misses: ", tt.misses, " Used: ", tt_cutoff)


if __name__ == "__main__":
    n, m = input_board_dimensions()

    player1 = input_player_type("Player 1: ")
    player2 = input_player_type("Player 2: ")

    game_loop(n, m, player1, player2, Turn.VERTICAL)

    with open(f"moves_duration_{n}x{m}_undo_move_tt.txt", "w") as f:
        for t in move_duration_list:
            f.write(f"{t}\n")
