import numpy as np
import os
import time

#Tic-Tac-Toe game

def legalMove(board: np.ndarray, row: int, col: int) -> bool:
    """Checks if the square is empty"""
    return True if board[row, col] == 0 else False

def makePretty(board: np.ndarray) -> np.ndarray: 
    """
    Converts numbers to correct strings for printing.
    """
    boardDict = {1 : 'X', 2 : 'O', 0 : ' '}
    prettyBoard = np.zeros_like(board, dtype=str)
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            prettyBoard[i, j] = boardDict[col]
    return prettyBoard

def printBoard(board: np.ndarray) -> None:
    """Prints the board"""

    prettyBoard = makePretty(board)
    print('   ' + '  ' + '   '.join(['1', '2', '3']))
    for i, row in enumerate(prettyBoard):
        print('   ' + '-' * 13)
        print(f' {i + 1} | ' + ' | '.join(row) + ' |')
    print('   ' + '-' * 13)

    
def checkWin(board: np.ndarray) -> int:
    """Returns 1 if player 1 has won. Returns 2 if player 2 has won. Else 0"""
    
    for idx, row in enumerate(board):
        if len(set(row)) == 1 and 0 not in row: #Checks all the rows
            return row[0]
        if len(set(board[:, idx])) == 1 and 0 not in board[:, idx]: #Checks all the columns
            return board[:, idx][0]
    #create diagonals
    diagonal1 = [board[0, 0], board[1, 1], board[2, 2]]
    diagonal2 = [board[2, 0], board[1, 1], board[0, 2]]
    #check diagonals
    if len(set(diagonal1)) == 1 and 0 not in diagonal1:
        return diagonal1[0]
    if len(set(diagonal2)) == 1 and 0 not in diagonal2:
        return diagonal2[0]
    
    return 0

def checkDraw(board: np.ndarray) -> bool:
    """Returns True if the game is a draw"""
    return True if 0 not in np.concatenate(board) and not checkWin(board) else False

def takeMove(board: np.ndarray, player: int, numToPlayer: dict) -> tuple[int]:
    """Asks the player for an input and returns the move as a tuple if legal"""

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        printBoard(board)
        print(f"It is {numToPlayer[player]}'s turn.")
        row = input('Choose row: ')
        col = input("Choose column: ")

        try:
            row = int(row) - 1
            col = int(col) - 1
            if legalMove(board, row, col):
                break
            else:
                print('Illegal move. Make sure the input square is empty.')

        except ValueError:
            print('Invalid input. Only input integers between 1 and 3.')
        except IndexError:
            print('Invalid input. The row and column must be between 1 and 3.')
        time.sleep(2)
    return row, col

def move(board: np.ndarray, player: int, numToPlayer: dict) -> None:
    """Places either X or O in the given square"""
    row, col = takeMove(board, player, numToPlayer)
    board[row, col] = player #ndarrays are passed by reference, so no return is needed


def takePlayerNames() -> tuple[str]:
    """Asks for the players names and returns them in a tuple of strings"""
    print("Who's playing? ")
    player1 = input('Player 1: ')
    player2 = input('PLayer 2: ')
    return player1, player2


def minimax(board: np.ndarray, depth: int, maximizer: int, isMaximizing: bool) -> int:
    """Minimax algorithm to determine the best moves"""

    minimizer = 2 if maximizer == 1 else 1

    #END STATES
    if checkWin(board) == maximizer:
        return 1
    if checkWin(board) == minimizer:
        return -1
    if checkDraw(board):
        return 0
    
    #MINIMAX
    bestScore = -float('inf') if isMaximizing else float('inf')

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if legalMove(board, i, j):
                board[i, j] = maximizer if isMaximizing else minimizer
                maximizeNext = False if isMaximizing else True
                score = minimax(board, depth + 1, maximizer, maximizeNext)
                board[i, j] = 0
                bestScore = max(bestScore, score) if isMaximizing else min(bestScore, score)
    return bestScore




def computerMove(board: np.ndarray, turn: int, player: int) -> None:
    """The computer makes the best possible move"""
    bestScore = -float('inf')
    bestMove = (0, 0) #default

    if turn != 1: #(0, 0) is the best first move so we save time by skipping the minimax function for turn 1
        for i, row in enumerate(board):
            for j, col in enumerate(row):
                if legalMove(board, i, j):
                    board[i, j] = player
                    score = minimax(board, turn, player, False)
                    board[i, j] = 0 #reset

                    if score > bestScore:
                        bestScore = score
                        bestMove = (i, j)
    row, col = bestMove

    board[row, col] = player


def clearScreen():
    """Clears the terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def twoPlayer():
    """Runs the Tic Tac Toe game for two players"""
    board = np.zeros(shape = (3, 3), dtype= int)

    #Welcome message
    print('You have chosen two-player mode.')
    time.sleep(1)

    #take player names and asign them
    playerDict = {}
    player1, player2 = takePlayerNames()
    playerDict[1] = player1
    playerDict[2] = player2

    #Keep track of turn
    turn = 1

    while True:
        player = 2 if turn % 2 == 0 else 1
        move(board, player, playerDict)
        if checkWin(board):
            clearScreen()
            printBoard(board)
            time.sleep(1)
            print(f"3 in a row! {playerDict[checkWin(board)]} won!")
            break
        if checkDraw(board):
            clearScreen()
            time.sleep(1)
            printBoard(board)
            print("Draw.")
            break
        turn += 1
    print('Thanks for playing!')

def singlePlayer():
    """Plays the game vs the computer"""

    board = np.zeros(shape = (3, 3), dtype= int)

    #Welcome message
    print('You have chosen one-player mode.')
    time.sleep(1)

    playerDict = {}
    print("Who's playing? ")
    player = input('Name: ')

    start = ''
    while start != 'y' and start != 'n':
        clearScreen()
        start = input('Do you wanna start? [y/n] ').lower()

        if start == 'y':
            playerDict[1] = player
            playerDict[2] = 'AI'
            human = 1
            ai = 2
        elif start == 'n':
            playerDict[1] = 'AI'
            playerDict[2] = player
            human = 2
            ai = 1
        else:
            print('Invalid input. Type either "y" or "n".')
            time.sleep(2)

        #Keep track of turn
    turn = 1

    while True:
        player = 2 if turn % 2 == 0 else 1
        if player == human:
            move(board, player, playerDict)
        else:
                #Message to player
            clearScreen()
            printBoard(board)
            print('The AI is making its move...')
            time.sleep(2)
            computerMove(board, turn, ai)
        if checkWin(board):
            clearScreen()
            printBoard(board)
            time.sleep(1)
            print(f"3 in a row! {playerDict[checkWin(board)]} won!")
            break
        if checkDraw(board):
            clearScreen()
            printBoard(board)
            time.sleep(1)
            print("Draw.")
            break
        turn += 1
    print('Thanks for playing!')

def menu() -> None:
    clearScreen()
    gamemode = ''
    print('Welcome to Tic Tac Toe!') #welcome message
    time.sleep(1)
    while gamemode != '1' and gamemode != '2':
        print('''Choose gamemode:
        1) Single-player (vs. computer)
        2) Two-player (locally)
        q) Quit''')
        gamemode = input("Enter choice: ")
        if gamemode == '1':
            clearScreen()
            singlePlayer()
        elif gamemode == '2':
            clearScreen()
            twoPlayer()
        elif gamemode == 'q':
            print("Bye!")
            return #quits
        else:
            print('Inavlid input. Type either "1", "2" or "q".')
            time.sleep(2)
            clearScreen()


if __name__ == "__main__":
    menu()