from enum import Enum
from typing import Tuple


class Field(Enum):
    EMPTY = 1
    PLAYER1 = 2
    PLAYER2 = 3


class Game:
    def __init__(self, n: int = 8, m: int = 8) -> None:
        self.n: int = n  # broj vrsta
        self.m: int = m  # broj kolona
        self.v_players_turn: bool = True

        self.v_possible_moves: set[Tuple[int, int]] = set()
        self.h_possible_moves: set[Tuple[int, int]] = set()

        for i in range(n-2):
            for j in range(m-2):
                self.v_possible_moves.add((i, j))
                self.h_possible_moves.add((i, j))

        # vertikalni u poslednjoj koloni
        for i in range(n-1):
            self.v_possible_moves.add((i, m-1))

        # horizontalni u poslednjoj vrsti
        for i in range(m-1):
            self.h_possible_moves.add((n-1, i))

        self.board_matrix = [[Field.EMPTY for _ in range(m)] for _ in range(n)]

    def ai_turn(self) -> None:
        # pozvati minimax
        # x, y = minimax(...)
        # self.place(x, y)

        return

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
            self.h_possible_moves.discard((x, y-1))
            self.h_possible_moves.discard((x + 1, y-1))
            self.h_possible_moves.discard((x, y + 1))
            # vertikali sam sebi blokira jos jedno polje
            # # b #
            # #[b]#
            # #[b]#
            self.v_possible_moves.discard((x + 1, y))
            self.v_possible_moves.discard((x - 1, y))

        else:  # horizontal zauzima mesta (x, y) i (x, y + 1)
            self.board_matrix[x][y + 1] = fieldToWrite

            # vertikalnom blokira jos 3 polja 
            self.h_possible_moves.discard((x - 1, y + 1))
            self.v_possible_moves.discard((x - 1, y + 1))
            self.v_possible_moves.discard((x, y + 1))

            # horizontalni samom sebi blokira jos dva polja
            self.h_possible_moves.discard((x, y + 1))
            self.h_possible_moves.discard((x, y - 1))

        self.v_players_turn = not self.v_players_turn
        return

    def valid_move(self, x: int, y: int) -> bool:
        if self.v_players_turn:
            return (x, y) in self.v_possible_moves
        else:
            return (x, y) in self.h_possible_moves

    def evaluate(self) -> float:
        return 0

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
game.place(1, 1)
game.place(6, 1)
game.place(7, 2)
print(game)
