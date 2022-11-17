from game import Game


class AI:
    @staticmethod
    def maxmin(game: Game, move: tuple[int, int], depth: int, alpha: float, beta: float) -> tuple[tuple[int, int], float]:
        if depth == 0 or game.game_over():  # O(1)
            return (move, game.evaluate())  # najskuplja operacija

        game.do_move(move[0], move[1])  # O(1)

        if game.v_players_turn:
            best_move = ((0, 0), float('-inf'))
            for move in game.v_possible_moves:
                candidate = AI.maxmin(game, move, depth - 1, alpha, beta)

                if candidate[1] > best_move[1]:
                    best_move = candidate

                alpha = max(alpha, best_move[1])
                if alpha >= beta:
                    break

        else:
            best_move = ((0, 0), float('inf'))
            for move in game.h_possible_moves:
                candidate = AI.maxmin(game, move, depth - 1, alpha, beta)

                if candidate[1] < best_move[1]:
                    best_move = candidate

                beta = min(beta, best_move[1])
                if alpha >= beta:
                    break

        game.undo_move()  # O(1)
        return best_move


# initial call
# minimax(current_position, 3, -∞, +∞, True)
