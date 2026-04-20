import random  # Import random module for AI's random column selection
import sys      # Import sys to check command-line arguments (e.g., --cli flag)

# Attempt to import tkinter for the GUI; if unavailable (e.g., headless server), set tk to None
try:
    import tkinter as tk
    from tkinter import messagebox  # messagebox provides pop-up dialogs (info, warning, error)
except ImportError:
    tk = None  # GUI will not be available; CLI mode will be used as fallback


# ---------------------------------------------------------------------------
# CORE GAME LOGIC — board management, win/draw checking, and AI move generation
# ---------------------------------------------------------------------------

def create_board(rows, cols): 
    """
    Create and return a fresh 2D game board as a list of lists.
    Each cell is initialized to a single space ' ' representing an empty slot.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]


def print_board(board, rows, cols):
    """
    Print the current board state to the terminal.
    Each row's cells are separated by '|', and column indices are shown below.
    """
    for row in board:                                        # Iterate over each row in the board
        print('|'.join(row))                                 # Join cells with '|' and print the row
    print('-' * (cols * 2 - 1))                             # Print a dashed divider scaled to board width
    print(' '.join(str(i) for i in range(cols)))            # Print column index numbers for reference


def drop_piece(board, col, piece, rows):
    """
    Drop a game piece into the specified column.
    Pieces fall to the lowest available (empty) row due to gravity simulation.
    Returns True if the piece was placed successfully, False if the column is full.
    """
    for row in range(rows - 1, -1, -1):  # Scan rows from the bottom upward
        if board[row][col] == ' ':        # Found an empty cell in this column
            board[row][col] = piece       # Place the piece here
            return True                   # Placement successful
    return False                          # Column is completely full; move is invalid


def check_win(board, piece, rows, cols, win_len):
    """
    Check whether the given piece has achieved a winning sequence on the board.
    Checks all four directions: horizontal, vertical, diagonal down-right, diagonal up-right.
    Returns True if a winning sequence of length win_len is found, otherwise False.
    """

    # Horizontal check
    for r in range(rows):                          # Every row is a candidate
        for c in range(cols - win_len + 1):        # Only start where win_len cells fit to the right
            if all(board[r][c + i] == piece for i in range(win_len)):
                return True                        # Found win_len consecutive horizontal cells

    # Vertical check 
    for r in range(rows - win_len + 1):            # Only start where win_len cells fit downward
        for c in range(cols):                      # Every column is a candidate
            if all(board[r + i][c] == piece for i in range(win_len)):
                return True                        # Found win_len consecutive vertical cells

    # Diagonal check (top-left → bottom-right)
    for r in range(rows - win_len + 1):            # Rows with enough room to go down
        for c in range(cols - win_len + 1):        # Columns with enough room to go right
            if all(board[r + i][c + i] == piece for i in range(win_len)):
                return True                        # Found win_len cells along a down-right diagonal

    # Diagonal check (bottom-left → top-right) 
    for r in range(win_len - 1, rows):             # Start from a row deep enough to go upward
        for c in range(cols - win_len + 1):        # Columns with enough room to go right
            if all(board[r - i][c + i] == piece for i in range(win_len)):
                return True                        # Found win_len cells along an up-right diagonal

    return False  # No winning sequence found in any direction


def check_draw(board):
    """
    Determine whether the board is completely full with no empty cells remaining.
    A full board with no winner is a draw.
    Returns True if it's a draw, False if at least one empty cell still exists.
    """
    for row in board:           # Inspect every row
        if ' ' in row:          # An empty cell means the game can continue
            return False        # Not a draw yet
    return True                 # Every cell is occupied — it's a draw


def ai_move(board, cols):
    """
    Determine a move for the AI player by randomly selecting a valid (non-full) column.
    Returns the chosen column index.
    """
    valid_cols = []                          # Collect all columns that still have room
    for c in range(cols):
        if board[0][c] == ' ':              # The top cell of a column is empty → column is playable
            valid_cols.append(c)
    return random.choice(valid_cols)        # Pick one of the valid columns at random



# GUI MODE — tkinter-based graphical interface

class Connect4GUI:

    def __init__(self):
        
        # Initialize the main window and default game settings, then show the setup screen.
        
        self.root = tk.Tk()
        self.root.title("Connect 4")
        

        # Default game configuration values
        self.rows = 6
        self.cols = 7
        self.win_len = 4
        self.mode = '2'     # '1' = two-player, '2' = vs AI
        self.turn = 0       # 0 = Player 1 (X), 1 = Player 2 / AI (O)
        self.board = []     # Will hold the 2D game board
        self.cells = []     # Grid of Label widgets representing board cells
        self.col_buttons = []  # Buttons along the top for column selection

        # tkinter variables bound to the setup form inputs
        self.rows_var = tk.StringVar(value=str(self.rows))
        self.cols_var = tk.StringVar(value=str(self.cols))
        self.win_var = tk.StringVar(value=str(self.win_len))
        self.mode_var = tk.StringVar(value=self.mode)

        self.status_label = None    # Label widget that shows whose turn it is

        self.create_setup_screen()  # Display the settings form before starting a game
        self.root.mainloop()        # Start the tkinter event loop

    def create_setup_screen(self):
       # Build and display the game configuration screen.
        # Clears any existing widgets and presents input fields for rows, columns, 
        # win length, and game mode, plus a Start Game button.
        
        for widget in self.root.winfo_children():   # Remove all existing widgets from the window
            widget.destroy()

        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.pack()

        # Title label
        tk.Label(frame, text="Connect 4", font=("Helvetica", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 10))

        # Row count input
        tk.Label(frame, text="Rows:").grid(row=1, column=0, sticky="e", pady=4)
        tk.Entry(frame, textvariable=self.rows_var, width=5).grid(row=1, column=1, sticky="w", pady=4)

        # Column count input
        tk.Label(frame, text="Columns:").grid(row=2, column=0, sticky="e", pady=4)
        tk.Entry(frame, textvariable=self.cols_var, width=5).grid(row=2, column=1, sticky="w", pady=4)

        # Win length input
        tk.Label(frame, text="Win length:").grid(row=3, column=0, sticky="e", pady=4)
        tk.Entry(frame, textvariable=self.win_var, width=5).grid(row=3, column=1, sticky="w", pady=4)

        # Mode selection via radio buttons
        tk.Label(frame, text="Mode:").grid(row=4, column=0, sticky="e", pady=4)
        tk.Radiobutton(frame, text="Two player", variable=self.mode_var, value='1').grid(
            row=4, column=1, sticky="w")
        tk.Radiobutton(frame, text="Vs AI", variable=self.mode_var, value='2').grid(
            row=5, column=1, sticky="w")

        # Start button that validates inputs and launches the game
        tk.Button(frame, text="Start Game", command=self.start_game, width=20).grid(
            row=6, column=0, columnspan=2, pady=(10, 0))

    def start_game(self):
       
       # Validate the setup form inputs and initialize a new game.
       # Shows error dialogs for invalid values; otherwise builds the game screen.
     
        try:
            rows = int(self.rows_var.get())       # Parse rows input as integer
            cols = int(self.cols_var.get())       # Parse columns input as integer
            win_len = int(self.win_var.get())     # Parse win length input as integer
        except ValueError:
            messagebox.showerror("Invalid input", "Rows, columns, and win length must be whole numbers.")
            return

        # Enforce minimum board dimensions
        if rows < 4 or cols < 4:
            messagebox.showerror("Invalid input", "Rows and columns must be at least 4.")
            return

        # Win length must be achievable within the board's dimensions
        if win_len < 3 or win_len > rows or win_len > cols:
            messagebox.showerror("Invalid input",
                                 "Win length must be at least 3 and no greater than rows or columns.")
            return

        # Store validated settings and reset game state
        self.rows = rows
        self.cols = cols
        self.win_len = win_len
        self.mode = self.mode_var.get()
        self.turn = 0                              # Player 1 always goes first
        self.board = create_board(rows, cols)      # Create a fresh empty board

        self.build_game_screen()   # Construct the game UI widgets
        self.draw_board()          # Render the initial (empty) board state

    def build_game_screen(self):
        """
        Construct the full game interface: status label, board grid, column buttons,
        and bottom navigation buttons (New Game / Quit).
        Replaces any previously displayed widgets.
        """
        for widget in self.root.winfo_children():   # Clear the window before rebuilding
            widget.destroy()

        # --- Status area (shows whose turn it is) ---
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack()
        self.status_label = tk.Label(top_frame, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=(0, 8))

        # --- Main board grid ---
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)

        # --- Column selection buttons (one per column, above the board) ---
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=(0, 10))

        self.col_buttons = []
        for col in range(self.cols):
            # Each button is labeled with its column index and drops a piece when clicked
            button = tk.Button(button_frame, text=str(col), width=4,
                               command=lambda col=col: self.on_column_click(col))
            button.grid(row=0, column=col, padx=2)
            self.col_buttons.append(button)

        # --- Cell labels that visually represent the board grid ---
        self.cells = []
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                label = tk.Label(self.board_frame, text=" ", width=4, height=2,
                                 borderwidth=1, relief="ridge", font=("Helvetica", 14))
                label.grid(row=row, column=col, padx=1, pady=1)
                row_cells.append(label)
            self.cells.append(row_cells)

        # --- Bottom navigation buttons ---
        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack()
        tk.Button(bottom_frame, text="New Game", command=self.create_setup_screen, width=12).pack(
            side="left", padx=6)
        tk.Button(bottom_frame, text="Quit", command=self.root.destroy, width=12).pack(
            side="left", padx=6)

    def draw_board(self):
        """
        Refresh the visual board to reflect the current state of self.board.
        Colors cells blue for Player 1 (X), red for Player 2/AI (O), and light grey when empty.
        Also updates the status label with the current player's turn.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                value = self.board[row][col]        # Get the piece at this cell (' ', 'X', or 'O')
                label = self.cells[row][col]        # Get the corresponding tkinter Label widget
                label.config(text=value if value != ' ' else ' ')   # Show piece symbol or blank

                # Apply background colour based on which player occupies the cell
                if value == 'X':
                    label.config(bg="#9dd1ff")      # Blue tint for Player 1
                elif value == 'O':
                    label.config(bg="#ffb6b6")      # Red tint for Player 2 / AI
                else:
                    label.config(bg="#f0f0f0")      # Neutral grey for empty cells

        # Update the status label to indicate whose turn it currently is
        if self.turn == 0:
            self.status_label.config(text="Player 1 (X) turn")
        else:
            self.status_label.config(
                text="Player 2 (O) turn" if self.mode == '1' else "AI (O) turn")

    def on_column_click(self, col):
        """
        Handle a column button click from the human player.
        Ignored if it is the AI's turn (prevents human input during AI moves).
        Attempts to drop the current player's piece into the selected column.
        Shows a warning if the chosen column is already full.
        """
        if self.turn == 1 and self.mode == '2':
            return  # Block input during the AI's turn in vs-AI mode

        piece = 'X' if self.turn == 0 else 'O'      # Determine which piece to place
        row = drop_piece(self.board, col, piece, self.rows)  # Attempt the drop

        if row == -1:   # drop_piece returns -1 (or False) when the column is full
            messagebox.showwarning("Column full", "That column is full. Choose a different one.")
            return

        self.after_move()   # Process the result of the move

    def animate_drop(self, col, row, piece):
        """
        (Unused in current grid-based layout — intended for a canvas-based version)
        Animates a piece falling from the top of the column to its final row position.
        """
        x = col * self.cell_size + self.cell_size // 2
        start_y = self.rows * self.cell_size + self.cell_size // 2
        target_y = (self.rows - 1 - row) * self.cell_size + self.cell_size // 2
        color = "#e74c3c" if piece == 'X' else "#f1c40f"
        # Draw the falling piece as an oval on the canvas
        id = self.canvas.create_oval(
            x - self.piece_radius + 3, start_y - self.piece_radius + 3,
            x + self.piece_radius - 3, start_y + self.piece_radius - 3,
            fill=color, outline="#000000", width=2)
        dy = 10  # Number of pixels to move per animation frame
        self.animate_step(id, dy, target_y)

    def animate_step(self, id, dy, target_y):
        """
        (Unused in current grid-based layout — supports animate_drop)
        Recursively moves the falling piece oval downward by dy pixels per frame
        until it reaches the target row position, then cleans up and triggers after_move.
        """
        coords = self.canvas.coords(id)
        current_y = coords[1] + self.piece_radius      # Calculate current bottom edge of the oval
        if current_y >= target_y:                       # Piece has reached its destination row
            self.canvas.delete(id)                      # Remove the animated oval from canvas
            self.after_move()                           # Process win/draw/turn logic
            return
        self.canvas.move(id, 0, dy)                     # Move the oval downward by dy pixels
        self.root.after(30, lambda: self.animate_step(id, dy, target_y))  # Schedule next frame in 30ms

    def after_move(self):
        """
        Called after every piece placement (by human or AI) to check game outcomes.
        Checks for a win or draw; if neither, advances the turn and triggers an AI move if needed.
        Disables column buttons when the game ends to prevent further input.
        """
        piece = 'X' if self.turn == 0 else 'O'   # The piece that was just placed

        # Check whether the last move resulted in a win
        if check_win(self.board, piece, self.rows, self.cols, self.win_len):
            self.draw_board()  # Render the final board state before showing the result
            winner = "Player 1" if self.turn == 0 else ("Player 2" if self.mode == '1' else "AI")
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.set_column_buttons_state("disabled")   # Lock the board — game is over
            return

        # Check whether the board is completely full (draw)
        if check_draw(self.board):
            self.draw_board()
            messagebox.showinfo("Game Over", "The game is a draw.")
            self.set_column_buttons_state("disabled")   # Lock the board — game is over
            return

        # No winner or draw — advance to the next player's turn
        self.turn = 1 - self.turn    # Toggle between 0 (Player 1) and 1 (Player 2 / AI)
        self.draw_board()            # Refresh the board display for the new turn

        # If playing vs AI and it's now the AI's turn, schedule the AI move with a short delay
        if self.mode == '2' and self.turn == 1:
            self.root.after(250, self.ai_turn)   # 250ms pause makes the AI feel more natural

    def ai_turn(self):
        """
        Execute the AI's move by selecting a random valid column and dropping its piece.
        Skips the move if the board is already full (safety guard against edge cases).
        """
        if check_draw(self.board):
            return  # Nothing to do if there are no valid moves left

        col = ai_move(self.board, self.cols)          # Let the AI pick a column
        drop_piece(self.board, col, 'O', self.rows)   # Drop the AI's piece ('O') into that column
        self.after_move()                             # Check for win/draw and advance turn

    def set_column_buttons_state(self, state):
        """
        Enable or disable all column selection buttons.
        Pass 'disabled' to lock the board at game end, or 'normal' to re-enable.
        """
        for button in self.col_buttons:
            button.config(state=state)


