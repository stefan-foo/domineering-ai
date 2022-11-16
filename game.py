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
        self.first_players_turn: bool = True

        self.player1_moves_left: set[Tuple[int, int]] = set()
        self.player2_moves_left: set[Tuple[int, int]] = set()

        for i in range(n-2):
            for j in range(m-2):
                self.player1_moves_left.add((i, j))
                self.player2_moves_left.add((i, j))

        # vertikalni u poslednjoj koloni
        for i in range(n-1):
            self.player1_moves_left.add((i, m-1))

        # horizontalni u poslednjoj vrsti
        for i in range(m-1):
            self.player2_moves_left.add((n-1, i))

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

        fieldToWrite: Field = Field.PLAYER1 if self.first_players_turn else Field.PLAYER2

        self.board_matrix[x][y] = fieldToWrite

        self.player1_moves_left.discard((x, y))
        self.player1_moves_left.discard((x, y-1))

        self.player2_moves_left.discard((x, y))
        self.player2_moves_left.discard((x-1, y))

        if self.first_players_turn:  # vertical zauzima mesta (x, y) i (x, y+1)
            self.board_matrix[x][y+1] = fieldToWrite

            # vertikali sam sebi blokira jos jedno polje
            # # b #
            # #[b]#
            # #[b]#
            self.player1_moves_left.discard((x, y+1))

            # horizontalnom blokira 2 polja
            # # # #
            # b[b]#
            # b[b]#
            self.player2_moves_left.discard((x-1, y+1))
            self.player2_moves_left.discard((x, y+1))

        else:  # horizontal zauzima mesta (x, y) i (x+1, y)
            self.board_matrix[x+1][y] = fieldToWrite

            # vertikalnom blokira jos 2 polja (polja iznad)
            self.player1_moves_left.discard((x+1, y))
            self.player1_moves_left.discard((x+1, y-1))

            # horizontalni samom sebi blokira jos jedno polje
            self.player2_moves_left.discard((x+1, y))

        self.first_players_turn = not self.first_players_turn
        return

    def valid_move(self, x: int, y: int) -> bool:
        if self.first_players_turn:
            return (x, y) in self.player1_moves_left
        else:
            return (x, y) in self.player2_moves_left

    def evaluate(self) -> float:
        return 0

    # mora da bude O(1)
    def game_over(self) -> bool:
        return len(self.player1_moves_left) == 0 or len(self.player2_moves_left) == 0

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
