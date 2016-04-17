import itertools
import copy
from TicTacToeHelper import TicTacToeHelper

class TicTacToeBoard:

	## BOARD IS INDEXED AS:
	##
	##	1 | 2 | 3
	##	4 | 5 | 6
	##	7 | 8 | 9
	##

	def __init__(self):
		self.__board_size = 3
		self.__model = [[TicTacToeHelper.EMPTY for x in range(self.__board_size)] for x in range(self.__board_size)] # n*n matrix set to all 0's

	def getBoardState(self):
		return copy.deepcopy(self.__model)

	def getBoardSideSize(self):
		return self.__board_size

	def makeMove(self, player_id, move):
		#from the mapping 'move', get the actual location on the board.
		try:
			move_int = int(move)
		except Exception:
			return False

		move_i, move_j = TicTacToeBoard.__getMovePosition(move_int)
		if self.__isValidMove(move_i, move_j):
			self.__model[move_i][move_j] = player_id
			return True
		return False

	def isValidMove(self, move):
		try:
			move_int = int(move)
		except Exception:
			return False

		i,j = TicTacToeBoard.__getMovePosition(move)
		return self.__isValidMove(i,j)

	@staticmethod
	def __getMovePosition(move, board_size = 3):
		i = (move-1)/board_size
		j = (move-1) % board_size
		return i,j

	def __isValidMove(self, i, j):
		return (i >=0 and i < self.__board_size and \
				j >=0 and j < self.__board_size and \
				self.__model[i][j] == TicTacToeHelper.EMPTY)

