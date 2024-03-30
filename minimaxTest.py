import TicTacToe as ttt
import numpy as np
from matplotlib import pyplot as plt

#This script simulates games between a player making random moves, and the minimax AI.
#Keep in mind that >50 simulations will take quite a long time to simulate.
#50 simulations takes approximately 24 seconds.

def getLegalMoves(board: np.ndarray) -> list[tuple]:
    """Takes in the board and returns a list of legal moves in the form of tuples (row, col)"""
    legalMoves = []
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if ttt.legalMove(board, i, j):
                legalMoves.append((i, j))
    return legalMoves


def randomMove(board: np.ndarray, player: int) -> None:
    """Make a random legal move"""
    legalMoves = getLegalMoves(board)
    randomMove = np.random.randint(0, len(legalMoves), dtype = int)
    row, col = legalMoves[randomMove]
    board[row, col] = player

def simGames(n: int = 50) -> None:
    """Simulates n games between the player playing random moves and the Minimax AI.
    Half of the games are played with the AI as X and half as O. Plots the results of the games."""
    playerDict = {}

    #Keep track of results
    AIWinsX = 0
    AIWinsO = 0
    randomWinsX = 0
    randomWinsO = 0
    drawsAIX = 0
    drawsAIO = 0

    for i in range(n):
        AI = 1 if i % 2 == 0 else 2
        randomPlayer = 2 if i % 2 == 0 else 1
        turn = 1
        playerDict[AI] = 'Minimax AI'
        playerDict[randomPlayer] = 'Random-player'

        #Simulate game
        board = np.zeros(shape = (3, 3), dtype = int)
        while True:
            player = 2 if turn % 2 == 0 else 1
            ttt.clearScreen()
            ttt.printBoard(board)
            
            if player == randomPlayer:
                randomMove(board, randomPlayer)
            else:
                ttt.computerMove(board, turn, AI)
            if ttt.checkWin(board):
                ttt.clearScreen()
                ttt.printBoard(board)
                print(f"3 in a row! {playerDict[ttt.checkWin(board)]} won!")
                if ttt.checkWin(board) == AI:
                    if AI == 1:
                        AIWinsX += 1
                    else:
                        AIWinsO += 1
                else:
                    if AI == 1:
                        randomWinsO += 1
                    else:
                        randomWinsX += 1
                break
            if ttt.checkDraw(board):
                ttt.clearScreen()
                ttt.printBoard(board)
                print("Draw.")
                if AI == 1:
                    drawsAIX += 1
                else:
                    drawsAIO += 1
                break
            turn += 1
        
    totalAIWins = AIWinsX + AIWinsO
    totalRandomWins = randomWinsX + randomWinsO
    totalDraws = drawsAIX + drawsAIO

    #Display the results
    fig, ax = plt.subplots(facecolor = 'teal', layout = 'constrained')
    ax.set_title(f'Simulation of {n} Tic-Tac-Toe games\nbetween random player and minimax AI',
                    fontsize = 12,
                    fontweight = 'bold')

    results = {'AI-wins' : (AIWinsX, AIWinsO, totalAIWins),
               'Random-player-wins' : (randomWinsO, randomWinsX, totalRandomWins),
               'Draws' : (drawsAIX, drawsAIO, totalDraws)}

    labels = ['AI first', 'AI second', 'Total']
    x = np.arange(len(labels)) #Label locations
    width = 0.25 #bar width
    multiplier = 0

    for player, wins in results.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, wins, width, label = player)
        ax.bar_label(rects, padding = 3)
        multiplier += 1

    ax.set_ylabel('Games')
    ax.set_xticks(x + width, labels)
    ax.legend(fontsize = 9, loc = 'upper left', ncols = 3, framealpha = 0) 
    #fig.savefig(f'Sim_of_{n}_games.png')
    plt.show()

if __name__ == "__main__":
    simGames(50)