import random, copy

# CONSTANT VALUES

DIMENSION = 9
EMPTY_VALUE = 0

## --- FUNCTIONS ---

# intersection of two lists
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def numberOfDuplicates(l):
    return list(set([x for x in l if l.count(x) > 1]))

# given a .txt file, create the matrix
def createBoard(file):
    board = []
    f = open(file, "r")
    text = f.readlines()
    for row in text:
        board.append(list(map(int, row.replace('\n',''))))
    f.close()
    return board

# given the name of the algorithm, the file name and the board, writes the board in a new .txt file in the results/technique folder
def writeBoard(technique, filename, board):
    f = open(f"./results/{technique}/{filename}", "w+")
    for row in board:
        f.write(str(row).replace('[', '').replace(']','').replace(', ', '') + '\n')
    f.close()

# printing the matrix
def printBoard(board):
    for row in board:
        print(str(row).replace('[', '').replace(']','').replace(', ', ''))



## --- COSTRAINTS ---

# check if a given value can be inserted in a row: if the count > 1, then the value cannot be inserted in the row; otherwise it can.
def checkRow(value, row, board):
    count = 0
    for col in range(0, DIMENSION):
        if board[row][col] == value:
            count += 1
    if count > 1:
        return False
    return True

# check if a given value can be inserted in a column: if the count > 1, then the value cannot be inserted in the column; otherwise it can.
def checkColumn(value, col, board):
    count = 0
    for row in range(0, DIMENSION):
        if board[row][col] == value:
            count += 1
    if count > 1:
        return False
    return True

