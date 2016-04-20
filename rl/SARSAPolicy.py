
from QLearningPolicy import QLearningPolicy

class SARSAPolicy(QLearningPolicy):

	def __init__(self, model={}, statefile = None, alpha = 0.7, gamma = 0.8, exploration = 15, policytype = "sarsa"):
		print "BOT FOLLOWS SARSA POLICY"
		QLearningPolicy.__init__(self, model=model, statefile = statefile, alpha = alpha, gamma = gamma, exploration = exploration, policytype = policytype)


	def updateQValues(self, state_history, reward = 0):
		"""
		We are given the sequence of states which the player has seen till it reached the terminal state and acquired
		`reward`. Based on <s0,s1,s2,...,sn> and reward at sn, update the Q-Policy using SARSA method.
		:param state_history: List of states visited by player
		:param reward: Reward acquired at terminal state
		"""

		#from the state history create sliding window with 2 states to get all state transitions
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
				this_reward = 0 #a2 == -1 means terminal state (this hardcoded value needs some code refactoring)

			#NEED TO FIND qval_s2.
			#For Q-Learning, this will the max( Q(s2, ax) , ax)
			#For SARSA, this will the  Q(s2, a2)
			s2_moves = self.q.get(s2, {})
			qval_s2 = s2_moves.get(a2, 0)


			qvals_state = self.q.get(s1, {})
			q_sa = qvals_state.get(a1, 0)

			new_q_sa = q_sa + self.alpha * (this_reward + (self.gamma * qval_s2) - q_sa)

			qvals_state[a1] = new_q_sa
			self.q[s1] = qvals_state

		#print "Q VALUES AFTER EPISODE::"
		#print self.q