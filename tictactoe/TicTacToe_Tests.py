import unittest
from TicTacToeBoard import TicTacToeBoard
from TicTacToeHelper import TicTacToeHelper
from TicTacToeEngine import TicTacToeEngine

class TicTacToeBoard_Test(unittest.TestCase):

	def setUp(self):
		self.board = TicTacToeBoard()
		self.board.makeMove(1,4)
		self.board.makeMove(2,6)
		self.board.makeMove(1,7)

	def test_boardState(self):
		e = TicTacToeHelper.EMPTY
		state = [[e,e,e],[1,e,2],[1,e,e]]
		self.assertItemsEqual(self.board.getBoardState(), state)

	def test_checkMove(self):
		self.assertFalse(self.board.isValidMove(6))
		self.assertFalse(self.board.makeMove(1, 4))
		self.assertTrue(self.board.makeMove(1, 5))


class TicTacToeHelper_Test(unittest.TestCase):

	def setUp(self):
		self.board = TicTacToeBoard()
		self.board.makeMove(1,4)
		self.board.makeMove(2,6)
		self.board.makeMove(1,7)

	def test_validMoves(self):
		valid_moves = [1,2,3,5,8,9]
		self.assertEqual(TicTacToeHelper.getValidMoves(self.board.getBoardState()), valid_moves)

	def test_serializeBoard(self):
		flat_board = "000102100"
		self.assertEqual(TicTacToeHelper.serializeBoard(self.board.getBoardState()), flat_board)

	def test_rotateBoard_clockwise(self):
		e = TicTacToeHelper.EMPTY
		rotated_board = [(1, 1, e), (e, e, e), (e, 2, e)]
		self.assertEqual(TicTacToeHelper.rotateBoard_clockwise(self.board.getBoardState()), rotated_board)

	def test_normalizeBoard(self):
		norm1 = [[0, 0, 0], ['A', 0, 'B'], ['A', 0, 0]]
		norm2 = [[0, 0, 0], ['B', 0, 'A'], ['B', 0, 0]]
		self.assertEqual(TicTacToeHelper.normalizeBoard(self.board.getBoardState(), 1), norm1)
		self.assertEqual(TicTacToeHelper.normalizeBoard(self.board.getBoardState(), 2), norm2)

	def test_getMoveIndexes(self):
		self.assertEqual(TicTacToeHelper.getMoveIndexes(5), (1,1))
		self.assertEqual(TicTacToeHelper.getMoveIndexes(1), (0,0))
		self.assertEqual(TicTacToeHelper.getMoveIndexes(9), (2,2))
		self.assertEqual(TicTacToeHelper.getMoveIndexes(-1), (-1,-1))
		self.assertEqual(TicTacToeHelper.getMoveIndexes(50), (-1,-1))

	def test_getBoardPosition(self):
		self.assertEqual(TicTacToeHelper.getBoardPosition(1,1), 5)
		self.assertEqual(TicTacToeHelper.getBoardPosition(1,2), 6)
		self.assertEqual(TicTacToeHelper.getBoardPosition(1,3), -1)

	def test_getSymmetricBoardStates(self):
		sym_states = [[[0, 0, 0], [1, 0, 2], [1, 0, 0]],
					  [(1, 1, 0), (0, 0, 0), (0, 2, 0)],
					  [(0, 0, 1), (2, 0, 1), (0, 0, 0)],
					  [(0, 2, 0), (0, 0, 0), (0, 1, 1)]]
		self.assertEqual(TicTacToeHelper.getBoardRotatedStates(self.board.getBoardState()), sym_states)

	def test_reverseRotateMove(self):
		self.assertEqual(TicTacToeHelper.reverseRotateMove(7, 0), 7)
		self.assertEqual(TicTacToeHelper.reverseRotateMove(7, 1), 9)
		self.assertEqual(TicTacToeHelper.reverseRotateMove(7, 2), 3)
		self.assertEqual(TicTacToeHelper.reverseRotateMove(7, 3), 1)
		self.assertEqual(TicTacToeHelper.reverseRotateMove(7, 4), -1)


def suite():
	board_tests = ['test_boardState', 'test_checkMove']
	board_suit = unittest.TestSuite(map(TicTacToeBoard_Test, board_tests))

	helper_tests = ['test_validMoves',
					'test_serializeBoard',
					'test_rotateBoard_clockwise',
					'test_normalizeBoard',
					'test_getMoveIndexes',
					'test_getBoardPosition',
					'test_getSymmetricBoardStates',
					'test_reverseRotateMove'
					]

	helper_suit = unittest.TestSuite(map(TicTacToeHelper_Test, helper_tests))

	return unittest.TestSuite([board_suit, helper_suit])


if __name__ == '__main__':
	suite = suite()
	unittest.TextTestRunner(verbosity=2).run(suite)