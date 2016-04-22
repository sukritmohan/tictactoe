
from QPolicy import QPolicy

class QLearningPolicy(QPolicy):

	def __init__(self, model={}, statefile = None, alpha = 0.2, gamma = 0.8, exploration = 15, policytype = "qlearning"):
		print "BOT FOLLOWS QLEARNING POLICY"
		QPolicy.__init__(self, policytype, model, exploration, statefile)

		self.setLearningRate(alpha) #set alpha to 0.2 by default
		self.setDiscountingFactor(gamma) #set gamma to 0.8 by default

	def setLearningRate(self, alpha):
		self.alpha = alpha

	def setDiscountingFactor(self, gamma):
		self.gamma = gamma


	def updatePolicyWithStateHistory(self, state_history):
		"""
		state_history is a list of tuples (state, action, reward) describing the actions taken by the bot
		update q-values using the state transitions, and store the reward for this episode
		:param state_history: List of tuples (state, action, reward)
		"""
		self.__updateQValuesWithStateHistory(state_history)
		rewards = map(lambda t: t[2], state_history)
		self.episode_rewards.append(sum(rewards))


	def updatePolicy(self, state1, action1, state2, action2 = None, reward = 0):
		"""
		Given s1,a1,r1,s2,a2, update the Q-values using Q-Learning
		"""
		
		#NEED TO FIND qval_s2.
		#For Q-Learning, this will be  max( Q(s2, ax) , ax)
		s2_moves = self.q.get(state2, {})
		
		if len(s2_moves) > 0:
		        qval_state2 = max(s2_moves.values())
		else:
		        qval_state2 = 0
		#For SARSA, this will the  Q(s2, a2)
		#       --implemented in SARSAPolicy
		
		s1_moves = self.q.get(state1, {})
		q_sa = s1_moves.get(action1, 0)
		
		new_q_sa = (1 - self.alpha) * q_sa + self.alpha * (reward + (self.gamma * qval_state2) - q_sa)
		
		s1_moves[action1] = new_q_sa
		self.q[state1] = s1_moves


	def __updateQValuesWithStateHistory(self, state_history):
		"""
		From the state_history supplied, update q-values for this policy
		:param state_history: List of tuples (state, action, reward)
		"""

		state_history.append(("game", -1, 0))

		#from the state history create sliding window with 2 states to capture state transitions
		state_transitions = [state_history[i:i+2] for i in xrange(len(state_history)-1)]

		while state_transitions:
			transition = state_transitions.pop()

			#print transition
			
			e1 = transition[0]
			s1 = e1[0]
			a1 = e1[1]
			r1 = e1[2]
			e2 = transition[1]
			s2 = e2[0]
			a2 = e2[1]
			r2 = e2[2]

			self.updatePolicy(s1,a1,s2,a2,r1)

		#print "Q VALUES AFTER EPISODE::"
		#print self.q


