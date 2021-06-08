import unittest
import random

from minesweeper import Minesweeper
from minesweeper import CellStates
from minesweeper import GameStatus

import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb, messagebox

class Game(tk.Frame):
	def __init__(self, parent, Minesweeper, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.SIZE = 10
		self.parent = parent
		self.minesweeper = Minesweeper
		self.cells =[[MinesweeperCell for i in range(self.SIZE)] for j in range(self.SIZE)]
		self.gameFrame = tk.LabelFrame(text='Minesweeper', bg='#f7f5ff')
		self.gameFrame.grid(row = self.SIZE, column = self.SIZE, sticky = N+S+E+W)

		for row in range(0, self.SIZE):
			for column in range(0, self.SIZE):
					self.cells[row][column] = MinesweeperCell(self.gameFrame, row, column, self.minesweeper.cell_states[row][column], self.minesweeper.mines[row][column], self.minesweeper.adjacentMinesCountAt(row, column), text = '     ', bg = '#c2c2c2', width = 4, height = 2)
					self.cells[row][column].grid(column = column, row = row, sticky = N+S+E+W)

					self.cells[row][column].bind('<Button-1>', lambda event, self = self,  row = row, column = column: self.gui_expose_cell(event, row, column))
					self.cells[row][column].bind('<Button-3>', lambda event, self = self,  row = row, column = column: self.gui_seal_cell(event, row, column))

	def gui_expose_cell(self, event, row, column):
		if self.minesweeper.get_game_status() == GameStatus.INPROGRESS:
			if self.minesweeper.get_cell_state(row, column) != CellStates.SEALED:
				self.minesweeper.expose_cell(row, column)
				if self.cells[row][column].mine:
						text = '*'
						self.cells[row][column]['text'] = text

				elif self.minesweeper.adjacentMinesCountAt(row, column) > 0:
						text = self.minesweeper.adjacentMinesCountAt(row, column)
				else:
						text = '--'
						self.gui_expose_neighbors(row, column)
				self.cells[row][column]['text'] = text
				self.gui_game_status()
			
	def gui_expose_neighbors(self, row, column):
			def determine_type(row, column):
				text = '*'
				if self.minesweeper.adjacentMinesCountAt(row, column) > 0:
					text = self.minesweeper.adjacentMinesCountAt(row, column)
				elif not self.minesweeper.is_mine_at(row, column):
					text = '--'
				return text

			for i in range(self.minesweeper.SIZE):
					for j in range(self.minesweeper.SIZE):
						if self.minesweeper.get_cell_state(i, j) == CellStates.EXPOSED:
							self.cells[i][j]['text'] = determine_type(i, j)

	def gui_seal_cell(self, event, row, column):
		if self.minesweeper.get_game_status() == GameStatus.INPROGRESS:
			if self.minesweeper.get_cell_state(row, column) == CellStates.UNEXPOSED:
				self.cells[row][column]['text'] = '|>'
			elif self.minesweeper.get_cell_state(row, column) == CellStates.SEALED:
				self.cells[row][column]['text'] = '     '
			self.minesweeper.toggle_seal(row, column)
			self.gui_game_status()
	
	def gui_game_status(self):
		def expose_all_mines():
			for i in range(self.minesweeper.SIZE):
				for j in range(self.minesweeper.SIZE):
					if self.cells[i][j].mine:
						self.cells[i][j]['text'] = '*'
						
		game_status = self.minesweeper.get_game_status()
		if game_status == GameStatus.LOST:
			expose_all_mines()
			messagebox.showerror('Game Lost', 'Mine Exposed!')

		elif game_status == GameStatus.WON:
			messagebox.showinfo('Game Won', 'Congratulations! You Won The Game!')

class MinesweeperCell(tk.Button):
	def __init__(self, parent, row, column, cell_state, mine_info, adj_mines_count, *args, **kwargs):
		tk.Button.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.row = row
		self.column = column
		self.minesweeper = Minesweeper
		self.state = cell_state
		self.mine = mine_info
		self.adj_mines_count = adj_mines_count

root = tk.Tk()
root.geometry('382x428')
root.title('Minesweeper')
root.configure(background='whitesmoke')
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
minesweeper = Minesweeper()
minesweeper.setMines(0)
game = Game(root, minesweeper)
root.mainloop()