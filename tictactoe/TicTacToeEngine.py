import itertools
from TicTacToeBoard import TicTacToeBoard
from TicTacToeHelper import TicTacToeHelper

class TicTacToeEngine:

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.player1_score = 0
		self.player2_score = 0

		self.__board = None

		self.turn = False #Player 1 starts. {False: player1, True: player2}

	def newGame(self):
		self.__board = TicTacToeBoard()
		self.__board_size = self.__board.getBoardSideSize()

	def getGameplayState(self):
		return {self.player1.id: self.player1_score,
				self.player2.id: self.player2_score,
				'next': self.getNextPlayer()}

	def getBoard(self):
		if not self.__board:
			raise Exception('must start newGame before calling getBoard')

		return self.__board.getBoardState()

	def getNextPlayer(self):
		if(not self.turn):
			player = self.player1
		else:
			player = self.player2
		return player

	def makeMove(self, player, move):
		if not self.__board:
			raise Exception('must start newGame before calling makeMove')

		if(player != self.getNextPlayer()):
			return False


		move_successful = self.__board.makeMove(player.id, move)

		if move_successful:
			self.turn = not self.turn

		return move_successful


	def evaluateBoard(self):
		if not self.__board:
			raise Exception('must start newGame before calling evaluateBoard')

		#ways of winning: n horizontal, n vertical, 2 diagonal
		state = -1 # {-1: still playing, 0: draw, <x>: player with id <x> wins}
		model = self.getBoard()

		#HORIZONTAL
		for i in range(0, self.__board_size):
			this_row = model[i]
			if (len(set( this_row )) == 1 and this_row[0] != TicTacToeHelper.EMPTY):
				state = this_row[0]
				break

		#VERTICAL
		if (state == -1):
			for i in range(0, self.__board_size):
				this_col = map(lambda t: t[i], model)
				if (len(set( this_col )) == 1 and this_col[0] != TicTacToeHelper.EMPTY):
					state = this_col[0]
					break

		#DIAGONAL
		#enumerate gives us the index of each row. We can use this row_index to find diagonals.
		#[
		# (0, [1, 2, 3]),
		# (1, [4, 5, 6]),
		# (2, [7, 8, 9])
		#]
		if (state == -1):
			diag_lr = map(lambda (row_index, row): row[row_index], enumerate(model))
			if (len(set( diag_lr )) == 1 and diag_lr[0] != TicTacToeHelper.EMPTY):
				state = diag_lr[0]

		if (state == -1):
			diag_rl = map(lambda (row_index, row): row[self.__board_size-1-row_index], enumerate(model))
			if (len(set( diag_rl )) == 1 and diag_rl[0] != TicTacToeHelper.EMPTY):
				state = diag_rl[0]

		#DRAW
		if (state == -1):
			flattened_board = list(itertools.chain.from_iterable(model))
			if all(x != TicTacToeHelper.EMPTY for x in flattened_board):
				state = 0


		print state
		if (state == 1):
			self.player1_score += 1
		elif (state == 2):
			self.player2_score += 1

		return state

	def die(self):
		self.player1.saveState()
		self.player2.saveState()


