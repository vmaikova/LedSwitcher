import sys
from urllib.request import urlopen

def parseLine(line):
    # Remove sirst and final spaces
    line = line.strip()

    # clean iput
    if "turn on" in line:
        line = line.replace("turn on", "turnon")
    if "turn off" in line:
        line = line.replace("turn off", "turnoff")

    # split by space.
    parsedParams = line.split(" ")

    if parsedParams[0] == "turnon":
        startX = parsedParams[1].split(",")[0].strip()
        startY = parsedParams[1].split(",")[1].strip()
        endX = parsedParams[3].split(",")[0].strip()
        endY = parsedParams[3].split(",")[1].strip()
        result = ["turnon", int(startX), int(startY), int(endX), int(endY)]
        return result

    elif parsedParams[0] == "turnoff":
        startX = parsedParams[1].split(",")[0].strip()
        startY = parsedParams[1].split(",")[1].strip()
        endX = parsedParams[3].split(",")[0].strip()
        endY = parsedParams[3].split(",")[1].strip()
        result = ["turnoff", int(startX), int(startY), int(endX), int(endY)]
        return result

    elif parsedParams[0] == "switch":
        startX = parsedParams[1].split(",")[0].strip()
        startY = parsedParams[1].split(",")[1].strip()
        endX = parsedParams[3].split(",")[0].strip()
        endY = parsedParams[3].split(",")[1].strip()
        result = ["switch", int(startX), int(startY), int(endX), int(endY)]
        return result

    # the method must return somthing!
    return ["nothing"]

def parseFile(filename):
    readSize = False
    if filename[:4] == "http":
        size = 0
        inputs = []
        for line in urlopen(filename):
            line = line.decode("utf-8")
            line = line.strip()
            if readSize == False:
                size = int(line)
                readSize = True
            elif len(line) > 1:
                inputs.append(parseLine(line))
        return size, inputs
    else:
        with open(filename) as f:
            size = int(f.readline())
            inputs = []
            for line in f:
                if len(line) > 1:
                    inputs.append(parseLine(line))
            return size, inputs
        f.closed

def getDisplayOf(size):
    display = []
    for x in range(0, size):
        row = []
        for y in range(0, size):
            row.append(False)
        display.append(row)
    return display

def changeState(x, y, state, display):
    if state == "switch":
        boolean = display[x][y]
        boolean ^= True
        display[x][y] = boolean
    else:
        if state == "turnon":
            display[x][y] = True
        else:
            display[x][y] = False

    return display

def applyIstruction(display, instruction):
    if instruction[0] != "nothing":
        for x in range(instruction[1], instruction[3] + 1):
            for y in range(instruction[2], instruction[4] + 1):
                changeState(x, y, instruction[0], display)
        return display
    return display

def countOnPixel(display):
    count = 0
    for row in display:
        for pixel in row:
            if pixel == True:
                count += 1
    return count

def taskResult(filename):
    size, inputs = parseFile(filename)

    display = getDisplayOf(size)

    for instruction in inputs:
        display = applyIstruction(display, instruction)

    return countOnPixel(display)

def main():
    print(taskResult(sys.argv[1]))

if __name__ == '__main__':
    """Run this if its the root python file."""
    print(taskResult(sys.argv[1]))
