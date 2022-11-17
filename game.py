from enum import Enum
from typing import Tuple


class Field(Enum):
    EMPTY = 1
    VERTICAL = 2
    HORIZONTAL = 3


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

        self.h_moves_within_bounds = self.h_possible_moves.copy()
        self.v_moves_within_bounds = self.v_possible_moves.copy()

        self.board_matrix = [[Field.EMPTY for _ in range(m)] for _ in range(n)]
        self.move_history: list[tuple[int, int]] = []

    def ai_turn(self) -> None:
        # pozvati minimax
        # x, y = minimax(...)
        # self.place(x, y)

        return

    def evaluate(self) -> float:
        if (self.game_over()):
            return -100 if self.v_players_turn else 100
        return len(self.v_possible_moves) / len(self.h_possible_moves)

    def player_turn(self, x: int, y: int) -> None:
        self.do_move(x, y)
        return

    def do_move(self, x: int, y: int) -> None:
        if not self.valid_move(x, y):
            return

        fieldToWrite: Field = Field.VERTICAL if self.v_players_turn else Field.HORIZONTAL

        self.board_matrix[x][y] = fieldToWrite

        self.v_possible_moves.discard((x, y))
        self.h_possible_moves.discard((x, y))

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

    def undo_move(self) -> None:
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
            if (px, py) in self.h_moves_within_bounds and self.board_matrix[px][py] is Field.EMPTY:
                self.h_possible_moves.add((px, py))

        for cx, cy in effects_to_v:
            px, py = x + cx, y + cy
            if (px, py) in self.v_moves_within_bounds and self.board_matrix[px][py] is Field.EMPTY:
                self.v_possible_moves.add((px, py))

    def valid_move(self, x: int, y: int) -> bool:
        if self.v_players_turn:
            return (x, y) in self.v_possible_moves
        else:
            return (x, y) in self.h_possible_moves

    def move_within_bounds(self, x: int, y: int) -> bool:
        if self.v_players_turn:
            return (x, y) in self.v_moves_within_bounds
        else:
            return (x, y) in self.h_moves_within_bounds

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
                    case Field.VERTICAL:
                        output_str += "[*]"
                    case Field.HORIZONTAL:
                        output_str += "[x]"
            output_str += "\n"
        return output_str


game: Game = Game()
print("initial", len(game.h_possible_moves))

game.do_move(1, 1)
print(1, 1, len(game.h_possible_moves))
print(game)

game.do_move(6, 1)
print(6, 1, len(game.h_possible_moves))
print(game)

game.do_move(6, 4)
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
