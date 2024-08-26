from cmu_graphics import *
import random
import math

def almostEqual(num1,num2):
    if abs(num1-num2) < .0005:
        return True
    else:
        return False


#Visuals
################################################################################
def onAppStart(app):
    newGame(app)

#resets game, grid,vertices,edges,passengers
def newGame(app):
    app.width = 1400
    app.height = 1000
    app.rows = 3
    app.cols = 4

    app.boardLeft = app.width/60
    app.boardTop = app.height/16
    app.boardWidth = app.width - app.width/30
    app.boardHeight = app.height - app.height/6
    app.cellWidth = app.boardWidth/app.cols
    app.cellHeight = app.boardHeight/app.rows
    app.cellBorderWidth = 1
    app.board = [([None] * app.cols) for row in range(app.rows)]

    app.vSpawnRate = 30
    app.pSpawnRate = 5
    app.levelRate = 150
    app.level = 0
    app.score = 0
    app.stepsPerSecond = 1
    app.pause = True
    app.gameOver = False
    app.startGame = True
    app.newLevel = False
    app.steps = 0

    app.currVertex = None
    app.currMouse = None
    app.currEdgeColor = None
    app.currVPair = None

    vClass.store = []
    vClass.adjLists = {}
    vClass.tCount = 3
    vClass.currPassengers = {}

    eClass.store = []
    eClass.bank = {}
    eClass.tCount = 2
    eClass.edgeCount = {}
    eClass.edgeLists = {}
    for color in eClass.allColors:
        eClass.edgeCount[color] = 0
        eClass.edgeLists[color] = []

    passengers.store = []
    metros.store = []


#Drawing
################################################################################
def redrawAll(app):
    drawRect(0,app.boardTop,app.width,app.boardHeight, fill = "papayaWhip",
             border = "black")
    drawEdgeBank(app)
    drawLabel('Mini Metro', app.boardLeft,
              app.height/40, size=app.height/30, bold = True, align = "left")
    drawLabel(f'Score = {app.score}', app.boardWidth+app.boardLeft,
              app.height/40, size=app.height/30, bold = True, align = "right")
    drawLines(app)
    if (app.currVertex != None and app.currMouse != None and app.currEdgeColor != None
        and not(isInEdgeBank(app,app.currMouse[0],app.currMouse[1]))):
        x = app.boardLeft+(app.currVertex.col*app.cellWidth)+app.cellWidth/2
        y = app.boardTop+(app.currVertex.row*app.cellHeight)+app.cellHeight/2
        drawLine(x,y,app.currMouse[0],app.currMouse[1])
    drawBoard(app)
    if app.gameOver:
        drawGameOver(app)
    if not(app.pause) and not(app.gameOver):
        drawRect(app.width/2 - app.width/90,app.boardTop/2, app.width/75, app.boardTop/1.5,
                 align = "center")
        drawRect(app.width/2 + app.width/90,app.boardTop/2, app.width/75, app.boardTop/1.5,
                 align = "center")
    if app.pause and not(app.startGame) and not(app.gameOver):
        drawRegularPolygon(app.width/2,app.boardTop/2,app.boardTop/2,3, rotateAngle = 90)
    if not(app.newLevel):
        drawMetros(app)
    if app.newLevel:
        drawNewLevel(app)
    if app.startGame:
        drawRect(0,0,app.width,app.height, fill = "papayaWhip",
             border = "black")
        drawLabel("Welcome to Mini Metro!", app.width/2, app.height/10, size = 50, fill = "blue")
        drawLabel("You are a Civil Engineer responsible for constructing the city's metro lines",app.width/2,2*app.height/10, size = 35)
        drawLabel("Stations will randomly appear with passengers spawning at them",app.width/2, 3*app.height/10, size = 35)
        drawLabel("You must ensure that passengers can get to their destination as indicated by their shape!",app.width/2, 4*app.height/10, size = 35)
        drawLabel("Using the mouse, you can select a line from the line bank in the bottom left corner",app.width/2, 5*app.height/10, size = 35)
        drawLabel("Once selected, you can connect stations by clicking and dragging the mouse",app.width/2, 6*app.height/10, size = 35)
        drawLabel("To delete a connection, select the color then the edge and press 'd'",app.width/2, 7*app.height/10, size = 35)
        drawLabel("Note: you can only delete the edges on the end of the line",app.width/2, 7.75*app.height/10, size = 25)
        drawLabel("And some line formations are restricted so be wary!",app.width/2, 8.25*app.height/10, size = 25)
        drawLabel("Good Luck and Have Fun!",app.width/2, 9*app.height/10, size = 35, fill = "blue")
    

