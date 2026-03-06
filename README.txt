# Connect 4 Python Game

## Description

This program implements a simple **two-player Connect 4 game** in Python that runs in the terminal.

Players take turns dropping pieces into a **6 x 7 board**.

* **Player 1** uses the piece `X`
* **Player 2** uses the piece `O`

The goal is to be the first player to connect **four pieces in a row**. A win can occur:

* Horizontally
* Vertically
* Diagonally

If the board fills up and no player connects four pieces, the game ends in a **draw**.

The project also includes a **test suite** that automatically checks the core game functions.

---

## Files Included

* `midterm_connect4.py` – main Connect 4 game program
* `test_connect4.py` – automated test suite for the game logic
* `README.md` – instructions for running the program

---

## Requirements

* Python 3 installed on your computer

---

## How to Run the Game

Open a terminal and navigate to the folder containing the files.

Run the game with:

```
python3 loops_tulane.py
```

The board will appear in the terminal.

Example:

```
 | | | | | | 
 | | | | | | 
 | | | | | | 
 | | | | | | 
 | | | | | | 
 | | | | | | 
-------------
0 1 2 3 4 5 6
```

Players take turns entering a column number **from 0 to 6**.

Example:

```
Player 1 turn
Choose column (0-6): 3
```

The piece will drop into the chosen column.

The game continues until:

* One player connects **four pieces in a row**, or
* The board becomes full (draw).

---

## How to Run the Tests

The project includes a **unit test suite** to verify the game logic.

Run the tests with:

```
python3 -m unittest test_connect4.py
```

If all tests pass, you will see output similar to:

```
......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

---

## Features Implemented

* Board creation
* Turn-based gameplay
* Piece dropping mechanics
* Win detection

  * Horizontal
  * Vertical
  * Diagonal
* Draw detection
* Input validation
* Automated unit testing

---
