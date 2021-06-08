import unittest
import random

from src import minesweeper
from minesweeper import Minesweeper
from minesweeper import CellStates
from minesweeper import GameStatus

class MinesweeperTests(unittest.TestCase):
  def setUp(self):
      self.minesweeper = Minesweeper()
    
  def test_canary(self):
      self.assertTrue(True)

  def test_initial_cell_state_unexposed(self):
    self.assertEqual(CellStates.UNEXPOSED, self.minesweeper.get_cell_state(1, 2))

  def test_expose_unexposed_cell(self):
    self.minesweeper.expose_cell(1, 3)

    self.assertEqual(CellStates.EXPOSED, self.minesweeper.get_cell_state(1, 3))

  def test_expose_exposed_cell(self):
    self.minesweeper.expose_cell(1, 3)

    self.minesweeper.expose_cell(1, 3)

    self.assertEqual(CellStates.EXPOSED, self.minesweeper.get_cell_state(1, 3))
  
  def test_out_of_bounds(self):
    self.assertRaises(IndexError, self.minesweeper.expose_cell, 10, 10)

  def test_seal_unexposed_cell(self):
    self.minesweeper.toggle_seal(1, 4)

    self.assertEqual(CellStates.SEALED, self.minesweeper.get_cell_state(1, 4))

  def test_unseal_sealed_cell(self):
    self.minesweeper.toggle_seal(1, 4)

    self.minesweeper.toggle_seal(1, 4)

    self.assertEqual(CellStates.UNEXPOSED, self.minesweeper.get_cell_state(1, 4))

  def test_seal_exposed_cell(self):
    self.minesweeper.expose_cell(1, 4)

    self.minesweeper.toggle_seal(1, 4)

    self.assertEqual(CellStates.EXPOSED, self.minesweeper.get_cell_state(1, 4))

  def test_expose_sealed_cell(self):
    self.minesweeper.toggle_seal(1, 4)

    self.minesweeper.expose_cell(1, 4)

    self.assertEqual(CellStates.SEALED, self.minesweeper.get_cell_state(1, 4))

  def test_expose_calls_expose_neighbors(self):
    class MinesweeperExposeNeighborsStubbed(Minesweeper):
      def expose_neighbors(self, row, column):
        self.called = True
        
    minesweeper = MinesweeperExposeNeighborsStubbed()
    
    minesweeper.called = False

    minesweeper.expose_cell(1, 3)
    
    self.assertTrue(minesweeper.called)

  def test_expose_does_not_call_expose_neighbors_on_exposed_cells(self):
    class MinesweeperExposeNeighborsStubbed(Minesweeper):
      def expose_neighbors(self, row, column):
        self.called = True
        
    minesweeper = MinesweeperExposeNeighborsStubbed()
    
    minesweeper.expose_cell(1, 3)

    minesweeper.called = False

    minesweeper.expose_cell(1, 3)
    
    self.assertFalse(minesweeper.called)

  def test_expose_sealed_does_not_call_expose_neighbors(self):
    class MinesweeperExposeNeighborsStubbed(Minesweeper):
      def expose_neighbors(self, row, column):
        self.called = True

    minesweeper = MinesweeperExposeNeighborsStubbed()

    minesweeper.toggle_seal(1, 6)

    minesweeper.called = False

    minesweeper.expose_cell(1, 6)

    self.assertFalse(minesweeper.called)

  def test_expose_neighbors_calls_expose_on_eight_neighbors(self):
    class MinesweeperExposeNeighborsStubbed(Minesweeper):
      actual_values = []

      def expose_cell(self, row, column):
          self.actual_values.append((row, column))

    minesweeper = MinesweeperExposeNeighborsStubbed()

    expected_values = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]

    minesweeper.expose_neighbors(4, 4)

    self.assertEqual(expected_values, minesweeper.actual_values)
  

  def test_expose_top_left_cell_expose_only_existing_cells(self):
    class MinesweeperExposeNeighborsStubbed(Minesweeper):
      actual_values = []

      def expose_cell(self, row, column):
        self.actual_values.append((row, column))

    minesweeper = MinesweeperExposeNeighborsStubbed()

    expected_values = [(0, 0), (0, 1), (1, 0), (1, 1)]

    minesweeper.expose_neighbors(0, 0)

    self.assertEqual(expected_values, minesweeper.actual_values)
  
  def test_expose_bottom_right_cell_expose_only_existing_cells(self):
    class MinesweeperExposeNeighborsStubbed(Minesweeper):
      actual_values = []

      def expose_cell(self, row, column):
        self.actual_values.append((row, column))

    minesweeper = MinesweeperExposeNeighborsStubbed()

    expected_values = [(8, 8), (8, 9), (9, 8), (9, 9)]

    minesweeper.expose_neighbors(9, 9)

    self.assertEqual(expected_values, minesweeper.actual_values)

  def test_expose_border_cell_expose_only_existing_cells(self):
    class MinesweeperExposeNeighborsStubbed(Minesweeper):
      actual_values = []

      def expose_cell(self, row, column):
        self.actual_values.append((row, column))

    minesweeper = MinesweeperExposeNeighborsStubbed()

    expected_values = [(4, 0), (4, 1), (5, 0), (5, 1), (6, 0), (6, 1)]

    minesweeper.expose_neighbors(5, 0)

    self.assertEqual(expected_values, minesweeper.actual_values)

  def test_mine_at_position(self):
    self.assertFalse(self.minesweeper.is_mine_at(3, 2))

  def test_set_mine(self):
    self.minesweeper.mines[3][2] = True

    self.assertTrue(self.minesweeper.is_mine_at(3, 2))

  def test_is_mine_at_first_case(self):
    self.assertFalse(self.minesweeper.is_mine_at(-1, 4))

  def test_is_mine_at_second_case(self):
    self.assertFalse(self.minesweeper.is_mine_at(10, 5))

  def test_is_mine_at_third_case(self):
    self.assertFalse(self.minesweeper.is_mine_at(5, -1))

  def test_is_mine_at_fourth_case(self):
    self.assertFalse(self.minesweeper.is_mine_at(7, 10))

  def test_adjacent_cell_not_calls_expose_neighbors(self):
    class MinesweeperExposeNeighborsStubbed(Minesweeper):
      def expose_neighbors(self, row, column):
        self.called = True

    minesweeper = MinesweeperExposeNeighborsStubbed()

    minesweeper.called = False

    minesweeper.mines[3][3] = True

    minesweeper.expose_cell(4, 4)

    self.assertFalse(minesweeper.called)

  def test_adjacent_mines_count_returns_zero(self):
    self.assertEqual(0, self.minesweeper.adjacentMinesCountAt(4, 6))

  def test_mined_cell_returns_zero_adjacent_mines(self):
    self.minesweeper.mines[3][4] = True

    self.assertEqual(0, self.minesweeper.adjacentMinesCountAt(3, 4))

  def test_one_adjacent_mine_returns_one(self):
    self.minesweeper.mines[3][4] = True

    self.assertEqual(1, self.minesweeper.adjacentMinesCountAt(3, 5))

  def test_two_adjacent_mines_returns_two(self):
    self.minesweeper.mines[3][4] = True

    self.minesweeper.mines[2][6] = True

    self.assertEqual(2, self.minesweeper.adjacentMinesCountAt(3, 5))

  def test_top_left_cell_returns_one_adjacent_mine(self):
    self.minesweeper.mines[0][1] = True

    self.assertEqual(1, self.minesweeper.adjacentMinesCountAt(0, 0))

  def test_top_right_cell_returns_zero_adjacent_mines(self):
    self.assertEqual(0, self.minesweeper.adjacentMinesCountAt(0, 9))

  def test_bottom_right_cell_returns_one_adjacent_mine(self):
    self.minesweeper.mines[9][8] = True

    self.assertEqual(1, self.minesweeper.adjacentMinesCountAt(9, 9))

  def test_bottom_left_cell_returns_zero_adjacent_mines(self):
    self.assertEqual(0, self.minesweeper.adjacentMinesCountAt(9, 0))

  def test_game_status_returns_inprogress(self):
    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_game_status_returns_lost_on_expose_mine_cell(self):
    self.minesweeper.mines[4][3] = True

    self.minesweeper.expose_cell(4, 3)

    self.assertEqual(GameStatus.LOST, self.minesweeper.get_game_status()) 

  def test_all_mines_sealed_returns_inprogress_when_cells_unexposed(self):
    self.minesweeper.mines[4][4]= True

    self.minesweeper.mines[6][7] = True

    self.minesweeper.toggle_seal(4, 4)

    self.minesweeper.toggle_seal(6, 7)

    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_all_mines_sealed_returns_inprogress_when_empty_cell_sealed(self):
    self.minesweeper.mines[4][4] = True

    self.minesweeper.mines[6][7] = True

    self.minesweeper.toggle_seal(4, 4)

    self.minesweeper.toggle_seal(6, 7)

    self.minesweeper.toggle_seal(3, 1)

    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_all_mines_sealed_returns_inprogress_when_adjacent_cell_unexposed(self):
    self.minesweeper.mines[4][4] = True

    self.minesweeper.mines[6][7] = True

    self.minesweeper.toggle_seal(4, 4)

    self.minesweeper.toggle_seal(6, 7)

    self.assertEqual(GameStatus.INPROGRESS, self.minesweeper.get_game_status())

  def test_all_mines_sealed_returns_won_all_other_cells_exposed(self):
    self.minesweeper.mines[4][4] = True

    self.minesweeper.mines[6][7] = True

    self.minesweeper.toggle_seal(4, 4)

    self.minesweeper.toggle_seal(6, 7)

    for row in range(0, 10):
      for column in range(0, 10):
        if not self.minesweeper.is_mine_at(row, column):
          self.minesweeper.cell_states[row][column] = CellStates.EXPOSED

    self.assertEqual(GameStatus.WON, self.minesweeper.get_game_status())

  def test_verify_ten_mines_for_seed_zero(self):
    self.minesweeper.setMines(0)

  def test_different_minefields_for_different_seeds(self):
    self.minesweeper.setMines(0)

    minefield_for_seed_zero = self.minesweeper.mines

    self.minesweeper.mines = [[False for j in range(0, 10)] for i in range(0, 10)]

    self.minesweeper.setMines(1)

    minefield_for_seed_one = self.minesweeper.mines

    self.assertNotEqual(minefield_for_seed_zero, minefield_for_seed_one)

if __name__ == '__main__':
    unittest.main()