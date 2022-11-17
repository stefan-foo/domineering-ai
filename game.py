from enum import Enum
from typing import Tuple


class Field(Enum):
    EMPTY = 1
    PLAYER1 = 2
    PLAYER2 = 3


v_effects_to_h = ((0, 0), (1, 0), (1, -1), (0, -1))
v_effects_to_v = ((0, 0), (1, 0), (-1, 0))

h_effects_to_h = ((0, 0), (0, 1), (0, -1))
h_effects_to_v = ((0, 0), (0, 1), (-1, 0), (-1, 1))


class Game:
    def __init__(self, n: int = 8, m: int = 8) -> None:
        self.n: int = n  # broj vrsta
        self.m: int = m  # broj kolona
        self.v_players_turn: bool = True

        self.v_possible_moves: set[Tuple[int, int]] = set()
        self.h_possible_moves: set[Tuple[int, int]] = set()

        for i in range(n-1):
            for j in range(m):
                self.v_possible_moves.add((i, j))
        for i in range(n):
            for j in range(m-1):
                self.h_possible_moves.add((i, j))

        self.h_legal_moves = self.h_possible_moves.copy()
        self.v_legal_moves = self.v_possible_moves.copy()

        self.board_matrix = [[Field.EMPTY for _ in range(m)] for _ in range(n)]
        self.move_history: list[tuple[int, int]] = []

    def ai_turn(self) -> None:
        # pozvati minimax
        # x, y = minimax(...)
        # self.place(x, y)

        return

    def evaluate(self):
        if (self.game_over()):
            return -100 if self.v_players_turn else 100
        return len(self.v_possible_moves) / len(self.h_possible_moves)

    def maxmin(self, move: tuple[int, int], depth: int) -> tuple[tuple[int, int], float]:
        if (self.game_over()):
            return (move, self.evaluate())

        self.place(move[0], move[1])

        if self.v_players_turn:
            best_move = ((0, 0), float('-inf'))
            for move in self.v_possible_moves:
                candidate = self.maxmin(move, depth - 1)
                if candidate[1] > best_move[1]:
                    best_move = candidate
                self.undo_move()
        else:
            best_move = ((0, 0), float('inf'))
            for move in self.v_possible_moves:
                candidate = self.maxmin(move, depth - 1)
                if candidate[1] < best_move[1]:
                    best_move = candidate

        self.undo_move()
        return best_move

    def player_turn(self, x: int, y: int) -> None:
        self.place(x, y)
        return

    def place(self, x: int, y: int) -> None:
        if not self.valid_move(x, y):
            return

        fieldToWrite: Field = Field.PLAYER1 if self.v_players_turn else Field.PLAYER2

        self.board_matrix[x][y] = fieldToWrite

        self.v_possible_moves.discard((x, y))
        #self.v_possible_moves.discard((x - 1, y))

        self.h_possible_moves.discard((x, y))
        #self.h_possible_moves.discard((x, y - 1))

        if self.v_players_turn:  # vertical zauzima mesta (x, y) i (x+1, y)
            self.board_matrix[x+1][y] = fieldToWrite

            # horizontalnom blokira 2 polja
            # # # #
            # b[b]#
            # b[b]#
            self.h_possible_moves.discard((x + 1, y))
            self.h_possible_moves.discard((x, y - 1))
            self.h_possible_moves.discard((x + 1, y - 1))
            # vertikali sam sebi blokira jos jedno polje
            # # b #
            # #[b]#
            # #[b]#
            self.v_possible_moves.discard((x + 1, y))
            self.v_possible_moves.discard((x - 1, y))

        else:  # horizontal zauzima mesta (x, y) i (x, y + 1)
            self.board_matrix[x][y + 1] = fieldToWrite

            # vertikalnom blokira jos 3 polja
            self.v_possible_moves.discard((x - 1, y))
            self.v_possible_moves.discard((x, y + 1))
            self.v_possible_moves.discard((x - 1, y + 1))

            # horizontalni samom sebi blokira jos dva polja
            self.h_possible_moves.discard((x, y + 1))
            self.h_possible_moves.discard((x, y - 1))

        self.v_players_turn = not self.v_players_turn
        self.move_history.append((x, y))
        return

    def undo_move(self):
        if len(self.move_history) == 0:
            return

        *self.move_history, (x, y) = self.move_history
        # vraca se potez
        self.v_players_turn = not self.v_players_turn

        self.board_matrix[x][y] = Field.EMPTY
        if self.v_players_turn:
            self.board_matrix[x+1][y] = Field.EMPTY
            effects_to_v = v_effects_to_v
            effects_to_h = v_effects_to_h
        else:
            self.board_matrix[x][y + 1] = Field.EMPTY
            effects_to_v = h_effects_to_v
            effects_to_h = h_effects_to_h

        for cx, cy in effects_to_h:
            px, py = x + cx, y + cy
            if (px, py) in self.h_legal_moves and self.board_matrix[px][py] is Field.EMPTY:
                self.h_possible_moves.add((px, py))
        for cx, cy in effects_to_v:
            px, py = x + cx, y + cy
            if (px, py) in self.v_legal_moves and self.board_matrix[px][py] is Field.EMPTY:
                self.v_possible_moves.add((px, py))

    def valid_move(self, x: int, y: int) -> bool:
        if self.v_players_turn:
            return (x, y) in self.v_possible_moves
        else:
            return (x, y) in self.h_possible_moves

    # mora da bude O(1)
    def game_over(self) -> bool:
        return (len(self.v_possible_moves) == 0 and self.v_players_turn) or (
            len(self.h_possible_moves) == 0 and not self.v_players_turn)

    def __str__(self):
        output_str = ""
        for i in range(self.n):
            for j in range(self.m):
                match self.board_matrix[i][j]:
                    case Field.EMPTY:
                        output_str += "[ ]"
                    case Field.PLAYER1:
                        output_str += "[*]"
                    case Field.PLAYER2:
                        output_str += "[x]"
            output_str += "\n"
        return output_str


game: Game = Game()
print("initial", len(game.h_possible_moves))

game.place(1, 1)
print(1, 1, len(game.h_possible_moves))
print(game)

game.place(6, 1)
print(6, 1, len(game.h_possible_moves))
print(game)

game.place(6, 4)
print(6, 4, len(game.h_possible_moves))
print(game)

game.undo_move()
print("undo", 6, 4, len(game.h_possible_moves))
print(game)

game.undo_move()
print("undo", 6, 1, len(game.h_possible_moves))
print(game)

game.undo_move()
print("undo", 1, 1, len(game.h_possible_moves))
print(game)
