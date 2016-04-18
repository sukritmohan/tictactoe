import json
import os
import sys

from Player import Player
from rl import QLearningPolicy
from rl import SARSAPolicy
from tictactoe import TicTacToeHelper



class RLBotPlayer(Player):

	def __init__(self, id, statefile = None, policy='qlearning'):
		Player.__init__(self, id)

		self.__statefile = statefile
		self.__policytype = policy

		self.loadModel(self.__statefile)


	def loadModel(self, statefile):
		"""
		Load the model from the statefile given. If statefile doesn't exist, or is empty, start creating a new model
		:param statefile: Filepath of Reinforcement Learning Policy Model
		"""
		try:
			if not os.path.exists(statefile):
				open(statefile, 'w').close()
				self.__state = {}
			else:
				self.__state = json.load(open (statefile, 'r'))
		except Exception:
			print "Couldn't open model file for RLBotPlayer : %s" % statefile
			sys.exit(1)

		if 'policy' in self.__state:
			self.__policytype = self.__state['policy']

		if self.__policytype == 'qlearning':
			policy = QLearningPolicy(self.__state)
		else:
			policy = SARSAPolicy(self.__state)

		self.setPolicy(policy)


	def setPolicy(self, policy):
		self.policy = policy

	def newGame(self):
		self.policy.newEpisode()


	def __selectFromSymmetricStates(self, board):
		"""
		A tictactoe board is symmetrical on rotating. Find a symmetric rotation of this board which we may have seen earlier.
		If we haven't seen any symmetric variation of this board before, default to the original board state.
		Finding a symmetric variation of this board which we have seen before helps us use our previously gained knowledge
		about the optimal policy to choose a better action

		:param board: Status of current board
		:return: <integer>: number of rotations, <2d list>: rotated board
		"""

		#get all the possible board rotations
		board_rotations = TicTacToeHelper.getSymmetricBoardStates(board)
		#which board states have we seen so far?
		policy_seen_states = self.policy.getSeenStates()
		rotation = 0

		if(len(board_rotations) != 4):
			raise Exception("States should be formed by rotating board 4 times")

		while rotation < len(board_rotations):
			this_board = board_rotations[rotation]
			this_state = TicTacToeHelper.serializeBoard(this_board) #state is the serialized board (written as string instead of 2d list)
			if this_state in policy_seen_states:
				break
			rotation += 1

		if rotation == len(board_rotations):
			rotation = 0
			this_board = board_rotations[rotation]

		return rotation, this_board


	def updateState(self, board, reward):

		player_normalized_board = TicTacToeHelper.normalizeBoard(board, self.id)
		rotation, this_board = self.__selectFromSymmetricStates(player_normalized_board)

		self.policy.savePolicy(TicTacToeHelper.serializeBoard(this_board), reward)


	def requestMove(self, board):
		print "BOT_PLAYER MOVE"
		player_normalized_board = TicTacToeHelper.normalizeBoard(board, self.id)

		rotation, this_board = self.__selectFromSymmetricStates(player_normalized_board)

		# pass the rotated and normalized board to the policy to get back the optimal move.
		move = self.policy.getMove(this_board)

		# rotate the optimal move back `rotation` times to match the original board index
		ret_move = TicTacToeHelper.reverseRotateMove(move, rotation)
		return ret_move

	def saveState(self):
		self.policy.persistPolicy(self.__statefile)