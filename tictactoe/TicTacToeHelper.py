

class TicTacToeHelper():

	EMPTY = 0
	SIZE = 3

	REWARD_WIN = 100
	REWARD_DRAW = -5
	REWARD_LOSE = -100
	ONGOING = 0

	@staticmethod
	def getValidMoves(board):
		"""
		Returns the valid moves which can be made on this board. For a move to be valid, the board tile must be empty.
		:param board: tictactoe board
		:return: list of valid moves on board
		"""

		moves = []
		for i in range(TicTacToeHelper.SIZE):
			for j in range(TicTacToeHelper.SIZE):
				if(board[i][j] == TicTacToeHelper.EMPTY):
					moves.append( TicTacToeHelper.getBoardPosition(i, j) )
		return moves

	@staticmethod
	def serializeBoard(board):
		"""Flatten the board to make a string out of it - used to denote board state"""
		return "".join(map(lambda row: "".join( map(lambda t: str(t), row)), board))

	@staticmethod
	def rotateBoard_clockwise(board):
		"""Rotate the board clockwise"""
		return zip(*board[::-1])

	@staticmethod
	def normalizeBoard(board, id):
		"""Normalize the board such that the id passed is represented as 'A', and the other player is represented as 'B'. EMPTY stays EMPTY"""
		return map( \
				lambda row: map(lambda tile: 'A' if tile==id else('B' if tile!=TicTacToeHelper.EMPTY else TicTacToeHelper.EMPTY) , row), \
				board)

	@staticmethod
	def getMoveIndexes(move):
		"""
		From board position, return the board indexes
		Eg getMoveIndexes(5) = (1,1)
		"""
		if move < 0 or move > TicTacToeHelper.SIZE*TicTacToeHelper.SIZE:
			return -1, -1
		i = (move-1)/TicTacToeHelper.SIZE
		j = (move-1) % TicTacToeHelper.SIZE
		return i,j

	@staticmethod
	def getBoardPosition(i, j):
		"""
		From board index i and j, return the board position
		Eg: (1,2) = 6
		"""
		if i < 0 or i >= TicTacToeHelper.SIZE or j < 0 or j >= TicTacToeHelper.SIZE:
			return -1
		return TicTacToeHelper.SIZE*i + j + 1

	#
	@staticmethod
	def getBoardRotatedStates(board):
		"""
		Returns all the symmetric positions of the board, from different starting points by rotating the board 4 times.
		[
			original board,
			original board + clockwise rotation,
			original board + 2*clockwise rotation,
			original board + 3*clockwise rotation
		]
		:param board:
		:return: List of symmetric board positions
		"""
		ret = []
		ret.append(board)

		board_rotated = TicTacToeHelper.rotateBoard_clockwise(board)
		ret.append(board_rotated)

		board_rotated = TicTacToeHelper.rotateBoard_clockwise(board_rotated)
		ret.append(board_rotated)

		board_rotated = TicTacToeHelper.rotateBoard_clockwise(board_rotated)
		ret.append(board_rotated)

		return ret


	@staticmethod
	def reverseRotateMove(move, rotation):
		"""
		Returns the original index position of tile on the board, which is represented by position `move`
		on a board rotated `rotation` times.

		1 | 2 | 3                                  7 | 4 | 1
		--------- 								   ---------
		4 | 5 | 6          --- 1 rotation --->>    8 | 5 | 2
		---------								   _________
		7 | 8 | 9								   9 | 6 | 3

		Eg: reverseRotateMove(7, 1) = 9   (since 9 on the original board is index 7 on the rotated board)

		:param move: Move index on rotated board
		:param rotation: Number of rotations on new board
		:return: Index of number on original board (before rotations)
		"""
		i,j = TicTacToeHelper.getMoveIndexes(move)
		max_index = TicTacToeHelper.SIZE - 1

		if rotation == 0:
			return TicTacToeHelper.getBoardPosition(i,j)
		elif rotation == 1:
			return TicTacToeHelper.getBoardPosition(max_index-j,i)
		elif rotation == 2:
			return TicTacToeHelper.getBoardPosition(max_index-i,max_index-j)
		elif rotation == 3:
			return TicTacToeHelper.getBoardPosition(j,max_index-i)
		else:
			return -1

	@staticmethod
	def rotateMove(move, rotation):
		"""
		Returns the rotated index position of tile on the board rotated `rotation` times.
		
		1 | 2 | 3                                  7 | 4 | 1
		---------                                                                  ---------
		4 | 5 | 6          --- 1 rotation --->>    8 | 5 | 2
		---------                                                                  _________
		7 | 8 | 9                                                                  9 | 6 | 3
		
		Eg: rotateMove(7, 1) = 1   (since 7 on the original board is index 1 on the rotated board)
		
		:param move: Move index on rotated board
		:param rotation: Number of rotations on new board
		:return: Index of number on original board (before rotations)
		"""
		i,j = TicTacToeHelper.getMoveIndexes(move)
		
		if i<0 or j<0:
			return -1
		
		max_index = TicTacToeHelper.SIZE - 1
		
		if rotation == 0:
			return TicTacToeHelper.getBoardPosition(i,j)
		elif rotation == 1:
			return TicTacToeHelper.getBoardPosition(j,max_index-i)
		elif rotation == 2:
			return TicTacToeHelper.getBoardPosition(max_index-i,max_index-j)
		elif rotation == 3:
			return TicTacToeHelper.getBoardPosition(max_index-j,i)
		else:
			return -1