#draws metros and curr passengers aboard
def drawMetros(app):
    for metro in metros.store:
        if metro.currEdge != None and metro.currX != None and metro.currY != None:
            drawRect(metro.currX,metro.currY,app.cellWidth/5,app.cellHeight/5,
                     align = "center", fill = metro.color, border = "black",
                     borderWidth = 3)
            passWidth = app.cellWidth/21
            for i in range(len(metro.currPassengers)):
                person = metro.currPassengers[i]
                if i == 0:
                    drawRegularPolygon(metro.currX-app.cellWidth/15,
                    metro.currY-app.cellHeight/15,passWidth, person.type, fill= "white",
                    border = "black",borderWidth = 1)
                elif i == 1:
                    drawRegularPolygon(metro.currX+app.cellWidth/15,
                    metro.currY-app.cellHeight/15,passWidth, person.type, fill= "white",
                    border = "black",borderWidth = 1)
                elif i == 2:
                    drawRegularPolygon(metro.currX-app.cellWidth/15,
                    metro.currY+app.cellHeight/15,passWidth, person.type, fill= "white",
                    border = "black",borderWidth = 1)
                elif i == 3:
                    drawRegularPolygon(metro.currX+app.cellWidth/15,
                    metro.currY+app.cellHeight/15,passWidth, person.type, fill= "white",
                    border = "black",borderWidth = 1)
    
#draws grid
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

#draws each cell, if vertex in cell, draws vertex, if timer draw timer
#draws passengers
def drawCell(app, row, col, vertex):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight,
             fill= None)
    if vertex != None:
        if app.currVertex == vertex:
            drawRegularPolygon((cellLeft+app.cellWidth/2),(cellTop+app.cellHeight/2),
                    app.cellWidth/4,vertex.type,fill = "gainsboro", border = "black",
                    borderWidth = 3)
        else:
            drawRegularPolygon((cellLeft+app.cellWidth/2),(cellTop+app.cellHeight/2),
                    app.cellWidth/4, vertex.type, fill= "white", border = "black",
                    borderWidth = 3)
        if vertex.timer:
            drawRect(cellLeft,cellTop,app.cellWidth*3/4,
                    app.cellHeight/7, fill = None, border = "black",
                    borderWidth = 3)
            drawRect(cellLeft,cellTop,vertex.timeLeft*3/4*app.cellWidth/30,
                    app.cellHeight/7, fill = "black")
        drawPassengers(app,vertex,cellLeft,cellTop)

#if passengers at station draws them below
def drawPassengers(app,vertex,cellLeft,cellTop):
    people = vClass.currPassengers[vertex]
    passWidth = app.cellWidth/7
    yCord = cellTop + app.cellHeight*8/10
    for i in range(len(people)):
        person = people[i]
        drawRegularPolygon(cellLeft+(app.cellWidth/16)+(app.cellWidth/8)*(i+1),yCord,
                passWidth/3, person.type, fill= "white", border = "black",
                borderWidth = 3)

