import math
from faza1 import *
from faza2 import *


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


def evaluate_state(state: State) -> int:
    if is_game_over(state):
        return 100 if state.to_move is Turn.HORIZONTAL else -100

    (v_safe_moves, h_safe_moves) = derive_isolated_moves(state)
    return 2*len(state.v_possible_moves) + len(v_safe_moves) - (2*len(state.h_possible_moves) + len(h_safe_moves))


# @lru_cache(maxsize=256)
def alfabeta(state: State, depth: int, alpha: float, beta: float) -> tuple[Move, int]:
    if depth == 0 or is_game_over(state):
        return ((-1, -1), evaluate_state(state))

    if state.to_move is Turn.VERTICAL:
        best_move = ((-1, -1), -1001)
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
        best_move = ((-1, -1), 1001)
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


DEPTH_TEST = 4


def game_loop(n, m, player1, player2, initial_to_move) -> None:
    game_state = create_initial_state(n, m, initial_to_move)

    to_move, next_to_move = player1, player2
    while not is_game_over(game_state):
        if to_move == Player.AI:
            move, eval = alfabeta(game_state, DEPTH_TEST, -math.inf, math.inf)
        else:
            move = input_valid_move(game_state)

        new_state = derive_state(game_state, move)
        if new_state:
            game_state = new_state

        to_move, next_to_move = next_to_move, to_move
        print_state(game_state)

    print_state(game_state)


if __name__ == "__main__":
    game_loop(8, 8, Player.AI, Player.AI, Turn.VERTICAL)
