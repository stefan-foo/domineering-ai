from typing import Iterable
from faza1 import *


V_EFFECTS_TO_H = ((0, 0), (-1, 0), (-1, -1), (0, -1))
V_EFFECTS_TO_V = ((0, 0), (-1, 0), (1, 0))

H_EFFECTS_TO_H = ((0, 0), (0, 1), (0, -1))
H_EFFECTS_TO_V = ((0, 0), (0, 1), (1, 0), (1, 1))


def derive_state(state: State, move: Move) -> None | State:
    if not is_valid_move(state, move):
        return None

    (x, y) = move

    v_possible_moves_copy = state.v_possible_moves.copy()
    h_possible_moves_copy = state.h_possible_moves.copy()

    v_played_moves_copy = state.v_played_moves.copy()
    h_played_moves_copy = state.h_played_moves.copy()

    if state.to_move == Turn.VERTICAL:
        effects_to_v = V_EFFECTS_TO_V
        effects_to_h = V_EFFECTS_TO_H

        v_played_moves_copy.add((x, y))

        next_to_move = Turn.HORIZONTAL
    else:
        effects_to_v = H_EFFECTS_TO_V
        effects_to_h = H_EFFECTS_TO_H

        h_played_moves_copy.add((x, y))

        next_to_move = Turn.VERTICAL

    for cx, cy in effects_to_h:
        h_possible_moves_copy.discard((x + cx, y + cy))
    for cx, cy in effects_to_v:
        v_possible_moves_copy.discard((x + cx, y + cy))

    return State(
        n=state.n,
        m=state.m,
        v_played_moves=v_played_moves_copy,
        h_played_moves=h_played_moves_copy,
        v_possible_moves=v_possible_moves_copy,
        h_possible_moves=h_possible_moves_copy,
        to_move=next_to_move)


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


if __name__ == "__main__":
    game_loop()