#input two vertices, draws line between them
def drawConnection(app,v1,v2):
    x1 = app.boardLeft+(v1.col*app.cellWidth)+app.cellWidth/2
    y1 = app.boardTop+(v1.row*app.cellHeight)+app.cellHeight/2
    x2 = app.boardLeft+(v2.col*app.cellWidth)+app.cellWidth/2
    y2 = app.boardTop+(v2.row*app.cellHeight)+app.cellHeight/2
    height = distance(x1,x2,y1,y2)
    dx = x1-x2
    dy = y1-y2
    if dx != 0:
        rectAngle = math.degrees(math.atan(dy/dx))
    else:
        rectAngle = 90
    vPair = v1.sort(v2)
    if vPair in eClass.bank:
        for color in eClass.bank[vPair]:
            if vPair == app.currVPair and color == app.currEdgeColor:
                drawRect((x1+x2)/2,(y1+y2)/2,height,app.cellWidth/20, fill = color,
                        rotateAngle= rectAngle, align = "center", opacity = 50,
                        border = "black", borderWidth = 3)
            else:
                drawRect((x1+x2)/2,(y1+y2)/2,height,app.cellWidth/20, fill = color,
                        rotateAngle= rectAngle, align = "center", opacity = 50)
        if len(eClass.bank[vPair]) > 0:
            drawCircle((x1+x2)/2,(y1+y2)/2,app.cellWidth/25,fill = "black",opacity = 75)

#if reached new level, pauses game
def drawNewLevel(app):
    drawRect(0,0,app.width,app.height,fill = "black", opacity = 50)
    drawLabel("Congratulations, You made it to the next level!",
              app.width/2,app.height/2,size = 50, bold = True, fill = "blue")
    drawLabel("When you are ready, press p to continue!",app.width/2,
              app.height - 200,size = 30,bold = True, fill = "green")

#if timer expires, game over ends game
def drawGameOver(app):
    drawRect(0,0,app.width,app.height,fill = "black", opacity = 50)
    drawLabel("Game Over",app.width/2,app.height/2,size = 50, bold = True,
    fill = "red")
    drawLabel("Press r to restart!",app.width/2,app.height - 200,size = 30,
    bold = True, fill = "black")

#takes graph draws all connections in graph
def drawLines(app):
    pastConnections = set()
    for v1 in vClass.adjLists:
        for v2 in vClass.adjLists[v1]:
            vPair = v1.sort(v2)
            if vPair not in pastConnections:
                drawConnection(app,v1,v2)
                pastConnections.add((v1,v2))
                pastConnections.add((v2,v1))

#draws circles corresponding to each edge color
def drawEdgeBank(app):
    x = app.boardLeft + app.width/100
    y = app.height - app.height/23
    for i in range(len(eClass.currColors)):
        color = eClass.currColors[i]
        if color != app.currEdgeColor:
            drawCircle(x+i*app.width/15,y,app.width/100,fill = color)
        else:
            drawCircle(x+i*app.width/15,y,app.width/100,fill = color,
                       border = "black", borderWidth = 3)

#Mechanics
################################################################################

#gets top left corner of cell
def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.cellWidth
    cellTop = app.boardTop + row * app.cellHeight
    return (cellLeft, cellTop)

#pauses game, shifts grid
#updates app, board, metros
#adds more color and vertex options
def newLevel(app):
    app.pause = True
    app.rows += 1
    app.cols += 1
    app.cellWidth = app.boardWidth/app.cols
    app.cellHeight = app.boardHeight/app.rows
    app.level += 1
    vClass.tCount += 1
    eClass.tCount += 1
    eClass.currColors = eClass.allColors[:eClass.tCount]
    updateBoard(app)
    updateMetros(app)
    app.newLevel = True

#adds row and col
def updateBoard(app):
    app.board.append([None] * app.cols)
    for row in app.board:
        row.append(None)

#updates metros
#spawns passengers, vertices, and checks if time for new level
def takeStep(app):
    app.steps += 1
    updateMetros(app)
    checkTimer(app)
    if app.steps % app.levelRate == 0:
        newLevel(app)
    elif app.steps % app.vSpawnRate == 0:
        vertex = vClass(app)
        app.board[vertex.row][vertex.col] = vertex
    elif app.steps == 1:
        v1 = vClass(app,3)
        app.board[v1.row][v1.col] = v1
        v2 = vClass(app,4)
        app.board[v2.row][v2.col] = v2
        v3 = vClass(app,5)
        app.board[v3.row][v3.col] = v3
    elif app.steps % app.pSpawnRate == 0:
        passengers()

