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


	def updateState(self, board, reward):
		"""
		Should be called on terminal state. Update the policy.
		:param board: final board
		:param reward: reward at end of game
		:return: None
		"""
		#get the rotated and normalized board for this player
		rotation, this_board = self.__getNormalizedAndRotatedBoard(board)

		self.__state_history.append((TicTacToeHelper.serializeBoard(this_board), -1))

		self.policy.updatePolicy(self.__state_history, reward)


	def requestMove(self, board):

		#get the rotated and normalized board for this player
		rotation, this_board = self.__getNormalizedAndRotatedBoard(board)

		# pass the rotated and normalized board to the policy to get back the optimal move.
		this_state = TicTacToeHelper.serializeBoard(this_board)
		valid_moves = TicTacToeHelper.getValidMoves(this_board)

		move = self.policy.getAction(this_state, valid_moves)

		#save this state and the move that this player made for this state
		self.__state_history.append((this_state, move))

		# rotate the optimal move back `rotation` times to match the original board index
		ret_move = TicTacToeHelper.reverseRotateMove(move, rotation)
		return ret_move


	def saveState(self):
		self.policy.persistPolicy()