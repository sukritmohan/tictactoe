
class TrainingView(object):

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def initialize(self):
        pass

    def showGamePlayState(self, gameplay_state):
        print "SCORES:\t\tPlayer 1 (%s): %d\t\t\tPlayer 2 (%s) : %d" % \
			(self.player1.id, gameplay_state[self.player1.id], self.player2.id, gameplay_state[self.player2.id])

    def requestMove(self, player, board):
        return player, player.requestMove(board)

    def moveUnsuccessful(self):
        print "Move was unsuccessful. Please try again!"

    def gameEnd(self, state, board):
        pass

    def die(self):
        print "\n\nThat's all folks!!\n"