def onStep(app):
    if not(app.pause) and not(app.gameOver):
        takeStep(app)

#p pauses game
#d deletes edge if legal, if only one edge delete metro too
def onKeyPress(app, key):
    if key == "s":
        takeStep(app)
    elif key == "p":
        app.pause = not(app.pause)
        app.startGame = False
        app.newLevel = False
    elif key == "r":
        newGame(app)
    elif key == "l":
        newLevel(app)
    elif key == "n":
        passengers()
    elif key == "d" and app.currVPair != None and app.currEdgeColor != None:
        if (isLegalDelete(app.currVPair,app.currEdgeColor)
            and checkMetros(app)):
            eClass.bank[app.currVPair].remove(app.currEdgeColor)
            eClass.edgeCount[app.currEdgeColor] -= 1
            index = listFind(eClass.edgeLists[app.currEdgeColor],app.currVPair)
            v1, v2 = app.currVPair
            otherVPair = (v2,v1)
            if index != None:
                eClass.edgeLists[app.currEdgeColor].pop(index)
            else:
                eClass.edgeLists[app.currEdgeColor].remove(otherVPair)
        elif (isLegalDelete(app.currVPair,app.currEdgeColor)
            and len(eClass.edgeLists[app.currEdgeColor]) == 1):
            eClass.bank[app.currVPair].remove(app.currEdgeColor)
            eClass.edgeCount[app.currEdgeColor] -= 1
            index = listFind(eClass.edgeLists[app.currEdgeColor],app.currVPair)
            v1, v2 = app.currVPair
            otherVPair = (v2,v1)
            if index != None:
                eClass.edgeLists[app.currEdgeColor].pop(index)
            else:
                eClass.edgeLists[app.currEdgeColor].remove(otherVPair)
            for metro in metros.store:
                if metro.color == app.currEdgeColor:
                    metro.currEdge = None

#if metro on selected edge to delete, illegal
def checkMetros(app):
    for metro in metros.store:
        v1, v2 = app.currVPair
        if ((metro.currEdge == app.currVPair or metro.currEdge == (v2,v1))
            and metro.color == app.currEdgeColor):
            return False
    return True

#calculates distance
def distance(x1,x2,y1,y2):
    return ((x1-x2)**2+(y1-y2)**2)**.5

#if mouse click in vertex, returns vertex
def isInStation(app,mouseX,mouseY):
    if (app.boardLeft < mouseX < (app.boardWidth + app.boardLeft)
        and app.boardTop < mouseY < (app.boardHeight + app.boardTop)):
        col = int((mouseX-app.boardLeft)/app.cellWidth)
        row = int((mouseY-app.boardTop)/app.cellHeight)
        if app.board[row][col] != None:
            vertex = app.board[row][col]
            x = app.boardLeft+(col*app.cellWidth)+app.cellWidth/2
            y = app.boardTop+(row*app.cellHeight)+app.cellHeight/2
            if distance(x,mouseX,y,mouseY) < app.cellWidth/4:
                return vertex
    return False

#if mouse click in edge bank, returns color
def isInEdgeBank(app,mouseX,mouseY):
    if (app.height - app.height/23 - app.width/100 <= mouseY
        <= app.height - app.height/23 + app.width/100):
        x = app.boardLeft + app.width/100
        for i in range(len(eClass.currColors)):
            color = eClass.currColors[i]
            xcord = x+i*app.width/15
            if xcord - app.width/100 <= mouseX <= xcord + app.width/100:
                return color
    return False

