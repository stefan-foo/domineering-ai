import math
from game import Game


class Node:
    def __init__(self, data: float):
        self.children: list[Node] = []
        self.data = data


def minimax(game: Game, position: Node, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:

    # game.transform(position)

    if depth == 0 or game.game_over():
        return game.evaluate()

    if maximizing_player:
        max_eval: float = -math.inf
        for child in position.children:
            eval: float = minimax(game, child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return max_eval
    else:
        min_eval: float = +math.inf
        for child in position.children:
            eval: float = minimax(game, child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return min_eval


# initial call
# minimax(current_position, 3, -∞, +∞, True)
