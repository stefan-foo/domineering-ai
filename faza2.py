from typing import Iterable
from faza1 import *
from copy import deepcopy

V_EFFECTS_TO_H = ((0, 0), (-1, 0), (-1, -1), (0, -1))
V_EFFECTS_TO_V = ((0, 0), (-1, 0), (1, 0))

H_EFFECTS_TO_H = ((0, 0), (0, 1), (0, -1))
H_EFFECTS_TO_V = ((0, 0), (0, 1), (1, 0), (1, 1))


def derive_state(state: State, move: Move) -> State:
    (x, y) = move

    v_possible_moves_copy = set(state.v_possible_moves)
    h_possible_moves_copy = set(state.h_possible_moves)

    board_copy = deepcopy(state.board)

    if state.to_move == Turn.VERTICAL:
        effects_to_v = V_EFFECTS_TO_V
        effects_to_h = V_EFFECTS_TO_H

        board_copy[x][y] = board_copy[x-1][y] = 1

        next_to_move = Turn.HORIZONTAL
    else:
        effects_to_v = H_EFFECTS_TO_V
        effects_to_h = H_EFFECTS_TO_H

        board_copy[x][y] = board_copy[x][y+1] = 2

        next_to_move = Turn.VERTICAL

    for cx, cy in effects_to_h:
        h_possible_moves_copy.discard((x + cx, y + cy))
    for cx, cy in effects_to_v:
        v_possible_moves_copy.discard((x + cx, y + cy))

    return State(state.n, state.m, board_copy, v_possible_moves_copy, h_possible_moves_copy, next_to_move)


def modify_state(state: State, move: Move) -> State:
    (x, y) = move

    if state.to_move == Turn.VERTICAL:
        effects_to_v = V_EFFECTS_TO_V
        effects_to_h = V_EFFECTS_TO_H

        state.board[x][y] = state.board[x-1][y] = 1

        state.to_move = Turn.HORIZONTAL
    else:
        effects_to_v = H_EFFECTS_TO_V
        effects_to_h = H_EFFECTS_TO_H

        state.board[x][y] = state.board[x][y+1] = 2

        state.to_move = Turn.VERTICAL

    for cx, cy in effects_to_h:
        state.h_possible_moves.discard((x + cx, y + cy))
    for cx, cy in effects_to_v:
        state.v_possible_moves.discard((x + cx, y + cy))

    return state


def undo_move(state: State, move: Move) -> State:
    (x, y) = move

    if state.to_move == Turn.VERTICAL:
        effects_to_v = H_EFFECTS_TO_V
        effects_to_h = H_EFFECTS_TO_H

        state.board[x][y] = state.board[x][y+1] = 0

        state.to_move = Turn.HORIZONTAL
    else:
        effects_to_v = V_EFFECTS_TO_V
        effects_to_h = V_EFFECTS_TO_H

        state.board[x][y] = state.board[x-1][y] = 0

        state.to_move = Turn.VERTICAL

    for cx, cy in effects_to_h:
        p_move = x + cx, y + cy
        if is_valid_move_on_board(state.board, p_move, Turn.HORIZONTAL):
            state.h_possible_moves.add(p_move)

    for cx, cy in effects_to_v:
        p_move = x + cx, y + cy
        if is_valid_move_on_board(state.board, p_move, Turn.VERTICAL):
            state.v_possible_moves.add(p_move)

    return state


def generate_possible_states(state: State) -> Iterable[State]:
    for move in possible_moves(state):
        new_state = derive_state(state, move)
        if new_state is not None:
            yield new_state


def possible_moves(state: State) -> set[Move]:
    return state.v_possible_moves if state.to_move is Turn.VERTICAL else state.h_possible_moves


def input_valid_move(state: State) -> Move:
    legal_move = None
    while not legal_move:
        move = input_move(state.to_move)
        if move and is_valid_move(state, move):
            legal_move = move
        else:
            print(Fore.RED + "Invalid move!" + Style.RESET_ALL)
    return legal_move


def game_loop() -> None:
    n, m = input_board_dimensions()

    # initial_turn = input_move_order()
    # player1 = input_player_type()
    # player2 = input_player_type()

    state = create_initial_state(n, m)

    while not is_game_over(state):
        print_state(state)

        move = input_valid_move(state)

        new_state = derive_state(state, move)
        if new_state:
            state = new_state

    print_state(state)


game_state = create_initial_state(8, 8, Turn.VERTICAL)