#if click in edge returns selected edge
def isInEdge(app,mouseX,mouseY):
    res = None
    count = 0
    for (v1,v2) in eClass.bank:
        x1 = app.boardLeft+(v1.col*app.cellWidth)+app.cellWidth/2
        y1 = app.boardTop+(v1.row*app.cellHeight)+app.cellHeight/2
        x2 = app.boardLeft+(v2.col*app.cellWidth)+app.cellWidth/2
        y2 = app.boardTop+(v2.row*app.cellHeight)+app.cellHeight/2
        cx = (x1+x2)/2
        cy = (y1+y2)/2
        if distance(cx,mouseX,cy,mouseY) <= app.cellWidth/25:
            count += 1
            res = (v1,v2)
    if count == 1:
        return res
    else:
        return False

#if in vertex new selected station
#if in edge, new selected edge
#if in edgebank, new selected edge color
#else nothing selected
def onMousePress(app, mouseX, mouseY):
    if not(app.pause):
        resStation = isInStation(app,mouseX,mouseY)
        resEdge = isInEdge(app,mouseX,mouseY)
        resEdgeBank = isInEdgeBank(app,mouseX,mouseY)
        if resStation != False:
            app.currVertex = resStation
        elif resEdge != False:
            app.currVPair = resEdge 
        elif resEdgeBank != False:
            app.currEdgeColor = resEdgeBank
        else:
            app.currVertex = None
            app.currVPair = None

#if start vertex is selected, and mouse is dragged from one circle to another
#adds the two in graph, if not already there and legal edge
def onMouseDrag(app, mouseX, mouseY):
    app.currMouse = (mouseX, mouseY)
    if not(app.pause):
        if app.currVertex != None and app.currEdgeColor != None:
            possNewVert = isInStation(app,mouseX,mouseY)
            if (possNewVert != False and possNewVert != app.currVertex):
                if (app.currVertex not in vClass.adjLists[possNewVert]
                    and isLegalEdge(app.currVertex,possNewVert,app.currEdgeColor)):
                    vClass.adjLists[app.currVertex].add(possNewVert)
                    vClass.adjLists[possNewVert].add(app.currVertex)
                    if eClass.edgeCount[app.currEdgeColor] == 0:
                        eClass(app.currVertex,possNewVert,app.currEdgeColor,app.steps)
                    else:
                        eClass(app.currVertex,possNewVert,app.currEdgeColor)
                    app.currVertex = possNewVert
                else:
                    vPair = app.currVertex.sort(possNewVert)
                    if (vPair in eClass.bank and app.currEdgeColor not in eClass.bank[vPair]
                        and isLegalEdge(app.currVertex,possNewVert,app.currEdgeColor)):
                            if eClass.edgeCount[app.currEdgeColor] == 0:
                                eClass(app.currVertex,possNewVert,app.currEdgeColor,app.steps)
                            else:
                                eClass(app.currVertex,possNewVert,app.currEdgeColor)
                            app.currVertex = possNewVert

#make sure extending path, not creating new one
def isLegalEdge(currVert,newVert,color):
    if eClass.edgeCount[color] == 0:
        return True
    else:
        count1 = 0
        count2 = 0
        for neighbor in vClass.adjLists[currVert]:
            vPair = neighbor.sort(currVert)
            if vPair in eClass.bank and color in eClass.bank[vPair]:
                count1 += 1
        for neighbor in vClass.adjLists[newVert]:
            vPair = neighbor.sort(newVert)
            if vPair in eClass.bank and color in eClass.bank[vPair]:
                count2 += 1
        return count1 == 1 and count2 <= 1

