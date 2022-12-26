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
def alfabeta(state: State, depth: int, alpha: float, beta: float) -> tuple[Move | None, int]:
    if depth == 0 or is_game_over(state):
        return ((-1, -1), evaluate_state(state))

    if state.to_move is Turn.VERTICAL:
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


DEPTH_TEST = 4

mode = PlayingMode.PLAYER_VS_PLAYER


def human_turn(game_state):
    move = input_move(game_state.to_move)
    if move:
        new_game_state = derive_state(game_state, move)
        if new_game_state:
            game_state = new_game_state
        else:
            print("Invalid move")
    else:
        print("Enter move in format ROW COLUMN")
    return game_state, move


def game_loop() -> None:
    if mode is PlayingMode.PLAYER_VS_AI or mode is PlayingMode.PLAYER_VS_PLAYER:
        n, m = input_board_dimensions()
    else:
        n, m = 10, 10

    game_state: State = create_initial_state(n, m)

    last_move = None
    move = None
    eval = 0
    while not is_game_over(game_state):
        print_state(game_state)
        if last_move:
            print(
                f"\nMove played: {(last_move[0] + 1, chr(ord('A') + last_move[1]))} [{eval}]\n")
        if mode is PlayingMode.AI_VS_AI:
            move, eval = alfabeta(
                game_state, DEPTH_TEST, -math.inf, math.inf)
        elif mode is PlayingMode.PLAYER_VS_AI:
            if game_state.to_move is Turn.VERTICAL:  # Human turn
                game_state, move = human_turn(game_state)
            else:  # AI turn
                move, eval = alfabeta(
                    game_state, DEPTH_TEST, -math.inf, math.inf)
        elif mode is PlayingMode.PLAYER_VS_PLAYER:
            game_state, move = human_turn(game_state)

        # ovaj deo ispod da se ocisti, nzm sta je to kog djavola
        last_move = move
        if move:
            new_game_state = derive_state(game_state, move)
        else:
            break
        if new_game_state is not None:
            game_state = new_game_state

    # isto i ovo ispod
    last_state = game_state
    alfabeta(last_state, DEPTH_TEST, -math.inf, math.inf)
    print_state(game_state)
    print(
        f"{'VERTICAL' if game_state.to_move is Turn.HORIZONTAL else 'HORIZONTAL'} WON")


if __name__ == "__main__":
    game_loop()
