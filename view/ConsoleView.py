
class ConsoleView(object):


	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.id_sym = {}


	def initialize(self):
		self.__printHeader()

		print "\n"
		print "\t1 | 2 | 3"
		print "\t---------"
		print "\t4 | 5 | 6"
		print "\t---------"
		print "\t7 | 8 | 9"

		print "\n\nTile positions are number in the manner above.\nPlease enter the tile position to represent your move.\n\n"

		symbol = '_'
		while symbol.upper() != 'X' and symbol.upper() != 'O':
			symbol = raw_input("Player 1: Select 'x' or 'o':  ")
		self.player1.symbol = symbol.lower()
		self.id_sym[self.player1.id] = self.player1.symbol


		if symbol.upper() == 'X':
			self.player2.symbol = 'o'
		else:
			self.player2.symbol = 'x'
		self.id_sym[self.player2.id] = self.player2.symbol


	def __printHeader(self):
		print "\n\n"
		print "==========================================================================="
		print "---------------------------------------------------------------------------"
		print "                             TIC-TAC-TOE"
		print "---------------------------------------------------------------------------"
		print "==========================================================================="


	def showGamePlayState(self, gameplay_state):

		self.__printHeader()
		print "GAME NUMBER : %d" % gameplay_state['game_number']
		print "SCORES:\t\tPlayer 1 (%s): %d\t\t\tPlayer 2 (%s) : %d" % \
			(self.player1.symbol, gameplay_state[self.player1.id], self.player2.symbol, gameplay_state[self.player2.id])

		print "\nPlayer %d goes first!\n" % gameplay_state['next'].id

	def requestMove(self, player, board):
		print "\n"
		self.printBoard(board)

		# def request(id):
		# 	return raw_input("Player %d, select your move:  " % id)

		return player, player.requestMove(board)

	def moveUnsuccessful(self):
		print "Move was unsuccessful. Please try again!"

	def gameEnd(self, state, board):
		print "\n"
		self.printBoard(board)

		if(state == 0):
			print "\n\nThe match was a draw..."
		else:
			print "\n\nThe winner is player %s" % str(state)


	def printBoard(self, board):

		print " ", " ___________\n  ".join(map(lambda row: " | ".join(map(lambda t: ' ' if t == 0 else self.id_sym[t], row)) + "\n", board))


	def die(self):
		print "\n\nThat's all folks!!\n"
