import json
import pickle
import os
import sys

from Player import Player
from rl import QLearningPolicy
from rl import SARSAPolicy
from tictactoe import TicTacToeHelper



class RLBotPlayer(Player):

	def __init__(self, id, policy):
		Player.__init__(self, id)
		self.setPolicy(policy)

	def setPolicy(self, policy):
		self.policy = policy

	def newGame(self):
		self.__state_history = []
		self.__reward = []

	def __selectFromSymmetricStates(self, board):
		"""
		This is an optimization strategy. Instead of training the model on every possible variation of the board, train
		it on every distinct variation of the board. For any tictactoe board state, the boards formed by rotating this
		board 3 times are equivalent in structure to the original tictactoe board.

		Find a symmetric rotation of this board which we may have seen earlier.
		If we haven't seen any symmetric variation of this board before, default to the original board state.

		:param board: Status of current board
		:return: <integer>: number of rotations, <2d list>: rotated board
		"""

		#get all the possible board rotations
		board_rotations = TicTacToeHelper.getBoardRotatedStates(board)
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

	def __getNormalizedAndRotatedBoard(self, board):
		"""
		Normalize this board for this particular player (This player denoted as 'A', other player denoted as 'B', EMPTY as EMPTY).
		This normalized notation helps maintain consistency in denoting states for the RL model.
		Finding a symmetric variation of this board which we have seen before helps us use our previously gained knowledge
		about the optimal policy to choose a better action

		Choose a symmetric variation of normalized board which the RL model has seen before and return <rotation_count, rotated_board>
		"""
		player_normalized_board = TicTacToeHelper.normalizeBoard(board, self.id)
		rotation, this_board = self.__selectFromSymmetricStates(player_normalized_board)

		return rotation, this_board

	def updateState(self):
		"""Should be called on terminal state. Update the policy."""
		if len(self.__state_history) != len(self.__reward):
			raise Exception("State|Action tuples must be of the same length as Reward list")

		sar = [(sa[0], sa[1], r) for (sa, r) in zip(self.__state_history, self.__reward)]

		self.policy.updatePolicyWithStateHistory(sar)


	def requestMove(self, board):
		"""Request move from policy - this is called to get the move which the player wants to make"""
		#get the rotated and normalized board for this player
		rotation, this_board = self.__getNormalizedAndRotatedBoard(board)

		# pass the rotated and normalized board to the policy to get back the optimal move.
		this_state = TicTacToeHelper.serializeBoard(this_board)
		valid_moves = TicTacToeHelper.getValidMoves(this_board)

		move = self.policy.getAction(this_state, valid_moves)

		# rotate the optimal move back `rotation` times to match the original board index
		ret_move = TicTacToeHelper.reverseRotateMove(move, rotation)
		return ret_move

	def makeMove(self, board, move):
		"""
		If the move selected by the player is valid, 
		then Engine asks player to makeMove and update its internal state
		"""
		rotation, this_board = self.__getNormalizedAndRotatedBoard(board)
		this_state = TicTacToeHelper.serializeBoard(this_board)

		this_move = TicTacToeHelper.rotateMove(move, rotation)

		self.__state_history.append((this_state, this_move))

	def receiveReward(self, reward):
		"""
		Based on player's previous move and the state reached on taking action, 
		Engine sends player a reward for the move
		"""
		if len(self.__state_history) > 0:
			self.__reward.append(reward)
		else:
			#can't receive reward without making any move first. This else statement is encountered
			#on new game situations. Do nothing here..
			pass

	def saveState(self):
		self.policy.persistPolicy()


