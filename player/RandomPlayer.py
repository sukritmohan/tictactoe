from Player import Player
from tictactoe import TicTacToeHelper
import random

class RandomPlayer(Player):

	def __init__(self, id):
		Player.__init__(self, id)

	def requestMove(self, board):
		#print "RANDOM_PLAYER MOVE"
		valid_moves = TicTacToeHelper.getValidMoves(board)
		return random.choice(valid_moves)
