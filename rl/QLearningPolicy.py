
from QPolicy import QPolicy

class QLearningPolicy(QPolicy):

	def __init__(self, model={}, statefile = None, alpha = 0.7, gamma = 0.8, exploration = 15, policytype = "qlearning"):
		print "BOT FOLLOWS QLEARNING POLICY"
		QPolicy.__init__(self, policytype, model, exploration, statefile)

		self.setLearningRate(alpha) #set alpha to 0.7 by default
		self.setDiscountingFactor(gamma) #set gamma to 0.8 by default

	def setLearningRate(self, alpha):
		self.alpha = alpha

	def setDiscountingFactor(self, gamma):
		self.gamma = gamma

	def updatePolicy(self, state_history, reward = 0):
		self.updateQValues(state_history, reward)
		self.episode_rewards.append(reward)

	def updateQValues(self, state_history, reward = 0):
		"""
		We are given the sequence of states which the player has seen till it reached the terminal state and acquired
		`reward`. Based on <s0,s1,s2,...,sn> and reward at sn, update the Q-Policy using Q-Learning method.
		:param state_history: List of states visited by player
		:param reward: Reward acquired at terminal state
		"""

		#from the state history create sliding window with 2 states to capture state transitions
		state_transitions = [state_history[i:i+2] for i in xrange(len(state_history)-1)]

		while state_transitions:
			transition = state_transitions.pop()

			#print transition
			
			e1 = transition[0]
			s1 = e1[0]
			a1 = e1[1]
			e2 = transition[1]
			s2 = e2[0]
			a2 = e2[1]

			if a2 == -1:
				this_reward = reward
			else:
				this_reward = 0

			#NEED TO FIND qval_s2.
			#For Q-Learning, this will be  max( Q(s2, ax) , ax)
			s2_moves = self.q.get(s2, {})

			if len(s2_moves) > 0:
				qval_s2 = max(s2_moves.values())
			else:
				qval_s2 = 0
			#For SARSA, this will the  Q(s2, a2)
			#	--implemented in SARSAPolicy

			qvals_state = self.q.get(s1, {})
			q_sa = qvals_state.get(a1, 0)

			new_q_sa = q_sa + self.alpha * (this_reward + (self.gamma * qval_s2) - q_sa)

			qvals_state[a1] = new_q_sa
			self.q[s1] = qvals_state

		#print "Q VALUES AFTER EPISODE::"
		#print self.q