#can only delete edges last in path, unless only edge  
def isLegalDelete(vertexPair,color):
    v1,v2 = vertexPair
    v1NeighborCount = 0
    v2NeighborCount = 0
    for neighbor in vClass.adjLists[v1]:
        vPair = neighbor.sort(v1)
        if vPair in eClass.bank and color in eClass.bank[vPair]:
            v1NeighborCount += 1
    for neighbor in vClass.adjLists[v2]:
        vPair = neighbor.sort(v2)
        if vPair in eClass.bank and color in eClass.bank[vPair]:
            v2NeighborCount += 1
    loopBool = isLoop(color)
    if v1NeighborCount > 1 and v2NeighborCount > 1 and not(loopBool):
        return False
    elif v1NeighborCount > 1 and v2NeighborCount > 1 and loopBool:
        return True
    elif v1NeighborCount == 1 and v2NeighborCount == 1:
        return True
    elif (v1NeighborCount > 1 and v2NeighborCount == 1 or
          v1NeighborCount == 1 and v2NeighborCount > 1):
        return True

#iterates through adjacency lists if can return back to oringinal vertex
#through different edges loop
def isLoopOld(color,v1,v2):
    vStart, vEnd = v1, v2
    vBefore = vEnd
    while True:
        vStartSwitch = False
        for neighbor in vClass.adjLists[vStart]:
            vPair = neighbor.sort(vStart)
            if (vPair in eClass.bank and color in eClass.bank[vPair]
                and vPair != vStart.sort(vBefore)):
                vStart = neighbor
                vBefore = vStart
                vStartSwitch = True
                if vStart == vEnd:
                    return True
        if not(vStartSwitch):
            return False
        
#if starts and ends at same vertex, loop
def isLoop(color):
    path = eClass.edgeLists[color]
    return eClass.edgeLists[color][0][0] == eClass.edgeLists[color][-1][1]

#resets current mouse
def onMouseRelease(app, mouseX, mouseY):
    app.currMouse = None

#changes metros position, if reaches station calls helper function to deal
#with passengers and next edge
def updateMetros(app):
    for metro in metros.store:
        if metro.currEdge != None:
            if not(metro.reverse):
                v1, v2 = metro.currEdge
            else:
                v2, v1 = metro.currEdge
            v1.x = app.boardLeft+(v1.col*app.cellWidth)+app.cellWidth/2
            v1.y = app.boardTop+(v1.row*app.cellHeight)+app.cellHeight/2
            v2.x = app.boardLeft+(v2.col*app.cellWidth)+app.cellWidth/2
            v2.y = app.boardTop+(v2.row*app.cellHeight)+app.cellHeight/2
            metro.startx = v1.x
            metro.starty = v1.y
            vdx = v2.x - v1.x
            vdy = v2.y - v1.y
            metro.currdx = vdx/3*(app.steps-metro.time-1)
            metro.currdy = vdy/3*(app.steps-metro.time-1)
            metro.currX = metro.startx + metro.currdx
            metro.currY = metro.starty + metro.currdy
            if almostEqual(metro.currX,v2.x) and almostEqual(metro.currY,v2.y):
                atStationNew(app,metro,v2)
                nextEdge = findNextEdge(metro,metro.currEdge,metro.color)
                metro.time = app.steps
                if nextEdge != None:
                    metro.currEdge = nextEdge
                else:
                    metro.reverse = not(metro.reverse)

#if it is their destination they get off, score goes up
#get on if there is space
def atStationOriginal(app,metro,vertex):
    i = 0
    while i < len(metro.currPassengers):
        person = metro.currPassengers[i]
        res = gettingOffOriginal(person,vertex)
        if res:
            metro.currPassengers.pop(i)
            app.score += 1
        else:
            i += 1
    i = 0
    while len(metro.currPassengers) < metros.capacity and i < len(vClass.currPassengers[vertex]):
        person = vClass.currPassengers[vertex][i]
        res = gettingOnOriginal(person,metro)
        if res:
            metro.currPassengers.append(person)
            vClass.currPassengers[vertex].pop(0)
        else:
            i += 1

#only get off if reached destination
def gettingOffOriginal(passenger,vertex):
    if passenger.type == vertex.type:
        return True

#only get on if destination is on route
def gettingOnOriginal(passenger,metro):
    for v1,v2 in eClass.edgeLists[metro.color]:
        if v1.type == passenger.type or v2.type == passenger.type:
            return True
    return False


