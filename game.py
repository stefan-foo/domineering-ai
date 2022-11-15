from bitarray import bitarray

class Game:
  def __init__(self, n = 8, m = 8, playerIsVertical = True):
    self.playerToMove = playerIsVertical
    self.playerIsVertical = True
    self.n = n
    self.m = m

    arraySize = n * m
    self.hBitArray = bitarray(arraySize)
    self.vBitArray = bitarray(arraySize)
    self.hBitArray.setall(0)
    self.vBitArray.setall(0)

  def place(self, move):
    if not self.isValid(move):
      return

  def isValid(self, move, isVertical):
    (x, y) = move
    x1 = (x - 1) * self.m
    y1 = (y - 1)
    x2 = x1 if not isVertical else x1 + self.m
    y1 = y1 if isVertical else y1 + 1

    return not (self.hBitArray[x1 ] or self.hBitArray[x * self.m + y + 1] or self.vBitArray[x])

  def __str__(self):
    output = ""
    for i in range(0, self.m * self.n):
      output += "h" if self.hBitArray[i] else ("v" if self.vBitArray[i] else "-")
      output += "\n" if i % self.n == 0 else ""
    return output
  
game = Game()