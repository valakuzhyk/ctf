from pwn import remote
import time
import math
import Queue

def printLines(lines):
    print "Printing lines:"
    for l in lines:
        print l

def SolveProblem(string, maps):
    fields = string.split()
    target = int(fields[8])
    using = int(fields[13].strip(":"))
    return maps[using][target]


    # doubleDigit = str(using) + str(using)
    # if target > int(doubleDigit):
    #      return doubleDigit + constructString(target, using, 0, int(doubleDigit))
    # if target > using:
    #     return str(using) + constructString(target, using, 0, using) 
    # return str(using) + "/" + str(using) + constructString(int(target), int(using), 0, 1)




def constructStringUsingOne(target):
    if target == 1:
        return "1"
    if target == 2:
        return "1+1"
    if target == 3:
        return "1+1+1"
    if target == 4:
        return "1+1+1+1"
    if target == 8:
        return "(1+1)*(1+1)*(1+1)"

    subTarget = math.floor(math.sqrt(target))
    output = "(" +constructStringUsingOne(subTarget) +")*("+constructStringUsingOne(subTarget) +")" 
    if subTarget * subTarget == target:
        return output
    return output + "+" + constructStringUsingOne(target - subTarget ** 2)

def constructString(target, using, currentTotal, currentNumber):
    if target == currentTotal or target == currentNumber + currentTotal:
        return ""
    if currentTotal + currentNumber> target:
        print "You done fucked up now: ", currentTotal, target
        exit()
    if target >= currentTotal + currentNumber * using and using != 1:
        additional = "*"+str(using) 
        currentNumber = currentNumber * using
        return additional + constructString(target, using, currentTotal, currentNumber)
    # We are going to start a new number. Add the currentNumber in
    currentTotal = currentTotal + currentNumber

    doubleDigit = str(using) + str(using)

    if target == (currentTotal + using - 1):
        return "+" + str(using) + "-" + str(using) + "/" + str(using) 
    if target == (currentTotal + int(doubleDigit) - 1):
        return "+" + doubleDigit + "-" + str(using) + "/" + str(using) 
    if target >= currentTotal + int(doubleDigit):
        additional = "+" + doubleDigit
        currentNumber = int(doubleDigit)
        return additional + constructString(target, using, currentTotal, currentNumber)
    if target >= currentTotal + using:
        additional = "+"+str(using) 
        currentNumber =  using
        return additional + constructString(target, using, currentTotal, currentNumber)
    additional = "+"+str(using)+"/"+str(using)
    currentNumber = 1
    return additional + constructString(target, using, currentTotal, currentNumber)

def main():
    maps = ConstructMaps()
    conn = remote('sdp01.3dsctf.org', 8003)
    conn.send('start\n')
    print "Sent start"
    lines = conn.recvuntil(":", timeout = 2)
    print lines
    line = conn.recvuntil(":", timeout = 2)
    print line 

    while 1 ==1:
        try:
            line = conn.recvuntil(":", timeout = 2)
            

            print line 
            
            result = SolveProblem(line, maps)
            print "My solution: " + result
            conn.send(result)
            time.sleep(0.05)
        except Exception:
            print line
            line = conn.recvuntil("}", timeout = 2)
            print line



# new approach
operators = ["+-*/_"]
maxLength = 15
maxVal = 100
minVal = -20
queue = Queue.Queue()
def CreateMap(using):
    valToString = dict()
    queue.put(using)
    while not queue.empty():
        string = queue.get()
        newStrings = ProcessNextInQueue(string, using, valToString)
        for s in newStrings:
            queue.put(s)
    for i in xrange(maxVal):
        if i not in valToString:
            constructNumberInMap(i,using,valToString)
    return valToString

def ProcessNextInQueue(string, using, valToString):
    if len(string) > maxLength:
        return []
    value = eval(string)
    if value > maxVal or value < minVal:
        return []
    if value not in valToString:
        valToString[value] = string        
    elif len(valToString[value]) > string:
            valToString[value] = string
    returnStrings =  [string+"+"+using, string+"-"+using, string+"*"+using, string+"/"+using, string+using]
    return returnStrings

def constructNumberInMap(i, using, valToString):
    bestString = "12345678911234567892123456789312"
    for j in xrange(minVal,i):
        if j in valToString and i-j in valToString:
            candidateString = valToString[j] + "+" + valToString[i-j]
            if len(candidateString) > 31:
                continue
            if len(bestString) > len(candidateString):
                bestString = candidateString
    if len(bestString) > 31:
        print "No way to construct " + str(i) + " using " + str(using)
    else:
        valToString[i] = bestString

def ConstructMaps():
    numberMaps = dict()
    for i in xrange(1,10):
        numberMaps[i] = CreateMap(str(i))
    return numberMaps

main()