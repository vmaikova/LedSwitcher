import sys
from urllib.request import urlopen

def parseLine(line):
    # Remove first and final spaces
    line = line.strip()

    # replace some commands with version that has no space inside not to deal with different amount of spaces
    if "turn on" in line:
        line = line.replace("turn on", "turnon")
    if "turn off" in line:
        line = line.replace("turn off", "turnoff")

    # split by space.
    parsedParams = line.split(" ")


    # if value = "turnon" system sets variables startX, srartY, endX and endY and
    # assignes them into results array, that is returned at the end of the statement. 
    # When first item in result array is "turnon" system is setting itself to on state
    
    if parsedParams[0] == "turnon":
        startX = parsedParams[1].split(",")[0].strip()
        startY = parsedParams[1].split(",")[1].strip()
        endX = parsedParams[3].split(",")[0].strip()
        endY = parsedParams[3].split(",")[1].strip()
        result = ["turnon", int(startX), int(startY), int(endX), int(endY)]
    # returning results array with assigned values
        return result
    
    
    # if value = "turnoff" system sets variables startX, startY, endX, endY and 
    # assignes them into results array that is returned at the end of the statement.
    # When first item in in result array is "turnoff" system is setting itself to off state
    
    elif parsedParams[0] == "turnoff":
        startX = parsedParams[1].split(",")[0].strip()
        startY = parsedParams[1].split(",")[1].strip()
        endX = parsedParams[3].split(",")[0].strip()
        endY = parsedParams[3].split(",")[1].strip()
        result = ["turnoff", int(startX), int(startY), int(endX), int(endY)]
    # returning results array with assigned values
        return result


    # if value = "switch" system sets variables startX, startY, endX, endY and 
    # assignes them into results array that is returned at the end of the statement.
    # When first item in in result array is "switch" system is setting itself to switch state
    
    elif parsedParams[0] == "switch":
        startX = parsedParams[1].split(",")[0].strip()
        startY = parsedParams[1].split(",")[1].strip()
        endX = parsedParams[3].split(",")[0].strip()
        endY = parsedParams[3].split(",")[1].strip()
        result = ["switch", int(startX), int(startY), int(endX), int(endY)]
    # returning results array with assigned values
        return result

    # the method must return something!
    return ["nothing"]


    # opening and reading a file/url
def parseFile(filename):
    # setting readSize to false as default value
    readSize = False
    # if file name contains http (file should be downloaded from http source) system set decode to utf-8 standards
    # and returns size and input
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
    # else if file is not from http, for example if its passed from desktop
    else:
        with open(filename) as f:
            size = int(f.readline())
            inputs = []
            for line in f:
                if len(line) > 1:
                    inputs.append(parseLine(line))
            return size, inputs
        f.closed
        
    # Creates an empty display of desired size represented by 2 dimension array
def getDisplayOf(size):
    display = []
    for x in range(0, size):
        row = []
        for y in range(0, size):
            row.append(False)
        display.append(row)
    return display

    # System changes states according to parameters x, y, state in provided display
def changeState(x, y, state, display):
    if state == "switch":
        boolean = display[x][y]
        boolean ^= True
        display[x][y] = boolean
    else:
        if state == "turnon":
    # Setting display values to true        
            display[x][y] = True
        else:
    # Otherwise to false        
            display[x][y] = False

    return display

    # If system meets any criteria except of "nothing"
    # it applies instructions based on instruction on to array provided in display variable
def applyIstruction(display, instruction):
    if instruction[0] != "nothing":
        for x in range(instruction[1], instruction[3] + 1):
            for y in range(instruction[2], instruction[4] + 1):
                changeState(x, y, instruction[0], display)
        return display
    return display

    # System is looping through values in display array to count all items of two dimensional array set
    # to True what in this case represents ON state of the pixel
def countOnPixel(display):
    count = 0
    for row in display:
        for pixel in row:
            if pixel == True:
                count += 1
    return count

    # Function that wraps up all the task together 
def taskResult(filename):
    size, inputs = parseFile(filename)

    display = getDisplayOf(size)

    # Looping through inputs and applying instructions on the display
    for instruction in inputs:
        display = applyIstruction(display, instruction)

    # Returning amount of ON pixels of the display after applying all the instructions
    return countOnPixel(display)

def main():
    # Printing arguments of taskResults
    print(taskResult(sys.argv[1]))

if __name__ == '__main__':
    """Run this if its the root python file."""
    print(taskResult(sys.argv[1]))
