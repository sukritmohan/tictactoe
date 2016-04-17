import abc

class Player(object):

	def __init__(self, id):
		if (isinstance(id,int) and (id == 1 or id == 2)):
			self.id = id
		else:
			raise Exception('id for a player needs to be either 1 (player 1) or 2 (player 2)')

	@abc.abstractmethod
	def requestMove(*args):
		pass

	def saveState(*args):
		print "Saved No State -- DEFAULT"