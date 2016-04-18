import copy
import json

class QPolicy(object):

	def __init__(self, model = {}):
		self.q = model.get('model', {})
		self.episode_rewards = model.get('rewards', [])

	def getQ(self):
		return copy.deepcopy(self.q)

	def savePolicy(self):
		pass

	def saveToFile(self, filepath, policytype):
		qlmodel = {}
		qlmodel['policy'] = policytype
		qlmodel['model'] = self.q
		qlmodel['rewards'] = self.episode_rewards

		with open(filepath, 'w') as outfile:
			json.dump(qlmodel, outfile)