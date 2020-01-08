import time  # Used to add a delay for user readability

ROWS = COLS = possibleValues = 9  # The rows and columns of the board
GRID_ROWS = GRID_COLS = 3  # The rows and columns in which there are lines
possibleBoard = []


"""Functions"""

def board_filler():
    """Creates the sudoku board from user input"""
    board = [[] for _ in range(ROWS)]  # Creates the nested list to contain the board
    for x in range(ROWS):
        for y in range(COLS):
            # Takes an input makes sure it is good, and if not ask for another one, if it is add it to the list
            while True:
                number = input(
                    f"Please enter an integer for the square in column {x + 1} and in row {y + 1} (hit enter for no number): ")
                try:
                    number = int(number)  # Makes the input that was a string into a number
                    if number > 9 or number < 1:
                        raise ValueError
                    else:
                        board[x].append(number)  # Add the number to the list
                    break  # Exit the loop and let it move on to the next number
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
    counter = 0  # Makes sure it does not print extra lines
    for row in range(ROWS):
        s = ''  # A variable to contain the row before its printed
        # Adds the items from the list to the variable
        for col in range(COLS):
            s += str(board[row][col]) + ' '
            if not (col + 1) % GRID_COLS:
                s += '| '
        s = s[:-2]  # Removes trailing characters
        print(s)
        # Prints the line of lines
        if not (row + 1) % GRID_ROWS and counter < 2:
            print('-' * len(s))
            counter += 1


def line_solver(board):
    """Remove confirmed values from the possible values in the lines"""
    global possibleBoard
    # Checks to see if there are any duplicate numbers in each row, then removes them from the possible board
    for x in range(ROWS):
        for y in range(COLS):
            if board[x][y] == " ":
                for z in range(COLS):
                    try:
                        possibleBoard[x][y].remove(board[x][
                                                       z])  # Removes values from the possibleBoard that are in the same row as a number on the board
                    # If the number that the code is trying to remove has already been removed, do nothing
                    except (ValueError, AttributeError):
                        pass
    for x in range(ROWS):
        for y in range(COLS):
            if board[x][y] == " ":
                for z in range(ROWS):
                    try:
                        possibleBoard[x][y].remove(board[z][
                                                       y])  # Removes values from the possibleBoard that are in the same row as a number on the board
                    # If the number that the code is trying to remove has already been removed, do nothing
                    except (ValueError, AttributeError):
                        pass
    return board


def square_solver(board):
    """Remove confirmed values from the possible values in the squares"""
    global possibleBoard
    # Sets up a modulator to multiply by to get the 3x3 grid of one square with the first value being the rows and the second being the column
    blockNum = [0, 0]
    for _ in range(9):
        # A loop that checks the 9 numbers in one of the squares
        for x in range(3):
            for y in range(3):
                if not board[(blockNum[0] * 3) + x][(blockNum[0] * 3) + y] == " ":  # Checks if that square a number
                    # Checks all the empty spots in one of the squares for that number, then removes them
                    for z in range(3):
                        for w in range(3):
                            try:
                                # Removes the number from the possible board
                                possibleBoard[(blockNum[0] * 3) + z][(blockNum[1] * 3) + w].remove(
                                    board[(blockNum[0] * 3) + x][(blockNum[1] * 3) + y])
                            # If it can't do anything, run this
                            except (ValueError, AttributeError):
                                pass
        blockNum = block_num(blockNum)
    return board

def board_updater(board):
    """Makes it so if there is any number on the board, that that number is a definite on the possible board"""
    global possibleBoard
    for x in range(ROWS):
        for y in range(COLS):
            if not board[x][y] == " ":
                possibleBoard[x][y] = board[x][y]

def solver(board):
    """Solves a few number of the sudoku board"""
    global possibleBoard
    board_updater(board)
    board = line_solver(board)
    board = square_solver(board)
    # Sets up the counter and a modulator to multiply by to get the 3x3 grid of one square with the first value being the rows and the second being the column
    counter = [0] * 9
    blockNum = [0, 0]
    for _ in range(9):
        for x in range(3):
            for y in range(3):
                # Checks the possible board and counts how many time a possible number appears
                if type(possibleBoard[(blockNum[0] * 3) + x][(blockNum[0] * 3) + y]) == list:
                    for z in range(len(possibleBoard[(blockNum[0] * 3) + x][(blockNum[0] * 3) + y])):
                        counter[possibleBoard[(blockNum[0] * 3) + x][(blockNum[0] * 3) + y][z] - 1] += 1
        for x in range(len(counter)):
            # Checks to see if there was any times only one number appeared
            if counter[x] == 1:
                for y in range(3):
                    for z in range(3):
                        try:
                            # Finds the solo number, and makes that number definite
                            if (x + 1) in possibleBoard[(blockNum[0] * 3) + y][(blockNum[0] * 3) + z]:
                                board[(blockNum[0] * 3) + y][(blockNum[0] * 3) + z] = x + 1
                        except TypeError:
                            pass
        blockNum = block_num(blockNum)
        # Rests the counter
        counter = [0] * 9
    for x in range(ROWS):
        for y in range(COLS):
            # If there is only one number in the possibleBoard list, set that as a definite value on the possibleBoard list and add it to the board list
            if type(possibleBoard[x][y]) == list and len(possibleBoard[x][y]) == 1:
                board[x][y] = possibleBoard[x][y][0]
    return board


def filler():
    """Fills the possible board"""
    listOfLists = [[], [], [], [], [], [], [], [], []]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # All numbers are possible on an empty board so it fills it with all numbers
    # Adds 9 empty lists to the row list to represent the 9 squares
    for x in range(ROWS):
        for _ in range(ROWS):
            listOfLists[x].append([])
    # Puts the list with the numbers 1-9 in each square
    for x in range(ROWS):
        for y in range(COLS):
            listOfLists[x][y] = numbers.copy()
    return listOfLists


def solve_check():
    """Checks if board is solved"""
    for x in range(ROWS):
        for y in range(COLS):
            if type(possibleBoard[x][y]) == list:
                return False
    return True


"""Repeated code segments"""

def block_num(blockNum):
    """Increments the square"""
    blockNum[0] += 1
    if blockNum[0] > 2:
        blockNum[1] += 1
        blockNum[0] = 0
    return blockNum


possibleBoard = filler()
board = board_filler()
prevBoard = 0  # A variable to store the board state before it gets changed
# Solves some numbers, prints the new board then waits to allow user to see changes
while True:
    if solve_check():
        break
    board_printer(board)
    time.sleep(1)
    prevBoard = board
    board = solver(board)
    print("")
# Loops so that if entered from the command line, it does not close
while True:
    pass
