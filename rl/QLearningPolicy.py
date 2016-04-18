import os
import json
from tictactoe import TicTacToeHelper
from QPolicy import QPolicy
import random
import copy

class QLearningPolicy(QPolicy):

	def __init__(self, model={}, alpha = 0.7, gamma = 0.8):
		QPolicy.__init__(self, model)

		self.setLearningRate(alpha) #set alpha to 0.7 by default
		self.setDiscountingFactor(gamma) #set gama to 0.8 by default

		self.newEpisode()

	def newEpisode(self):
		self.__prev_state = None
		self.__prev_action = None
		self.__state_history = []

	def setLearningRate(self, alpha):
		self.alpha = alpha

	def setDiscountingFactor(self, gamma):
		self.gamma = gamma

	def getSeenStates(self):
		return frozenset(self.q.keys())

	# def savePolicy(self, s1, reward = 0):
	# 	self.saveQValue( s1, -1, 0, reward )
    #
	# def saveQValue(self, s1, a1, qval_s1, reward = 0):
	# 	#We want to compute the qval for the state stored in prev_state and update that value based on the qval
	# 	if self.__prev_action and self.__prev_state:
	# 		qvals_state = self.q.get(self.__prev_state, {})
	# 		q_sa = qvals_state.get(self.__prev_action, 0)
    #
	# 		new_q_sa = q_sa + self.alpha * (reward + (self.gamma * qval_s1) - q_sa)
    #
	# 		qvals_state[self.__prev_action] = new_q_sa
	# 		self.q[self.__prev_state] = qvals_state
    #
	# 	# if(abs(reward) > 0):
	# 	# 	print self.q
    #
	# 	self.__prev_action = a1
	# 	self.__prev_state = s1

	def savePolicy(self, terminal_state = None, reward = 0):
		if terminal_state:
			self.__state_history.append((terminal_state, -1))
		self.updateQValues(reward)
		self.episode_rewards.append(reward)

	def updateQValues(self, reward = 0):
		#from the state history create sliding window with 2 states
		reversed_history = list(reversed(self.__state_history))
		state_transitions = [reversed_history[i:i+2] for i in xrange(len(reversed_history)-1)]

		if state_transitions:
			transition = state_transitions.pop()
			e1 = transition[0]
			s1 = e1[0]
			a1 = e1[1]
			e2 = transition[1]
			s2 = e2[0]
			a2 = e2[1]

			#NEED TO FIND qval_s2.
			#For Q-Learning, this will the max( Q(s2, ax) , ax)
			s2_moves = self.q.get(s2, {})
			if len(s2_moves) > 0:
				qval_s2 = max(s2_moves.values())
			else:
				qval_s2 = 0
			#For SARSA, this will the  Q(s2, a2)


			qvals_state = self.q.get(s1, {})
			q_sa = qvals_state.get(a1, 0)

			new_q_sa = q_sa + self.alpha * (reward + (self.gamma * qval_s2) - q_sa)

			qvals_state[a1] = new_q_sa
			self.q[s1] = qvals_state

	def getMove(self, board):

		#print "Q:::"
		#print self.q

		state = TicTacToeHelper.serializeBoard(board)
		this_state_actions = self.q.get(state, {})

		valid_moves = TicTacToeHelper.getValidMoves(board)

		for move in valid_moves:
			this_state_actions[move] = this_state_actions.get(move, 0)

		#print "Q, THIS STATE:"
		#print this_state_actions

		#use the epsilon greedy strategy to find the next move.
		#create a list of tuples (action, q_value) from available actions (moves)
		move_qval = map(lambda move: (move, this_state_actions[move]), valid_moves)
		max_qval = max(move_qval, key = lambda x: x[1])

		orig_max_move = max_qval[0]

		#self.saveQValue(state, max_qval[0], max_qval[1])

		exploration_cutoff = 25 #set exploration to 15%
		exploration_choice = random.randint(1, 100)

		if(exploration_choice > 100 - exploration_cutoff and len(move_qval) > 1):
			print "Going explorer mode"
			#randomly make move
			move_qval.remove(max_qval)
			max_qval = random.choice(move_qval)

		ret_move = max_qval[0]

		self.__state_history.append((state, orig_max_move))
		self.q[state] = this_state_actions

		print "CHOSEN MOVE : ", `ret_move`
		return ret_move


	def persistPolicy(self, filepath):
		self.saveToFile(filepath, "qlearning")



