import itertools

class TicTacToeHelper():

	EMPTY = 0

	@staticmethod
	def getValidMoves(board):
		size = len(board)

		moves = []
		for i in range(size):
			for j in range(size):
				if(board[i][j] == TicTacToeHelper.EMPTY):
					moves.append(3*i+j+1)
		return moves

	#Flatten the board and make a string out of it
	@staticmethod
	def serializeBoard(board):
		return "".join(map(lambda row: "".join( map(lambda t: str(t), row)), board))

	@staticmethod
	def flattenBoard(board):
		return list(itertools.chain.from_iterable(board))

	@staticmethod
	def rotateBoard_clockwise(board):
		return zip(*board[::-1])

	#Normalize the board such that the id passed is represented as 'A', and the other player is represented as 'B'. EMPTY stays EMPTY
	@staticmethod
	def normalizeBoard(board, id):
		return map( \
				lambda row: map(lambda tile: 'A' if tile==id else('B' if tile!=TicTacToeHelper.EMPTY else TicTacToeHelper.EMPTY) , row), \
				board)