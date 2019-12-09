import math  # To be used later
import time # Used to add a delay for user readibility

ROWS = COLS = possibleValues = 9 # The rows and columns of the board
GRID_ROWS = GRID_COLS = 3 # The rows and columns in which there are lines
possibleBoard = []

def board_filler():
    """Creates the sudoku board from user input"""

    board = [[] for _ in range(ROWS)] # Creates the nested list to contain the board

    for x in range(ROWS):
        for y in range(COLS):
            # Takes an input makes sure it is good, and if not ask for another one, if it is add it to the list
            while True:
                number = input(f"Please enter an integer for the square in column {x + 1} and in row {y + 1} (hit enter for no number): ")

                try:
                    number = int(number) # Makes the input that was a string into a number

                    if number > 9 or number < 1:
                        raise ValueError
                    else:
                        board[x].append(number) # Add the number to the list

                    break # Exit the loop and let it move on to the next number
                # If its not a number, or a number more 9 or less than 1 runs this
                except (TypeError, ValueError):
                    # If its empty, adds just a space to the list
                    if not number:
                        board[x].append(" ")
                        break
                    else:
                        print("Please enter an integer between 1 and 9, or just hit enter")

    return board

def board_printer(board):
    """Prints the sudoku board"""
    counter = 0 # Makes sure it does not print extra lines
    for row in range(ROWS):
        s = '' # A vaible to contain the row before its printed
        # Adds the items from the list to the varible
        for col in range(COLS):
            s += str(board[row][col]) + ' '

            if not (col + 1) % GRID_COLS:
                s += '| '

        s = s[:-2] # Removes trailing charecters

        print(s)
        # Prints the line of lines
        if not (row + 1) % GRID_ROWS and counter < 2:
            print('-' * len(s))
            counter += 1

def solver(board):
    """Solves a few number of the sudoku board"""
    global possibleBoard
    # If a number is the board, replace the list in the possible board with that number
    for x in range(ROWS):
        for y in range(COLS):
            if not board[x][y] == " ":
                possibleBoard[x][y] = board[x][y]
    # Checks to see if there are any duplicate numbers in each row, then removes them from the possible board
    for x in range(ROWS):
        for y in range(COLS):
            if board[x][y] == " ":
                for z in range(COLS):
                    try:
                        possibleBoard[x][y].remove(board[x][z])
                    except ValueError:
                        pass
    for x in range(ROWS):
        for y in range(COLS):
            if type(possibleBoard[x][y]) == list and len(possibleBoard[x][y]) == 1:
                board[x][y] = possibleBoard[x][y][0]
                possibleBoard[x][y] = possibleBoard[x][y][0]
    return board

def filler():
    """Fills the possible board"""
    listOfLists = [[], [], [], [], [], [], [], [], []]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9] # All numbers are possible on an empty board so it fills it with all numbers
    emptyList = [] # Used to fill the list with 9 squares per row
    # Adds 9 empty lists to the row list to repersent the 9 squares
    for x in range(ROWS):
        for _ in range(ROWS):
            listOfLists[x].append(emptyList)
    # Puts the list with the numbers 1-9 in each square
    for x in range(ROWS):
        for y in range(COLS):
            listOfLists[x][y] = numbers
    return listOfLists

possibleBoard = filler()
board = board_filler()
# Solves some numbers, prints the new board then waits to allow user to see changes
while True:
    print(possibleBoard)
    board = solver(board)
    board_printer(board)
    time.sleep(1)
