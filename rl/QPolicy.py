import copy
import random
import pickle
import abc


class QPolicy(object):

	def __init__(self, policytype, model, exploration=15, statefile = None):
		self.__policytype = policytype
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
		"""
		Use the epsilon greedy policy to select the next action from a list of valid actions, given the state.
		Epsilon is stored as self.exploration - this is the probability by which function returns random action.
		Function returns optimal action with probability (1-epsilon).
		:param state: State of the game
		:param valid_actions: List of valid actions which can be taken
		:return:
		"""

		this_state_actions = self.q.get(state, {})

		for move in valid_actions:
			this_state_actions[move] = this_state_actions.get(move, 0)

		#use the epsilon greedy strategy to find the next move.
		#create a list of tuples (action, q_value) from available actions (moves)
		move_qval = map(lambda move: (move, this_state_actions[move]), valid_actions)
		max_qval = max(move_qval, key = lambda x: x[1])

		exploration_choice = random.randint(1, 100)

		if(exploration_choice > 100 - self.exploration and len(move_qval) > 1):
			#randomly make move
			move_qval.remove(max_qval)
			max_qval = random.choice(move_qval)

		ret_move = max_qval[0]

		self.q[state] = this_state_actions

		return ret_move

	@abc.abstractmethod
	def updatePolicy(*args):
		"""Subclasses of QPolicy must implement function to updatePolicy on reaching terminal state"""
		return

	def persistPolicy(self, filepath = None):
		if self.statefile or filepath:
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

