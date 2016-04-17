from Player import Player

class HumanPlayer(Player):

	def __init__(self, id):
		Player.__init__(self, id)

	def requestMove(self, board):
		return raw_input("Player %d move: " % self.id)
