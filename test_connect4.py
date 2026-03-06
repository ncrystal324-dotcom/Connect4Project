import unittest
from loops_tulane import create_board, drop_piece, check_win, check_draw, ROWS, COLS


class TestConnect4(unittest.TestCase):

    def test_create_board_size(self):
        board = create_board()
        self.assertEqual(len(board), ROWS)
        self.assertEqual(len(board[0]), COLS)


    def test_drop_piece_bottom(self):
        board = create_board()
        drop_piece(board, 0, 'X')
        self.assertEqual(board[ROWS-1][0], 'X')


    def test_drop_piece_stack(self):
        board = create_board()
        drop_piece(board, 0, 'X')
        drop_piece(board, 0, 'O')

        self.assertEqual(board[ROWS-1][0], 'X')
        self.assertEqual(board[ROWS-2][0], 'O')


    def test_horizontal_win(self):
        board = create_board()

        for c in range(4):
            drop_piece(board, c, 'X')

        self.assertTrue(check_win(board, 'X'))


    def test_vertical_win(self):
        board = create_board()

        for i in range(4):
            drop_piece(board, 0, 'O')

        self.assertTrue(check_win(board, 'O'))


    def test_diagonal_win(self):
        board = create_board()

        drop_piece(board,0,'X')

        drop_piece(board,1,'O')
        drop_piece(board,1,'X')

        drop_piece(board,2,'O')
        drop_piece(board,2,'O')
        drop_piece(board,2,'X')

        drop_piece(board,3,'O')
        drop_piece(board,3,'O')
        drop_piece(board,3,'O')
        drop_piece(board,3,'X')

        self.assertTrue(check_win(board,'X'))


    def test_draw(self):
        board = create_board()

        piece = 'X'
        for r in range(ROWS):
            for c in range(COLS):
                board[r][c] = piece
                piece = 'O' if piece == 'X' else 'X'

        self.assertTrue(check_draw(board))


if __name__ == "__main__":
    unittest.main()