# ---------------------------------------------------------------------------
# CLI MODE — terminal-based interface (fallback when tkinter is unavailable)
# ---------------------------------------------------------------------------

def cli_main():
    """
    Run the game entirely in the terminal using text input and printed output.
    Prompts the user to configure board dimensions, win length, and game mode,
    then loops until a winner is found or the board is full.
    """

    # --- Board size configuration ---
    while True:
        try:
            rows = int(input("Enter rows (min 4): "))
            cols = int(input("Enter columns (min 4): "))
            if rows >= 4 and cols >= 4:    # Enforce minimum playable dimensions
                break
        except ValueError:
            pass                           # Re-prompt on non-integer input
        print("Invalid input.")

    # --- Win length configuration ---
    while True:
        try:
            win_len = int(input("How many in a row to win? "))
            if win_len <= rows and win_len <= cols and win_len >= 3:
                break    # Win length must fit within the board and be at least 3
        except ValueError:
            pass
        print("Invalid win length.")

    # --- Game mode selection ---
    while True:
        mode = input("1 = Two Player, 2 = vs AI: ")
        if mode in ['1', '2']:
            break        # Only accept '1' or '2' as valid mode inputs

    board = create_board(rows, cols)   # Create the initial empty board
    turn = 0                           # Player 1 (X) always goes first

    # --- Main game loop ---
    while True:
        print_board(board, rows, cols)   # Display current board state before each move

        if turn == 0:
            # --- Player 1's turn ---
            piece = 'X'
            print("Player 1 turn")
            while True:
                try:
                    col = int(input(f"Choose column (0-{cols-1}): "))
                    if 0 <= col < cols:   # Ensure the column index is within bounds
                        break
                except ValueError:
                    pass
                print("Invalid column.")
        else:
            # --- Player 2 or AI's turn ---
            piece = 'O'
            if mode == '1':
                # Human Player 2 selects a column
                print("Player 2 turn")
                while True:
                    try:
                        col = int(input(f"Choose column (0-{cols-1}): "))
                        if 0 <= col < cols:
                            break
                    except ValueError:
                        pass
                    print("Invalid column.")
            else:
                # AI randomly selects a valid column
                print("AI turn")
                col = ai_move(board, cols)

        # Attempt to place the piece; warn and retry if column is full
        if not drop_piece(board, col, piece, rows):
            print("Column full.")
            continue   # Skip to the next iteration without switching turns

        # Check if the move just played wins the game
        if check_win(board, piece, rows, cols, win_len):
            print_board(board, rows, cols)
            print(f"Player {turn + 1} wins!")
            break      # Exit the game loop — we have a winner

        # Check for a draw (board completely filled with no winner)
        if check_draw(board):
            print_board(board, rows, cols)
            print("Game is a draw.")
            break      # Exit the game loop — it's a draw

        turn = 1 - turn   # Switch turns: 0 → 1, or 1 → 0


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    """
    Determine which interface to launch:
    - CLI mode if '--cli' flag is passed or tkinter is not available.
    - GUI mode otherwise.
    """
    if '--cli' in sys.argv or tk is None:
        cli_main()   # Run the terminal-based version
    else:
        Connect4GUI()   # Launch the graphical version


if __name__ == "__main__":
    main()   # Execute main() only when the script is run directly (not imported)