import os
import json
from QPolicy import QPolicy

class SARSAPolicy(QPolicy):

	def __init__(self, data = {}):
		self.q = data

	def savePolicy(self):
		print "SAVE THIS POLICY"

