import random
import sys
from faza1 import *


class TranspositionTable:
    def __init__(self, n: int, m: int):
        self.table = {}
        self.hits = 0
        self.key = [[[random.randint(0, sys.maxsize) for _ in range(
            m)] for _ in range(n)] for _ in range(2)]
        self.misses = 0

    def store(self, board: list[list[int]], best_move: tuple[Move, int], depth: int) -> None:
        self.table[self.cache_key(board)] = best_move, depth

    def retrieve(self, board: list[list[int]]):
        key = self.cache_key(board)
        if key in self.table:
            self.hits += 1
            return self.table[key]
        self.misses += 1
        return None

    def cache_key(self, board: list[list[int]]) -> int:
        hash = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] != 0):
                    hash = hash ^ self.key[board[i][j] - 1][i][j]
        return hash


i = 1000000000000000000000000
a = 5555555555555555555555555

print(i ^ a)