#if destination get on, increase score
#if not destination but destination on route, stay on
#if destination not on route, but this vertex offers other routes, get off and stay off til next car
#if destination not on route, and vertex does not have other connects stay on
#always get on
def atStationNew(app,metro,vertex):
    i = 0
    while i < len(metro.currPassengers):
        person = metro.currPassengers[i]
        res = gettingOffNew(person,metro,vertex)
        #print(res,person)
        if res == (True, True):
            metro.currPassengers.pop(i)
            app.score += 1
        elif res == (False, True):
            i += 1
        elif res == (True, False):
            if len(vClass.currPassengers[vertex]) < 6:
                metro.currPassengers.pop(i)
                vClass.currPassengers[vertex].append(person)
                person.justGotOff = True
        elif res == (False,False):
            i += 1
    i = 0
    while len(metro.currPassengers) < metros.capacity and i < len(vClass.currPassengers[vertex]):
        person = vClass.currPassengers[vertex][i]
        res = gettingOnNew(person,metro,vertex)
        if res and not(person.justGotOff):
            metro.currPassengers.append(person)
            vClass.currPassengers[vertex].pop(0)
        else:
            i += 1
    for person in vClass.currPassengers[vertex]:
        person.justGotOff = False

#if is their stop get off
def gettingOffNew(passenger,metro,vertex):
    if passenger.type == vertex.type:
        return (True,True)
    else:
        #use pathfinding
        return pathFinding(passenger,metro,vertex)

#always get on
def gettingOnNew(person,metro,vertex):
    return True

#goes through all edges on current metro, if one is destination stay on
#else if current vertex has other metro lines on it get off
def pathFinding(passenger,metro,vertex):
    for v1,v2 in eClass.edgeLists[metro.color]:
        if v1.type == passenger.type or v2.type == passenger.type:
            return (False,True)
    for neighbor in vClass.adjLists[vertex]:
        vPair = neighbor.sort(vertex)
        if vPair in eClass.bank:
            for color in eClass.bank[vPair]:
                if color != metro.color:
                    return (True, False)
    return (False,False)

#return index in list if in, else return None
def listFind(L,item):
    for i in range(len(L)):
        poss = L[i]
        if poss == item:
            return i  

#finds currEdge in list, finds next one based on if metro in reverse or not
#if end of route and not loop, swtich direction
#if loop keep going
def findNextEdge(metro,currEdge,color):
    v1, v2 = currEdge
    index = listFind(eClass.edgeLists[color],currEdge)
    if index == None:
        index = listFind(eClass.edgeLists[color],(v2,v1))
    if not(isLoop(color)):
        if ((index == 0 and metro.reverse)
            or (index == len(eClass.edgeLists[color])-1 and not(metro.reverse))):
            return None
        else:
            if metro.reverse:
                nextEdge = eClass.edgeLists[color][index-1]
            else:
                nextEdge = eClass.edgeLists[color][index+1]
            return nextEdge
    else:
        if metro.reverse:
            if index == 0:
                return eClass.edgeLists[color][-1]
            else:
                return eClass.edgeLists[color][index-1]
        else:
            if index == len(eClass.edgeLists[color])-1:
                return eClass.edgeLists[color][0]
            else:
                return eClass.edgeLists[color][index+1]

#if all full, can't spawn more
def maxPassengers():
        count = 0
        for vertex in vClass.currPassengers:
           if len(vClass.currPassengers[vertex]) == 6:
               count += 1
        if count == len(vClass.currPassengers):
           return True
        else:
           return False

