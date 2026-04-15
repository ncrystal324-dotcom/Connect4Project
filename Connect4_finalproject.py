
import random  # Import random module for AI's random column selection

# Function to create an empty game board as a 2D list
def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]  # Fill every cell with a space (empty)


# Function to display the current board state in the terminal
def print_board(board, rows, cols):
    for row in board:  # Loop through each row in the board
        print('|'.join(row))  # Print each row's cells separated by '|'
    print('-' * (cols * 2 - 1))  # Print a horizontal divider line scaled to board width
    print(' '.join(str(i) for i in range(cols)))  # Print column index numbers below the board


# Function to drop a piece into the lowest available cell in a given column
def drop_piece(board, col, piece, rows):
    for row in range(rows - 1, -1, -1):  # Iterate rows from bottom to top
        if board[row][col] == ' ':  # Check if the cell is empty
            board[row][col] = piece  # Place the piece in the empty cell
            return True  # Return True to indicate the move was successful
    return False  # Return False if the column is completely full


# Function to check if a given piece has achieved the win condition
def check_win(board, piece, rows, cols, win_len):

    # Check for a horizontal win
    for r in range(rows):  # Loop through every row
        for c in range(cols - win_len + 1):  # Loop through valid starting columns
            if all(board[r][c+i] == piece for i in range(win_len)):  # Check win_len consecutive cells horizontally
                return True  # Horizontal win found

    # Check for a vertical win
    for r in range(rows - win_len + 1):  # Loop through valid starting rows
        for c in range(cols):  # Loop through every column
            if all(board[r+i][c] == piece for i in range(win_len)):  # Check win_len consecutive cells vertically
                return True  # Vertical win found

    # Check for a diagonal win (top-left to bottom-right)
    for r in range(rows - win_len + 1):  # Loop through valid starting rows
        for c in range(cols - win_len + 1):  # Loop through valid starting columns
            if all(board[r+i][c+i] == piece for i in range(win_len)):  # Check win_len cells diagonally down-right
                return True  # Diagonal down-right win found

    # Check for a diagonal win (bottom-left to top-right)
    for r in range(win_len - 1, rows):  # Loop through valid starting rows (from bottom)
        for c in range(cols - win_len + 1):  # Loop through valid starting columns
            if all(board[r-i][c+i] == piece for i in range(win_len)):  # Check win_len cells diagonally up-right
                return True  # Diagonal up-right win found

    return False  # No winning condition found, return False


# Function to check if the board is completely full (draw condition)
def check_draw(board):
    for row in board:  # Loop through every row
        if ' ' in row:  # If any empty cell exists in the row
            return False  # Board is not full, not a draw
    return True  # No empty cells found, it's a draw


# Function to determine the AI's move (random valid column)
def ai_move(board, cols):
    valid_cols = []  # Initialize empty list to store playable columns
    for c in range(cols):  # Loop through every column
        if board[0][c] == ' ':  # Check if the top cell of the column is empty (column not full)
            valid_cols.append(c)  # Add the column to the valid options
    return random.choice(valid_cols)  # Randomly select and return one of the valid columns


# Main game function that controls setup and the game loop
def main():

    # Prompt user to set board size with validation
    while True:  # Loop until valid input is received
        try:
            rows = int(input("Enter rows (min 4): "))  # Get number of rows from user
            cols = int(input("Enter columns (min 4): "))  # Get number of columns from user
            if rows >= 4 and cols >= 4:  # Ensure both dimensions meet the minimum size
                break  # Valid input received, exit loop
        except:  # Catch any non-integer input
            pass  # Ignore the error and re-prompt
        print("Invalid input.")  # Notify user of invalid input

    # Prompt user to set the win length with validation
    while True:  # Loop until valid input is received
        try:
            win_len = int(input("How many in a row to win? "))  # Get the win condition length
            if win_len <= rows and win_len <= cols and win_len >= 3:  # Ensure win length fits the board and is at least 3
                break  # Valid input received, exit loop
        except:  # Catch any non-integer input
            pass  # Ignore the error and re-prompt
        print("Invalid win length.")  # Notify user of invalid input

    # Prompt user to select game mode with validation
    while True:  # Loop until valid input is received
        mode = input("1 = Two Player, 2 = vs AI: ")  # Get game mode choice
        if mode in ['1', '2']:  # Check if the input is a valid option
            break  # Valid input received, exit loop

    board = create_board(rows, cols)  # Initialize the game board with the chosen dimensions
    turn = 0  # Set the starting turn to Player 1 (0 = Player 1, 1 = Player 2/AI)

    while True:  # Main game loop — runs until a win or draw

        print_board(board, rows, cols)  # Display the current board state

        if turn == 0:  # Player 1's turn
            piece = 'X'  # Assign 'X' as Player 1's piece
            print("Player 1 turn")  # Announce Player 1's turn

            while True:  # Loop until a valid column is chosen
                try:
                    col = int(input(f"Choose column (0-{cols-1}): "))  # Prompt Player 1 for a column
                    if 0 <= col < cols:  # Check if the column is within valid range
                        break  # Valid column chosen, exit loop
                except:  # Catch non-integer input
                    pass  # Ignore the error and re-prompt
                print("Invalid column.")  # Notify user of invalid input

        else:  # Player 2 or AI's turn
            piece = 'O'  # Assign 'O' as Player 2/AI's piece

            if mode == '1':  # Two-player mode
                print("Player 2 turn")  # Announce Player 2's turn

                while True:  # Loop until a valid column is chosen
                    try:
                        col = int(input(f"Choose column (0-{cols-1}): "))  # Prompt Player 2 for a column
                        if 0 <= col < cols:  # Check if the column is within valid range
                            break  # Valid column chosen, exit loop
                    except:  # Catch non-integer input
                        pass  # Ignore the error and re-prompt
                    print("Invalid column.")  # Notify user of invalid input

            else:  # AI mode
                print("AI turn")  # Announce the AI's turn
                col = ai_move(board, cols)  # Get the AI's randomly chosen column

        if not drop_piece(board, col, piece, rows):  # Attempt to place the piece; check if column is full
            print("Column full.")  # Notify user the column is full
            continue  # Skip to the next iteration without switching turns

        if check_win(board, piece, rows, cols, win_len):  # Check if the current move won the game
            print_board(board, rows, cols)  # Display the final board state
            print(f"Player {turn+1} wins!")  # Announce the winner
            break  # End the game loop

        if check_draw(board):  # Check if the board is full with no winner
            print_board(board, rows, cols)  # Display the final board state
            print("Game is a draw.")  # Announce the draw
            break  # End the game loop

        turn = 1 - turn  # Switch turns: 0 becomes 1, 1 becomes 0


if __name__ == "__main__":  # Only run main() if this script is executed directly (not imported)
    main()  # Start the game