import sys

class xyCoordinates:
    x = -1
    y = -1
    def __init__(self, x, y):
        self.x = x
        self.y = y

def checkXYValid(x, y, roomDim):
    if x < 0 or x >= roomDim.x:
        return False
    if y < 0 or y >= roomDim.y:
        return False
    return True

def checkInstructionsValid(instructions):
    for ins in instructions:
        if not (ins == 'N' or ins == 'S' or ins == 'W' or ins == 'E'):
            return False
    return True

def parseInput(inputFile):
    if inputFile == '':
        return;
    with open(inputFile, 'r') as inputFile:
        input = (inputFile.read().split('\n')[: -1])
        dirtPos = set()
        for i, row in enumerate(input):
            row = row.split(' ')
            if i == 0: # Case for room dimension
                if int(row[0]) > 0 and int(row[1]) > 0:
                    roomDim  = xyCoordinates(int(row[0]), int(row[1]))
                    continue
                else:
                    sys.stdout.write("Dimension is not valid!\n")
                    sys.exit()
            if i == 1: # Case for initial position
                if checkXYValid(int(row[0]), int(row[1]), roomDim):
                    initPos = xyCoordinates(int(row[0]), int(row[1]))
                    continue
                else:
                    sys.stdout.write("Initial positon is not valid!\n")
                    sys.exit()
            if i == len(input) - 1: # Case for all the instructions
                instructions = list(str(row))
                instructions = instructions[2: len(instructions)-2]
                if not checkInstructionsValid(instructions):
                    sys.stdout.write("Instructions are not valid!\n")
                    sys.exit()
            else: # Case for all the obstacles' positions
                if checkXYValid(int(row[0]), int(row[1]), roomDim):
                    dirtPos.add((int(row[0]), int(row[1])))
                    continue
                else:
                    sys.stdout.write("Dirt positon is not valid!\n")
                    sys.exit()
        return (roomDim, initPos, instructions, dirtPos)

def computeNextPos(ins, currPos, roomDim):
    if ins == 'N':
        tempY = currPos.y + 1
        if tempY >= roomDim.y:
            tempY = roomDim.y - 1
        currPos.y = tempY
    elif ins == 'S':
        tempY = currPos.y - 1
        if tempY < 0:
            tempY = 0
        currPos.y = tempY
    elif ins == 'E':
        tempX = currPos.x + 1
        if tempX >= roomDim.x:
            tempX = roomDim.x - 1
        currPos.x = tempX
    elif ins == 'W':
        tempX = currPos.x - 1
        if tempX < 0:
            tempX = 0
        currPos.x = tempX
    return currPos

def computeCleanDirtNum(currPos, cleanNum, dirtPos):
    if (currPos.x, currPos.y) in dirtPos:
        cleanNum = cleanNum + 1
        dirtPos.remove((currPos.x, currPos.y))
    return cleanNum

def roombaMove(roomDim, initPos, instructions, dirtPos):
    currPos = initPos
    cleanNum = 0
    for ins in instructions:
        cleanNum = computeCleanDirtNum(currPos, cleanNum, dirtPos)
        currPos = computeNextPos(ins, currPos, roomDim)
    return (cleanNum, currPos)

if __name__ == "__main__":
    (roomDim, initPos, instructions, dirtPos) = parseInput("input.txt")
    (cleanNum, currPos) = roombaMove(roomDim, initPos, instructions, dirtPos)
    sys.stdout.write(str(currPos.x) + ' ' + str(currPos.y) + '\n')
    sys.stdout.write(str(cleanNum) + '\n')