# check if a given value can be inserted in a box: if the count > 1, then the value cannot be inserted in the box; otherwise it can.
def checkBox(value, row, col, board):
    count = 0
    for i in range((row//3) * 3, (row//3) * 3 + 3):
        for j in range((col//3) * 3, (col//3) * 3 + 3):
            if board[i][j] == value:
                count += 1
    if count > 1:
        return False
    return True

# check if a value can be inserted a given position of the board, according to the costraints of the game
def checkCostraints(val, row, col, board):
    if not checkRow(val, row, board) or not checkColumn(val, col, board) or not checkBox(val, row, col, board):
        return False
    return True

# check if the solution is completed and if it is corrected
def checkSolution(board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if board[row][col] == 0 or not checkCostraints(board[row][col], row, col, board):
                return False
    return True


## --- DOMAINS ---

# given a row, returns the list of possible values that can be inserted
def getRowDomain(row, board):
    domain = [int(x) for x in range(1, DIMENSION + 1)]
    for col in range(0, DIMENSION):
        val = board[row][col]
        if val in domain:
            domain.remove(val)
    return domain

# given a column, returns the list of possible values that can be inserted
def getColDomain(col, board):
    domain = [int(x) for x in range(1, DIMENSION + 1)]
    for row in range(0, DIMENSION):
        val = board[row][col]
        if val in domain:
            domain.remove(val)
    return domain

# given a box, returns the list of possible values that can be inserted
def getBoxDomain(row, col, board):
    domain = [int(x) for x in range(1, DIMENSION + 1)]
    for i in range((row//3) * 3, (row//3) * 3 + 3):
        for j in range((col//3) * 3, (col//3) * 3 + 3):
            val = board[i][j]
            if val in domain:
                domain.remove(val)
    return domain

# given a position in the board, returns the list of possible values that can be inserted
def getDomainCell(row, col, board):
    l1 = getRowDomain(row, board)
    l2 = getColDomain(col, board)
    l3 = getBoxDomain(row, col, board)
    return intersection(intersection(l1, l2), l3)

# given a board, returns the list of all the possible values that each position can take. The domain of a non-empty cell is the value of the cell
def getAllDomains(board):
    domains = []
    for row in range(0, DIMENSION):
        for col in range(0, DIMENSION):
            if board[row][col] == EMPTY_VALUE:
                domains.append(getDomainCell(row, col, board))
            else:
                domains.append([board[row][col]])
    return domains

# given a domain of a cell and the value of the cell, the function returns the number of possible values that the cell can take
def getLenDomain(domain, cellValue):
    if (len(domain) == 1 and domain[0] == cellValue): 
        return 10
    else:
        if cellValue != 0:
            return len(domain.remove(cellValue)) 
        else:
            return len(domain)

# gets the list of the length of the domain of each cell 
def getListMapDomain(domain, board):
    map = []
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            map.append(getLenDomain(domain[row * DIMENSION + col], board[row][col]))
    return map

# gets the position of the cell with the minimum length domain 
def getNextMinimumDomain(domain, board):
    listMapDomain = getListMapDomain(domain, board)
    minimumFirstList = min(listMapDomain)
    if minimumFirstList == 10 : return None
    index = listMapDomain.index(minimumFirstList)
    return(int(index / DIMENSION), index % DIMENSION)


## -- GENERATION OF VALUES --

# the function fills the empty values of the board with values contained in the domain of each box
# returns the new board and the list of filled positions  
def generateRandomStates(board):
    insertedValuesPosition = []
    for row in range(0,DIMENSION):
        for col in range(0, DIMENSION):
            possibleValues = getBoxDomain(row, col, board)
            for i in range((row//3) * 3, (row//3) * 3 + 3):
                for j in range((col//3) * 3, (col//3) * 3 + 3):
                    if board[i][j] == 0:
                        board[i][j] = possibleValues.pop(random.randint(0, len(possibleValues) - 1))
                        insertedValuesPosition.append(tuple((i,j)))
    return board, insertedValuesPosition

# returns a list of boxes: each box is a list of the positions in the box
def getBoxes():
    boxlist = []
    for r in range(0,3):
        for c in range(0,3):
            tmp = []
            for i in range((r%3) * 3, (r%3) * 3 + 3):
                for j in range((c%3) * 3, (c%3) * 3 + 3):
                    tmp.append(tuple((i,j)))
            boxlist.append(tmp)
    return boxlist

# randomly swap two values of the same box. If there are no values to swap, return False
def generateNewRandomState(posList, board):
    if posList == []:
        return False
    i = 1
    boxes = getBoxes()
    pos = random.randint(0, DIMENSION - i)
    # print("Numero scelto = ",pos)
    chosenBox = boxes[pos]
    # print("Box = ",chosenBox)
    while len(intersection(posList, chosenBox)) <= 1:
        # print("Entro nel loop")
        i += 1
        boxes.remove(chosenBox)
        pos = random.randint(0, DIMENSION - i)
        chosenBox = boxes[pos]

    if (boxes == []):
        return False

    possiblePositions = intersection(posList, chosenBox)
    # print("Possibili valori da swappare = ", possiblePositions)
    a = random.randint(0, len(possiblePositions) - 1)
    (xA,yA) = possiblePositions[a]
    # print("Coppia scelta = ", (xA, yA))
    b = random.randint(0, len(possiblePositions) - 1)
    while a == b:
        b = random.randint(0, len(possiblePositions) - 1)
    # print("Prima posizione = ", possiblePositions[a])
    # print("Seconda posizione = ", possiblePositions[b])
    # print("BEFORE")
    # printBoard(board)
    xB,yB = possiblePositions[b]
    elem = board[xA][yA]
    board[xA][yA] = board[xB][yB]
    board[xB][yB] = elem
    # print("AFTER")
    # printBoard(board)
    return True


# file = f"boards/easy/easy1.txt"
# board = createBoard(file)
# # print(getBoxes())
# # res = []
# # for row in range(0, DIMENSION):
# #     for col in range(0, DIMENSION):
# #         res += generateValuesBox(row, col, board)
# # print("Posizioni riempite = ",res)
# # printBoard(board)
# res = generateRandomStates(board)
# newBoard = res[0]
# list = res[1]

# printBoard(newBoard)
# print(generateNewRandomState(list, newBoard))
# printBoard(newBoard)
# # print(swap)