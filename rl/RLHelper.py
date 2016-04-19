import itertools
import copy
import os
import pickle
from SARSAPolicy import SARSAPolicy
from QLearningPolicy import QLearningPolicy


class RLHelper():


	@staticmethod
	def slidingAverage(list, window_length = 4):
		return map(lambda sl: sum(sl) / float(len(sl)), [list[i:i+window_length] for i in xrange(len(list)-window_length-1)])

	@classmethod
	def loadModel(cls, statefile):
		"""
		Load the model from the statefile given. If statefile doesn't exist, or is empty, start creating a new model
		:param statefile: Filepath of Reinforcement Learning Policy Model
		"""
		try:
			if not os.path.exists(statefile):
				open(statefile, 'w').close()
				state = {}
			else:
				state = pickle.load( open (statefile, 'rb'))
		except Exception, e:
			print e
			print "\nERROR: Couldn't open model file for RLBotPlayer : %s\n\n" % statefile
			state = {}

		if state.get('policy', "") == 'sarsa':
			policy = SARSAPolicy(state, statefile)
		else:
			policy =QLearningPolicy(state, statefile)

		return policy

	@classmethod
	def getNewModel(cls, policytype):
		if(policytype == 'sarsa'):
			policy = SARSAPolicy()
		else:
			policy = QLearningPolicy()

		return policy