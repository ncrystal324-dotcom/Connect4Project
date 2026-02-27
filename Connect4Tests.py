
# Test suite for basic Connect 4 functionality

def test_create_board():
    board = create_board()
    assert len(board) == 6, "Board should have 6 rows"
    assert all(len(row) == 7 for row in board), "Each row should have 7 columns"
    assert all(cell == ' ' for row in board for cell in row), "All cells should be empty"
    print("test_create_board passed")

def test_drop_piece():
    board = create_board()
    # Test dropping piece in empty column
    assert drop_piece(board, 0, 'X') == True
    assert board[-1][0] == 'X', "Piece should land in bottom row"

    # Fill column and test full
    for _ in range(5):
        drop_piece(board, 0, 'O')
    assert drop_piece(board, 0, 'X') == False, "Column full, should not allow piece"
    print("test_drop_piece passed")

# Uncomment once win detection is implemented
# def test_win_detection():
#     # Horizontal, vertical, and diagonal win tests
#     pass

test_create_board()
test_drop_piece()
# test_win_detection()