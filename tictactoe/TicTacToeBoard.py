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
		self.__board_size = TicTacToeHelper.SIZE
		self.__model = [[TicTacToeHelper.EMPTY for x in range(self.__board_size)] for x in range(self.__board_size)] # n*n matrix set to all 0's

	def getBoardState(self):
		"""Return a copy of the state of the board"""
		return copy.deepcopy(self.__model)

	def getBoardSideSize(self):
		"""Return board size"""
		return self.__board_size

	def isValidMove(self, move):
		"""Verify if `move` can be made on the tictactoe board"""
		try:
			move_int = int(move)
		except Exception:
			return False

		i,j = TicTacToeHelper.getMoveIndexes(move_int)
		return self.__isValidMove(i,j)

	def makeMove(self, player_id, move):
		"""Player `player_id` makes `move` on board"""
		if(self.isValidMove(move)):
			move_i, move_j = TicTacToeHelper.getMoveIndexes(int(move))
			self.__model[move_i][move_j] = player_id
			return True

		return False

	def __isValidMove(self, i, j):
		return (i >=0 and i < self.__board_size and \
				j >=0 and j < self.__board_size and \
				self.__model[i][j] == TicTacToeHelper.EMPTY)

