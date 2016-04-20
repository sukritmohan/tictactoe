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
					self.game_engine.gameEnd(state)


	def die(self):
		self.game_engine.die()



if __name__ == "__main__":

	this_dir = os.path.dirname(os.path.abspath(__file__))

	parser = OptionParser()
	parser.add_option("--2p", dest="is2P", default=False, action='store_true', help="Play a 2 Player game")
	parser.add_option("--training", dest="isTraining", default=False, action='store_true', help="Run in training mode")
	parser.add_option("--qlearning", dest="isQL", default=True, action='store_true', help="Use Q-Learning Policy for RL_Bot")
	parser.add_option("--sarsa", dest="isSARSA", default=False, action='store_true', help="Use SARSA Policy for RL_Bot")
	parser.add_option("--policy_file", dest="policy_file", help="Path to policy file. This is where the learned model will be read from and saved to.")


	(options, args) = parser.parse_args()

	if not options.is2P:
		if options.isQL: #Bot follows QLearning Policy
			#if model_file is passed, use that, otherwise use the previously trained qlearning model.
			filepath = options.policy_file or (this_dir + "/rl/qlmodel_agent_v_agent.dmp")
			policy = RLHelper.loadModel(filepath, "qlearning")
		elif options.isSARSA: #Bot follows SARSA Policy
			filepath = options.policy_file or (this_dir + "/rl/sarsamodel_agent_v_agent.dmp")
			policy = RLHelper.loadModel(filepath, "sarsa")



	if options.is2P:
		player1 = HumanPlayer(1)
		player2 = HumanPlayer(2)
		view = ConsoleView(player1, player2)
	elif options.isTraining:
		player1 = RandomPlayer(1)
		player2 = RLBotPlayer(2, policy)
		view = TrainingView(player1, player2)
	else: #default to 1P vs Bot game
		player1 = HumanPlayer(1)
		player2 = RLBotPlayer(2, policy)
		view = ConsoleView(player1, player2)

	## Training Agent-vs-Agent game using the same policy object ##
	# The way the code is designed, the rewards list will be meaningless here, since at each game we append a WIN and a LOSS to the list.
	# policy1 = RLHelper.loadModel((this_dir + "/rl/sarsamodel_agent_v_agent.dmp"), "sarsa")
	# policy2 = RLHelper.loadModel((this_dir + "/rl/qlmodel_agent_v_agent.dmp"), "qlearning")
	# player1 = RLBotPlayer(1, policy1)
	# player2 = RLBotPlayer(2, policy2)
	# view = TrainingView(player1, player2)

	game = TicTacToe(player1, player2, view)

	try:
		game.play()
	except KeyboardInterrupt, e:
		game.die()
		view.die()




