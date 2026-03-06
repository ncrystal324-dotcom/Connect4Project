# Constants that define the size of the Connect 4 board
ROWS = 6
COLS = 7


def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    for row in board:
        print('|'.join(row))
    print('-' * (COLS * 2 - 1))
    print(' '.join(str(i) for i in range(COLS)))


def drop_piece(board, col, piece):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = piece
            return True
    return False


def check_win(board, piece):

    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False


def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True


def main():

    board = create_board()
    turn = 0

    while True:

        print_board(board)

        if turn == 0:
            piece = 'X'
            print("Player 1 turn")
        else:
            piece = 'O'
            print("Player 2 turn")

        # safe input loop
        while True:
            try:
                col = int(input("Choose column (0-6): "))
                if 0 <= col <= 6:
                    break
                else:
                    print("Enter a number from 0 to 6.")
            except:
                print("Enter a number from 0 to 6.")

        if not drop_piece(board, col, piece):
            print("Column full. Try again.")
            continue

        if check_win(board, piece):
            print_board(board)
            print(f"Player {turn+1} wins!")
            break

        if check_draw(board):
            print_board(board)
            print("Game is a draw.")
            break

        turn = 1 - turn


if __name__ == "__main__":
    main()
