import random
import sys


class TranspositionTable:
    def __init__(self, n, m):
        self.table = {}
        self.hits = 0
        self.key = [[[random.randint(0, sys.maxsize) for _ in range(
            m)] for _ in range(n)] for _ in range(2)]
        self.misses = 0

    def store(self, board, best_move, depth):
        self.table[self.hash_board(board)] = best_move, depth

    def retrieve(self, board):
        # return None
        key = self.hash_board(board)
        if key in self.table:
            self.hits += 1
            return self.table[key]
        self.misses += 1
        return None

    def hash_board(self, board) -> int:
        hash = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] != 0):
                    hash = hash ^ self.key[board[i][j] - 1][i][j]
        return hash