#Classes and Storage
################################################################################
class vClass:
    tCount = 3
    currPassengers = {}
    store = []
    adjLists = {}
    count = len(store)

    def __init__(self,app,type = None):
        while True:
            self.row = random.choice([0,1,app.rows-2,app.rows-1])
            self.col = random.choice([0,1,app.cols-2,app.cols-1])
            count = 0
            for vertex in vClass.store:
                if (vertex.row, vertex.col) == (self.row, self.col):
                    count += 1
            if count > 0:
                continue
            break
        if type == None:
            self.type = random.randint(3,vClass.tCount+2)
        else:
            self.type = type
        self.timer = False
        self.timeLeft = 20
        self.timeLeft = 30
        vClass.store.append(self)
        vClass.currPassengers[self] = []
        vClass.adjLists[self] = set()
    
    def __repr__(self):
        return f"Row, Col = ({self.row},{self.col}), Type = {self.type}"
    
    def sort(self,other):
        if self.row**2 + self.col**2 > other.row**2 + other.col**2:
            return (self,other)
        elif self.row**2 + self.col**2 == other.row**2 + other.col**2:
            if self.row > other.row:
                return (self,other)
            else:
                return (other,self)
        else:
            return (other,self)

    def __eq__(self,other):
        if type(other) == type(self):
            if self.row == other.row and self.col == other.col:
                return True
        return False
    
    def __hash__(self):
        return hash((self.row,self.col))

class eClass:
    edgeCount = {}
    edgeLists = {}
    tCount = 2
    store = []
    bank = {}
    allColors = ["red","blue","yellow","green","orange","purple"]
    currColors = allColors[:tCount]
    def __init__(self,v1,v2,type,time = None):
        vPair = v1.sort(v2)
        self.type = type
        if eClass.edgeCount[type] == 0:
            metros(v1,v2,type,time)
        if eClass.edgeLists[type] == []:
            eClass.edgeLists[type].append((v1,v2))
        else:
            vStart = v1
            vEnd = v2
            if len(eClass.edgeLists[type]) == 0:
                eClass.edgeLists[type].append((vStart,vEnd))
            elif len(eClass.edgeLists[type]) == 1:
                edge = eClass.edgeLists[type][0]
                if edge[0] == vStart:
                    eClass.edgeLists[type].insert(0,(vEnd,vStart))
                else:
                    eClass.edgeLists[type].append((vStart,vEnd))
            else:
                leftEdge = eClass.edgeLists[type][0]
                if leftEdge[0] == vStart:
                    eClass.edgeLists[type].insert(0,(vEnd,vStart))
                else:
                    eClass.edgeLists[type].append((vStart,vEnd))
        eClass.edgeCount[type] += 1
        if vPair in eClass.bank:
            eClass.bank[vPair].add(self.type)
        else:
            eClass.bank[vPair] = {self.type}
        self.vPair = vPair
        self.type = type
        eClass.store.append(self)

#checks station, if full starts timer, once 0 game over
def checkTimer(app):
    for vertex in vClass.store:
        if len(vClass.currPassengers[vertex]) == 6 and not(vertex.timer):
            vertex.timer = True
        elif len(vClass.currPassengers[vertex]) == 6 and vertex.timer:
            vertex.timeLeft -= 1
            if vertex.timeLeft == 0.0:
                app.gameOver = True
        elif vertex.timer and len(vClass.currPassengers[vertex]) < 6:
            vertex.timer = False
            vertex.timeLeft = 30

class passengers:
    store = []
    count = len(store)
    def __init__(self):
        if not(maxPassengers()):
            while True:
                self.type = random.choice(vClass.store).type
                self.v = random.choice(vClass.store)
                self.justGotOff = False
                if self.v.type == self.type:
                    continue
                if len(vClass.currPassengers[self.v]) < 6:
                    vClass.currPassengers[self.v].append(self)
                    break
                else:
                    continue
        passengers.store.append(self)
    def __repr__(self):
        return f"{self.type}"

class metros:
    store = []
    capacity = 4
    def __init__(self,v1,v2,color,time=None):
        self.time = time
        self.color = color
        self.currEdge = (v1,v2)
        self.currX = None
        self.currY = None
        self.currdx = 0
        self.currdy = 0
        self.startx = None
        self.starty = None
        self.reverse = False
        self.currPassengers = []
        metros.store.append(self)

################################################################################

def main():
    runApp()
main()