from enum import Enum
import random
from itertools import product 
import tkinter

class CellStates(Enum):
  UNEXPOSED = 1
  EXPOSED = 2
  SEALED = 3

class GameStatus(Enum):
  WON = 1
  LOST = 2
  INPROGRESS = 3

class Minesweeper():
  def __init__(self):
    self.SIZE = 10
    self.cell_states = [[CellStates.UNEXPOSED for j in range(self.SIZE)] for i in range(self.SIZE)]
    self.mines = [[False for j in range(self.SIZE)] for i in range(self.SIZE)]

  def get_cell_state(self, row, column):
    return self.cell_states[row][column]

  def expose_cell(self, row, column):
    if self.cell_states[row][column] == CellStates.UNEXPOSED:
      self.cell_states[row][column] = CellStates.EXPOSED

      if self.adjacentMinesCountAt(row, column) == 0 and not self.is_mine_at(row, column):
        self.expose_neighbors(row, column)

  def toggle_seal(self, row, column):
    self.cell_states[row][column] = {
     CellStates.UNEXPOSED: CellStates.SEALED,
     CellStates.SEALED: CellStates.UNEXPOSED,
     CellStates.EXPOSED: CellStates.EXPOSED
    }[self.cell_states[row][column]]

  def expose_neighbors(self, row, column):
    for i in range(max(0, row - 1), min(row + 2, self.SIZE)):
      for j in range(max(0, column - 1), min(column + 2, self.SIZE)):
        self.expose_cell(i, j)

  def is_mine_at(self, row, column):
    return row in range(0, self.SIZE) and column in range (0, self.SIZE) and self.mines[row][column]
    
  def adjacentMinesCountAt(self, row, column):
    adjacent_mines_count = 0
    for i in range(max(0, row - 1), min(row + 2, self.SIZE)):
      for j in range(max(0, column - 1), min(column + 2, self.SIZE)):
        if self.mines[row][column] is not True and self.is_mine_at(i, j):
          adjacent_mines_count += 1

    return adjacent_mines_count

  def setMines(self, seed):
    random.seed(seed)

    mines_count = 0 

    while mines_count < 10:
      row = random.randint(0, 9)
      column = random.randint(0, 9)
      if not self.is_mine_at(row, column):
        self.mines[row][column] = True
        mines_count += 1

    return mines_count

  def get_game_status(self):
    def check_loss():
      return any([self.mines[row][column] == True and self.cell_states[row][column] == CellStates.EXPOSED for row, column in product(range(self.SIZE), range(self.SIZE))])
    
    def check_in_progress():
      return any([not self.mines[row][column] and self.cell_states[row][column] == CellStates.UNEXPOSED for row, column in product(range(self.SIZE), range(self.SIZE))])

    if check_loss():
      return GameStatus.LOST
  
    if check_in_progress():
      return GameStatus.INPROGRESS

    return GameStatus.WON