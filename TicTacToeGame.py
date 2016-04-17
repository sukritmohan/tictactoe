from tictactoe import TicTacToeEngine
from player import HumanPlayer
from player import RandomPlayer
from view import ConsoleView


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

	def die(self):
		self.game_engine.die()



if __name__ == "__main__":

	#first set if 2 player or against computer, or train
	#TODO: Read arguments and determine which game to play
	is2P = True

	if is2P:
		player1 = HumanPlayer(1)
		player2 = RandomPlayer(2)

	view = ConsoleView(player1, player2)

	game = TicTacToe(player1, player2, view)

	try:
		game.play()
	except KeyboardInterrupt, e:
		game.die()
		view.die()




