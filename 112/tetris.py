# Place your creative task here!

# Be clever, be creative, have fun!

from cmu_graphics import *
import random
def onAppStart(app):
    newGame(app)
    
##############################################################################################################

def newGame(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 95
    app.boardTop = 50
    app.boardWidth = 210
    app.boardHeight = 280
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadTetrisPieces(app)
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))
    loadNextPiece(app)
    app.score = 0
    app.stepsPerSecond = 3
    app.pause = True
    app.gameOver = False
    app.startGame = True


##############################################################################################################
def onStep(app):
    if not(app.pause) and not(app.gameOver):
        takeStep(app)

##############################################################################################################
#when press s, piece moves downward, if hits bottom calls placePieceOnBoard
def takeStep(app):
    if movePiece(app, +1, 0):
        pass
    else:
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)

##############################################################################################################
#loops through 2d board, pops board that are full, add new rows to top to keep dimensions
def removeFullRows(app):
    cols = len(app.board[0])
    rowsRemoved = 0
    row = 0
    while row < len(app.board):
        if app.board[row].count(None) == 0:
            app.board.pop(row)
            rowsRemoved += 1
        else:
            row += 1
    for i in range(rowsRemoved):
        app.board = [[None]*cols] + app.board
    app.score += rowsRemoved

##############################################################################################################
#when piece steps to bottom, piece locks in place and fills colors in board
def placePieceOnBoard(app):
    rows, cols = len(app.piece), len(app.piece[0])
    for row in range(rows):
        for col in range(cols):
            cell = app.piece[row][col]
            if cell:
                app.board[row+app.pieceTopRow][col+app.pieceLeftCol] = app.pieceColor
                    

##############################################################################################################
#creates new piece, shifts index to next piece
def loadNextPiece(app):
    loadPiece(app,app.nextPieceIndex)
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))

##############################################################################################################

def rotate2dListClockwise(L):
    #assigning new rows and cols in relation to old dimensions
    oldRows, oldCols = len(L), len(L[0])
    result = []
    #create 2d list of none with new dimensions
    for col in range(oldCols):
        blankRow = []
        for row in range(oldRows):
            blankRow.append(None)
        result.append(blankRow)
    #old starts from 0th col but starts at last row, iterates backwards
    for col in range(oldCols):
        for row in range(oldRows):
            oldCell = L[oldRows - (row+1)][col]
            result[col][row] = oldCell
    return result

##############################################################################################################

def rotatePieceClockwise(app):
    #stores old piece loc and orientation
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    #reorients piece
    app.piece = rotate2dListClockwise(oldPiece)
    #calculates new center row and col
    centerRow = oldTopRow + len(oldPiece)//2
    centerCol = oldLeftCol + len(oldPiece[0])//2
    newCols = len(oldPiece)
    newRows = len(oldPiece[0])
    #sets proper centers
    app.pieceTopRow = centerRow - newRows//2
    app.pieceLeftCol = centerCol - newCols//2
    #if legal, True
    if pieceIsLegal(app):
        return True
    else:
        #if not reset
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol  = oldLeftCol

##############################################################################################################

def pieceIsLegal(app):
    #iterates through list, if cells are true, makes sure it falls on board
    rows, cols = len(app.piece), len(app.piece[0])
    for row in range(rows):
        for col in range(cols):
            cell = app.piece[row][col]
            if cell:
                #check to see if piece is on board
                if ((app.pieceTopRow + row < 0) or 
                    (row + app.pieceTopRow >= app.rows)
                    or (app.pieceLeftCol + col < 0) or
                    (app.pieceLeftCol + col >= app.cols)):
                    return False
                #if piece would run into already set piece
                elif (app.board[app.pieceTopRow+row][app.pieceLeftCol+col]
                    != None):
                    return False
    return True

##############################################################################################################

def drawPiece(app):
    #iterate through piece, if true fill in correct spot on board
    rows, cols = len(app.piece), len(app.piece[0])
    for row in range(rows):
        for col in range(cols):
            cell = app.piece[row][col]
            if cell:
                drawCell(app, row + app.pieceTopRow, col + app.pieceLeftCol,
                        app.pieceColor)
                
##############################################################################################################

def loadPiece(app, pieceIndex):
    #get piece location, shape, and color
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    app.pieceTopRow = 0
    if pieceIndex != 0 and pieceIndex != 3:
        app.pieceLeftCol = app.cols//2 - len(app.piece[0])//2 - 1
    else:
        app.pieceLeftCol = app.cols//2 - len(app.piece[0])//2
    if not(pieceIsLegal(app)):
        app.gameOver = True

##############################################################################################################
  
def movePiece(app,drow,dcol):
    #change location based on direction
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    #test if move is legal
    if pieceIsLegal(app):
        return True
    else:
        #if not undo
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False

##############################################################################################################
 
def hardDropPiece(app):
    #moves until would be off board
    while movePiece(app, +1, 0):
        pass

##############################################################################################################

def onKeyPress(app, key):
    if "0" <= key <= "6":
        loadPiece(app,int(key))
    elif key == "left":
        movePiece(app,0,-1)
    elif key == "right":
        movePiece(app,0,1)
    elif key == "down":
        movePiece(app,1,0)
    elif key == "space":
        hardDropPiece(app)
    elif key == "up":
        rotatePieceClockwise(app)
    elif key == "s":
        takeStep(app)
    elif key == "p":
        app.pause = not(app.pause)
        app.startGame = False
    elif key == "r":
        newGame(app)

##############################################################################################################   

def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]

##############################################################################################################

def redrawAll(app):
    drawLabel(f'Tetris, Score = {app.score}', app.width/2, 30, size=30, bold = True)
    drawBoard(app)
    if app.piece != None:
        drawPiece(app)
    drawBoardBorder(app)
    if app.startGame:
        drawLabel('Press p to start!', app.width/2, app.height - 45, size=30, bold = True)
    if app.gameOver:
        drawGameOver(app)
    if not(app.pause) and not(app.gameOver):
        drawLabel('Press p to pause!', app.width/2, app.height - 45, size=20, bold = True)
    if app.pause and not(app.startGame) and not(app.gameOver):
        drawLabel('Press p to unpause!', app.width/2, app.height - 45, size=20, bold = True)
##############################################################################################################

def drawGameOver(app):
    drawRect(0,0,app.width,app.height,fill = "black", opacity = 50)
    drawLabel("Game Over",app.width/2,app.height/2,size = 50, bold = True,
    fill = "red")
    drawLabel("Press r to restart!",app.width/2,app.height - 50,size = 30,
    bold = True, fill = "green")

##############################################################################################################

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

##############################################################################################################

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

##############################################################################################################

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

##############################################################################################################

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

##############################################################################################################

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def main():
    runApp()
main()