#Reversi
#By Patrick

import random
import AI

generation = 861 ## Gerneation to play against
n = 8 # board size 8,6,4,2(needs to be even)
white = "☺" # white tile ascii
black = "☻" # black tile ascii
bg = "•" # bg tile ascii

w = -1 # white tile ID
b = 1 # black tile ID

board = [[0 for _ in range(n)] for _ in range(n)] # the board


def playerASCII(): # defining tile ID
    return white if turn == w else black

def countChess(turn): # count how many pieces are on the board
    return sum(board[i].count(turn) for i in range(n))

def printBoard(): # print the board
    print()
    print("  ", end = "")
    for i in range(n):
        print(i, end = " ")
    print()
    for i in range(n): # making a 2-D array
        print(i, end = " ")
        for j in range(n):
            print(white if board[j][i] == w else \
                  (black if board[j][i] == b else bg), end = " ")
        print()
    print(black + ":" + str(countChess(b)), end = "  ")
    print(white + ":" + str(countChess(w)), end = "")
    print()

def initBoard(): # prepare board
    board[n // 2 - 1][n // 2 - 1] = w
    board[n // 2][n // 2] = w
    board[n // 2][n // 2 - 1] = b
    board[n // 2 - 1][n // 2] = b
    
	## custom board for testing
	#global board
    #board = [[b,b,b,b,b,b,b,b],
    #         [b,b,b,b,b,b,b,b],
    #         [b,b,b,w,b,b,b,b],
    #         [b,w,b,b,b,w,b,b],
    #         [b,b,b,b,w,b,b,b],
    #         [b,b,b,0,w,b,b,b],
    #         [b,b,0,0,w,w,0,0],
    #         [b,0,0,0,w,w,w,0]]

def outOfBound(x, y): # if is out of board/bounds
    return x < 0 or x >= n or y < 0 or y >= n

def neighbourIsOpposite(x, y, dx, dy): 
    if outOfBound(x + dx, y + dy):
        return False
    return board[x + dx][y + dy] == opposite(turn)

def checkSandwich(x, y, dx, dy, turn):
    if dx == 0 and dy == 0:
        return False
    if outOfBound(x + dx, y + dy): # out of bound
        return False
    if board[x + dx][y + dy] == turn: # sandwiched
        return True
    elif board[x + dx][y + dy] == opposite(turn):
        return checkSandwich(x + dx, y + dy, dx, dy, turn)
    else: # space is unoccupied
        return False

def opposite(turn): # change turn
    return w if turn == b else b


def isLegal(x, y, turn):
    if outOfBound(x, y): # out of bound
        return False
    if board[x][y] != 0: # space is occupied
        return False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if neighbourIsOpposite(x, y, i, j) and \
               checkSandwich(x, y, i, j, turn):
                return True        
    return False

def replaceNeighbours(x, y, dx, dy, turn):
    if checkSandwich(x, y, dx, dy, turn):
        board[x + dx][y + dy] = turn
        replaceNeighbours(x + dx, y + dy, dx, dy, turn)

def generateValidMovesList():
    return [(i,j) for i in range(n) for j in range(n) \
                      if isLegal(i, j, turn)]

initBoard()

turn = b # turn indicator b or w(Black Or White), black goes first
whiteCanPlay = True # if white is not stuck
blackCanPlay = True # if black is not stuck

# legal check
playerTile = input("Choose your chess color.  Type 'b' for black and white otherwise.  Black goes first: ")
playerTile = b if playerTile == 'b' else w

bestNetwork = AI.loadNetworks(AI.structure, generation)[0]


while whiteCanPlay or blackCanPlay:

    validMoves = generateValidMovesList()

    if len(validMoves) == 0:
        print()
        if turn == w:
            whiteCanPlay = False
        if turn == b:
            blackCanPlay = False
    else :
        if turn == w:
            whiteCanPlay = True
        if turn == b:
            blackCanPlay = True
            
        printBoard()
        
        print("Valid Moves:", validMoves)

        if turn == playerTile:
            # player's turn, legal check
            while True:
                try:
                    x, y = input(playerASCII() + \
                                 ", it's your move (x y): ").split()
                    x, y = int(x), int(y)
                    if isLegal(x, y, turn):
                        break
                    else:
                        print("Invalid Move.  ", end = "")
                except:
                    print("Invalid Format.  ", end = "")
        else:
            # computer's turn
            #x, y = random.choice(validMoves)
            x, y = AI.chooseMove(board, AI.structure, bestNetwork, turn)
            print(playerASCII() + " Computer's move:", x, y)
           
        # replacing tiles
        board[x][y] = turn
        for i in range(-1, 2):
            for j in range(-1, 2):
                if neighbourIsOpposite(x, y, i, j):
                    replaceNeighbours(x, y, i, j, turn)

    # switching players
    turn = opposite(turn)


# printing who wins
print()
print("Game Over!")
printBoard()
print(black + " Wins!" if countChess(b) > countChess(w) else \
      (white + " Wins!" if countChess(b) < countChess(w) else \
       "It's a tie!"))
