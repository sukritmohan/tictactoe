import abc

class Player(object):

	def __init__(self, id):
		if (isinstance(id,int) and (id == 1 or id == 2)):
			self.id = id
		else:
			raise Exception('id for a player needs to be either 1 (player 1) or 2 (player 2)')

	@abc.abstractmethod
	def requestMove(*args):
		"""This is called to request the player to make a move. Subclasses must implement this function"""
		pass

	def saveState(*args):
		"""If the player maintains any state while playing, this is the chance to persist to file."""
		pass

	def updateState(*args):
		"""If the player needs to update its state during gameplay, call this function"""
		pass

	def newGame(*args):
		"""Any preparatory work that a player needs to do at the start of a game"""
		pass