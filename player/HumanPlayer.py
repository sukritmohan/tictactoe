from Player import Player

class HumanPlayer(Player):

	def __init__(self, id):
		Player.__init__(self, id)

	def requestMove(self, board):
		#TODO: This obviously won't work for anything other than ConsoleView. Need to refactor to generalize across views
		return raw_input("Player %d move: " % self.id)
