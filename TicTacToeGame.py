from tictactoe import TicTacToeEngine
from player import HumanPlayer
from player import RandomPlayer
from player import RLBotPlayer
from view import ConsoleView
from view import TrainingView

from rl import RLHelper

import os

from optparse import OptionParser


class TicTacToe:


	def __init__(self, player1, player2, view):
		self.player1 = player1
		self.player2 = player2
		self.view = view
		self.game_engine = TicTacToeEngine(self.player1, self.player2)

	def play(self):

		self.view.initialize()

		game_number = 0

		while True:

			self.view.showGamePlayState(self.game_engine.getGameplayState())
			state = -1

			self.game_engine.newGame()

			while(state == -1):

				player, move = self.view.requestMove(self.game_engine.getNextPlayer(), self.game_engine.getBoard())

				move_successful = self.game_engine.makeMove(player, move)
				if not move_successful:
					self.view.moveUnsuccessful() #Invalid move. Try again - engine does not toggle player turn.
					continue

				state = self.game_engine.evaluateBoard()
				if(state != -1):
					#game has ended. Print state.
					self.view.gameEnd(state, self.game_engine.getBoard())

			game_number += 1

	def die(self):
		self.game_engine.die()



if __name__ == "__main__":

	this_dir = os.path.dirname(os.path.abspath(__file__))

	is2P = False
	is1P = False
	isTraining = True

	isSARSA = True
	isQL = False

	parser = OptionParser()
	parser.add_option("--2p", dest="is2P", default=False, action='store_true')
	parser.add_option("--training", dest="isTraining", default=False, action='store_true')
	parser.add_option("--qlearning", dest="isQL", default=False, action='store_true')
	parser.add_option("--sarsa", dest="isSARSA", default=False, action='store_true')
	parser.add_option("--model_file", dest="model_file", help="Path to model file")


	(options, args) = parser.parse_args()

	if options.is2P:
		is2P = True
	elif options.isTraining:
		isTraining = True
	else:
		is1P = True

	if is1P or isTraining:
		statefile = options.model_file or ""

		if options.isQL:
			if not statefile:
				statefile = this_dir + "/rl/qlmodel_agent_v_random.dmp"
		elif options.isSARSA:
			if not statefile:
				statefile = this_dir + "/rl/sarsamodel_agent_v_random.dmp"


	#statefile = "/Users/sukritmohan/code/repo2/rl/test.dmp"


	#policy = RLHelper.loadModel(statefile)

	#policy = RLHelper.getNewModel("qlearning")
	policy = RLHelper.getNewModel("sarsa")
	policy.setStatefile(statefile)

	if isTraining:
		player1 = RandomPlayer(1)
		player2 = RLBotPlayer(2, policy)
		view = TrainingView(player1, player2)
	elif is1P:
		player1 = HumanPlayer(1)
		player2 = RLBotPlayer(2, policy)
		view = ConsoleView(player1, player2)
	elif is2P:
		player1 = HumanPlayer(1)
		player2 = HumanPlayer(2)
		view = ConsoleView(player1, player2)


	game = TicTacToe(player1, player2, view)

	try:
		game.play()
	except KeyboardInterrupt, e:
		game.die()
		view.die()




