from enum import Enum


class Field(Enum):
    EMPTY = 1
    PLAYER1 = 2
    PLAYER2 = 3


class Game:
    def __init__(self, n: int = 8, m: int = 8) -> None:
        self.n: int = n
        self.m: int = m
        self.firstPlayersTurn: bool = True

        self.board_matrix = [[Field.EMPTY for _ in range(m)] for _ in range(n)]

    def place(self, x: int, y: int) -> None:
        if not self.isValidMove(x, y):
            return

        fieldToWrite: Field = Field.PLAYER1 if self.firstPlayersTurn else Field.PLAYER2

        self.board_matrix[x][y] = fieldToWrite

        if self.firstPlayersTurn:  # vertical
            self.board_matrix[x+1][y] = fieldToWrite
        else:  # horizontal
            self.board_matrix[x][y+1] = fieldToWrite

        self.firstPlayersTurn = not self.firstPlayersTurn
        return

    def isValidMove(self, x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False

        if self.firstPlayersTurn:
            return x < self.n - 1 and y < self.m and (
                self.board_matrix[x][y] is Field.EMPTY and self.board_matrix[x+1][y] is Field.EMPTY)
        else:
            return x < self.n and y < self.m - 1 and (
                self.board_matrix[x][y] is Field.EMPTY and self.board_matrix[x][y+1] is Field.EMPTY)

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
