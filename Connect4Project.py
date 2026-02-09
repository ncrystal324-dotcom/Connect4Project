# Constants that define the size of the Connect 4 board
ROWS = 6
COLS = 7


def create_board():
    """
    Creates and returns an empty Connect 4 board.

    The board is represented as a list of lists (2D list),
    where each inner list represents a row.
    Each cell starts as a blank space ' '.

    Example structure:
    [
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ...
    ]
    """
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """
    Prints the current state of the board to the terminal.

    Each row is printed with '|' separating the columns.
    A line of dashes is printed at the bottom for readability.

    NOTE: This function only displays the board.
    It does not show column numbers yet, which may confuse users.
    """
    for row in board:
        print('|'.join(row))
    print('-' * (COLS * 2 - 1))


def drop_piece(board, col, piece):
    """
    Attempts to drop a piece ('X' or 'O') into the specified column.

    The function starts checking from the bottom row upward,
    which matches how Connect 4 works in real life.

    Parameters:
    - board: the current game board
    - col: the column index chosen by the player
    - piece: the player's symbol ('X' or 'O')

    Returns:
    - True if the piece was successfully placed
    - False if the column is already full

    NOTE: This function assumes the column index is valid.
    Input validation is not handled here.
    """
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = piece
            return True
    return False


def main():
    """
    Main game loop for the Connect 4 game.

    This function:
    - Initializes the board
    - Alternates turns between Player 1 and Player 2
    - Prompts players for column input
    - Updates and prints the board after each move

    MISSING FEATURES:
    - Win detection
    - Draw detection
    - Robust input validation
    """
    board = create_board()
    turn = 0  # 0 = Player 1, 1 = Player 2

    while True:
        print_board(board)

        # Ask the current player to choose a column
        col = int(input(f"Player {turn + 1}, choose column (0-{COLS - 1}): "))

        # Determine which piece to drop based on the current turn
        piece = 'X' if turn == 0 else 'O'

        if drop_piece(board, col, piece):
            # Switch turns if the move was successful
            turn = 1 - turn
        else:
            print("Column full! Try again.")


# This ensures the game only runs when this file is executed directly
if __name__ == "__main__":
    main()