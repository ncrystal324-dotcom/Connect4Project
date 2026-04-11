import random

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board, rows, cols):
    for row in board:
        print('|'.join(row))
    print('-' * (cols * 2 - 1))
    print(' '.join(str(i) for i in range(cols)))


def drop_piece(board, col, piece, rows):
    for row in range(rows - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = piece
            return True
    return False


def check_win(board, piece, rows, cols, win_len):

    # horizontal
    for r in range(rows):
        for c in range(cols - win_len + 1):
            if all(board[r][c+i] == piece for i in range(win_len)):
                return True

    # vertical
    for r in range(rows - win_len + 1):
        for c in range(cols):
            if all(board[r+i][c] == piece for i in range(win_len)):
                return True

    # diagonal down-right
    for r in range(rows - win_len + 1):
        for c in range(cols - win_len + 1):
            if all(board[r+i][c+i] == piece for i in range(win_len)):
                return True

    # diagonal up-right
    for r in range(win_len - 1, rows):
        for c in range(cols - win_len + 1):
            if all(board[r-i][c+i] == piece for i in range(win_len)):
                return True

    return False


def check_draw(board):
    for row in board:
        if ' ' in row:
            return False
    return True


def ai_move(board, cols):
    valid_cols = []
    for c in range(cols):
        if board[0][c] == ' ':
            valid_cols.append(c)
    return random.choice(valid_cols)


def main():

    # board size
    while True:
        try:
            rows = int(input("Enter rows (min 4): "))
            cols = int(input("Enter columns (min 4): "))
            if rows >= 4 and cols >= 4:
                break
        except:
            pass
        print("Invalid input.")

    # win condition
    while True:
        try:
            win_len = int(input("How many in a row to win? "))
            if win_len <= rows and win_len <= cols and win_len >= 3:
                break
        except:
            pass
        print("Invalid win length.")

    # game mode
    while True:
        mode = input("1 = Two Player, 2 = vs AI: ")
        if mode in ['1', '2']:
            break

    board = create_board(rows, cols)
    turn = 0

    while True:

        print_board(board, rows, cols)

        if turn == 0:
            piece = 'X'
            print("Player 1 turn")

            while True:
                try:
                    col = int(input(f"Choose column (0-{cols-1}): "))
                    if 0 <= col < cols:
                        break
                except:
                    pass
                print("Invalid column.")

        else:
            piece = 'O'

            if mode == '1':
                print("Player 2 turn")

                while True:
                    try:
                        col = int(input(f"Choose column (0-{cols-1}): "))
                        if 0 <= col < cols:
                            break
                    except:
                        pass
                    print("Invalid column.")

            else:
                print("AI turn")
                col = ai_move(board, cols)

        if not drop_piece(board, col, piece, rows):
            print("Column full.")
            continue

        if check_win(board, piece, rows, cols, win_len):
            print_board(board, rows, cols)
            print(f"Player {turn+1} wins!")
            break

        if check_draw(board):
            print_board(board, rows, cols)
            print("Game is a draw.")
            break

        turn = 1 - turn


if __name__ == "__main__":
    main()
