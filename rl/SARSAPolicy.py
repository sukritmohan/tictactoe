
from QLearningPolicy import QLearningPolicy

class SARSAPolicy(QLearningPolicy):

	def __init__(self, model={}, statefile = None, alpha = 0.7, gamma = 0.8, exploration = 15, policytype = "sarsa"):
		print "BOT FOLLOWS SARSA POLICY"
		QLearningPolicy.__init__(self, model=model, statefile = statefile, alpha = alpha, gamma = gamma, exploration = exploration, policytype = policytype)


	def updatePolicy(self, state1, action1, state2, action2 = None, reward = 0):
		"""
		Given s1,a1,r1,s2,a2, update the Q-values using Q-Learning
		"""
		
		#NEED TO FIND qval_s2.
		#For Q-Learning, this will the max( Q(s2, ax) , ax)
		#For SARSA, this will the  Q(s2, a2)
		s2_moves = self.q.get(state2, {})
		qval_state2 = s2_moves.get(action2, 0)
		
		s1_moves = self.q.get(state1, {})
		q_sa = s1_moves.get(action1, 0)
		
		new_q_sa = q_sa + self.alpha * (reward + (self.gamma * qval_state2) - q_sa)
		
		s1_moves[action1] = new_q_sa
		self.q[state1] = s1_moves
