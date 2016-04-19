import copy
import random
import pickle

class QPolicy(object):

	def __init__(self, policy, model, exploration=15, statefile = None):
		self.__policytype = policy
		self.setStatefile(statefile)
		self.q = model.get('model', {})
		self.episode_rewards = model.get('rewards', [])
		self.setExplorationRate(exploration) #set exploration to 15% by default

	def setExplorationRate(self, exploration):
		self.exploration = exploration

	def getQ(self):
		return copy.deepcopy(self.q)

	def getPolicyType(self):
		return self.__policytype

	def getSeenStates(self):
		return frozenset(self.q.keys())

	def setStatefile(self, statefile):
		print "SETTING STATEFILE %s" % statefile
		self.statefile = statefile


	def getAction(self, state, valid_actions):

		this_state_actions = self.q.get(state, {})

		for move in valid_actions:
			this_state_actions[move] = this_state_actions.get(move, 0)

		#use the epsilon greedy strategy to find the next move.
		#create a list of tuples (action, q_value) from available actions (moves)
		move_qval = map(lambda move: (move, this_state_actions[move]), valid_actions)
		#print move_qval
		max_qval = max(move_qval, key = lambda x: x[1])
		#print max_qval

		exploration_choice = random.randint(1, 100)

		if(exploration_choice > 100 - self.exploration and len(move_qval) > 1):
			#randomly make move
			move_qval.remove(max_qval)
			max_qval = random.choice(move_qval)

		ret_move = max_qval[0]

		self.q[state] = this_state_actions

		return ret_move


	def updatePolicy(self):
		pass

	def persistPolicy(self, filepath = None):
		if self.statefile:
			qlmodel = {}
			qlmodel['policy'] = self.__policytype
			qlmodel['model'] = self.q
			qlmodel['rewards'] = self.episode_rewards

			try:
				file = filepath or self.statefile
				with open(file, 'wb') as outfile:
					pickle.dump(qlmodel, outfile)
			except Exception, e:
				print "ERROR: Could not persist policy to file"
				print e
		else:
			print "ERROR: Could not persist policy to file. Please set statefile"

