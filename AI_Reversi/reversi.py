#Reversi

n = 8 # board size 8,6,4,2(needs to be even)
white = "☺" # white tile ascii
black = "☻" # black tile ascii
bg = "•" # bg tile ascii

w = -1 # white tile ID
b = 1 # black tile ID

def playerASCII(): # defining tile ID
    return white if turn == w else black

def countChess(board, turn): # count how many pieces are on the board
    return sum(board[i].count(turn) for i in range(n))

def printBoard(board): # print the board
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
    print(black + ":" + strLoop(countChess(b)), end = "  ")
    print(white + ":" + str(countChess(w)), end = "")
    print()

def generateBoard(): # prepare board
    board = [[0 for _ in range(n)] for _ in range(n)] # the board
    board[n // 2 - 1][n // 2 - 1] = w
    board[n // 2][n // 2] = w
    board[n // 2][n // 2 - 1] = b
    board[n // 2 - 1][n // 2] = b
    return board

def outOfBound(x, y): # if is out of board/bounds
    return x < 0 or x >= n or y < 0 or y >= n

def neighbourIsOpposite(board, x, y, dx, dy, turn): 
    if outOfBound(x + dx, y + dy):
        return False
    return board[x + dx][y + dy] == opposite(turn)

def checkSandwich(board, x, y, dx, dy, turn):
    if dx == 0 and dy == 0:
        return False
    if outOfBound(x + dx, y + dy): # out of bound
        return False
    if board[x + dx][y + dy] == turn: # sandwiched
        return True
    elif board[x + dx][y + dy] == opposite(turn):
        return checkSandwich(board, x + dx, y + dy, dx, dy, turn)
    else: # space is unoccupied
        return False

def opposite(turn): # change turn
    return w if turn == b else b

def isLegal(board, x, y, turn):
    if outOfBound(x, y): # out of bound
        return False
    if board[x][y] != 0: # space is occupied
        return False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if neighbourIsOpposite(board, x, y, i, j, turn) and \
               checkSandwich(board, x, y, i, j, turn):
                return True        
    return False

def replaceNeighbours(board, x, y, dx, dy, turn):
    if checkSandwich(board, x, y, dx, dy, turn):
        board[x + dx][y + dy] = turn
        replaceNeighbours(board, x + dx, y + dy, dx, dy, turn)

def generateValidMovesList(board, turn):
    return [(i,j) for i in range(n) for j in range(n) \
                      if isLegal(board, i, j, turn)]

def makeMove(board, x, y, turn):
    board[x][y] = turn
    for i in range(-1, 2):
        for j in range(-1, 2):
            if neighbourIsOpposite(board, x, y, i, j, turn):
                replaceNeighbours(board, x, y, i, j, turn)
    return board


### printing who wins
##print()
##print("Game Over!")
##printBoard(board)
##print(black + " Wins!" if countChess(b) > countChess(w) else \
##      (white + " Wins!" if countChess(b) < countChess(w) else \
##       "It's a tie!"))
