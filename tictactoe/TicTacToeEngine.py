import itertools
from TicTacToeBoard import TicTacToeBoard
from TicTacToeHelper import TicTacToeHelper

class TicTacToeEngine:

	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.player1_score = 0
		self.player2_score = 0
		self.game_count = 0

		self.turn = False #Player 1 starts. {False: player1, True: player2}
		self.newGame()


	def newGame(self):
		"""
		Set up the board and increment the game_count
		"""
		self.__board = TicTacToeBoard()
		self.__board_size = self.__board.getBoardSideSize()
		self.game_count += 1
		self.player1.newGame()
		self.player2.newGame()

	def getGameplayState(self):
		"""
		Return the gameplay state (to display in view)
		"""
		return {self.player1.id: self.player1_score,
				self.player2.id: self.player2_score,
				'game_number': self.game_count,
				'next': self.getNextPlayer()}

	def getBoard(self):
		"""Return the state of the board"""
		return self.__board.getBoardState()

	def getNextPlayer(self):
		"""Return the next player"""
		if(not self.turn):
			player = self.player1
		else:
			player = self.player2
		return player

	def makeMove(self, player, move):
		"""
		`player` makes `move` on tictactoe board
		:param player: player making the move
		:param move: integer representing tile position on tictactoe board
		:return: boolean denoting whether or not move was successful
		"""

		#the player who is making the move, must be the next player according to TicTacToeEngine. Otherwise something weird is up..
		if(player != self.getNextPlayer()):
			return False

		#make the move on the board. If the move is successful, toggle turn
		move_successful = self.__board.makeMove(player.id, move)
		if move_successful:
			self.turn = not self.turn

		return move_successful


	def evaluateBoard(self):
		"""
		Evaluate whether the game is ongoing or finished, and return the status (ongoing, draw, player1 win, player2 win)
		:return: integer 'state' of the game. {-1: still playing, 0: draw, <x>: player with id <x> wins}
		"""

		#ways of winning: n horizontal, n vertical, 2 diagonal
		state = -1 #
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

		return state


	def gameEnd(self, state):
		"""
		Called when the current game has ended. Depending on state, update the states for the players with the
		appropriate rewards
		:param state: Final game state
		:return:
		"""
		model = self.getBoard()

		if (state == 1):
			self.player1_score += 1
			self.player1.updateState(model, TicTacToeHelper.REWARD_WIN)
			self.player2.updateState(model, TicTacToeHelper.REWARD_LOSE)
		elif (state == 2):
			self.player2_score += 1
			self.player1.updateState(model, TicTacToeHelper.REWARD_LOSE)
			self.player2.updateState(model, TicTacToeHelper.REWARD_WIN)
		elif (state == 0):
			self.player1.updateState(model, TicTacToeHelper.REWARD_DRAW)
			self.player2.updateState(model, TicTacToeHelper.REWARD_DRAW)
		else:
			print "Invalid gameEnd state. Not doing anything"


	def die(self):
		self.player1.saveState()
		self.player2.saveState()


